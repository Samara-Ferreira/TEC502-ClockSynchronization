"""Módulo para controlar o nó."""

import socket
import requests
from math import floor
from time import sleep
from threading import Thread
from NetworkConfig import host_list
from ControllerClock import ControllerClock


class Node:
    def __init__(self, id_node: str) -> None:
        """Construtor da classe Node."""

        self.id_node: str = id_node
        self.is_leader: bool = False
        self.id_leader: str = ""
        self.control_clock: ControllerClock = ControllerClock()
        Thread(target=self.check_nodes).start()
        Thread(target=self.start_server).start()

    def start_server(self) -> None:
        """Método para iniciar o servidor."""""

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_port = host_list[self.id_node]["port"] - 1000
            server.bind((host_list[self.id_node]["host"], new_port))
            server.listen(5)
            print(f"| Servidor iniciado no IP {host_list[self.id_node]['host']} e porta {host_list[self.id_node]['port']}!")
            while True:
                server.accept()

        except OSError:
            print("| Erro ao iniciar o servidor.")

    def start_election(self) -> None:
        """Método para iniciar a eleição."""

        max_id = self.find_max_id()     # Encontrar o nó ativo com maior id

        if self.id_node == max_id:      # Mensagem para o próprio líder: nó que iniciou a eleição
            self.set_leader()

        else:   # Mensagem para o líder: outro nó que não iniciou a eleição
            try:
                requests.post(f"http://{host_list[max_id]['host']}:{host_list[max_id]['port']}/elect_leader",
                              timeout=5)
            except requests.exceptions.RequestException:
                pass

    def set_leader(self) -> None:
        """Método para atribuir os dados do líder."""

        if not self.is_leader:
            self.is_leader = True
            self.id_leader = self.id_node
            print(f"| O nó {self.id_node} é o líder!\n")

            for id in host_list:    # Depois da atualização, envia confirmação para os outros nós
                if id != self.id_node and host_list[id]["active"]:
                    try:
                        requests.post(f"http://{host_list[id]['host']}:{host_list[id]['port']}/{self.id_node}"
                                      f"/confirm_leader", timeout=5)
                    except requests.exceptions.RequestException:
                        pass
            Thread(target=self.syncronize_clock).start()

    def confirm_leader(self, id) -> str:
        """Método para confirmar o líder."""

        self.id_leader = id
        self.is_leader = False
        print(f"\n| O nó {self.id_node} confirmou o líder {id}!\n")
        Thread(target=self.check_leader, args=(id,)).start()
        return "Líder confirmado com sucesso! ID do node: " + str(self.id_node)

    def find_max_id(self) -> str:
        """Método para encontrar o nó ativo com maior id."""

        max_id = self.id_node
        for id in host_list:
            if id != self.id_node and host_list[id]["active"] and id > max_id:
                max_id = id
        return max_id

    def check_nodes(self) -> None:
        """Método para verificar se outros nós estão ativos."""

        for id in host_list:
            if id != self.id_node:  # Não é necessário verificar o próprio nó
                try:
                    timeout = 5
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                    sock.close()

                    # Caso o nó esteja inativo
                    if not host_list[id]["active"]:
                        host_list[id]["active"] = True

                    try:
                        # Verifica se o nó é o líder
                        check_leader = requests.get(f"http://{host_list[id]['host']}:{host_list[id]['port']}"
                                                    f"/get_leader", timeout=5)
                    except requests.exceptions.RequestException:
                        continue

                    # Caso seja o lider
                    if check_leader.json()["is_leader"]:
                        self.id_leader = id
                        print(f"\n| O nó {id} é o líder!\n")
                        # Inicia verificação continua se o líder está ativo
                        Thread(target=self.check_leader, args=(id,)).start()
                        return

                except (socket.timeout, socket.error):
                    # Caso o nó não esteja ativo
                    print("\n| Nó inativo! ", id, "\n")
                    if host_list[id]["active"]:
                        host_list[id]["active"] = False

        # Verificar se há outro nó ativo
        if self.check_active_nodes():
            # Inicia eleição, já que há outros nós ativos
            self.start_election()

    def check_online_nodes(self) -> None:
        """Método para verificar se outros nós estão ativos."""
        for id in host_list:
            if id != self.id_node:
                try:
                    timeout = 5
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                    sock.close()

                    # Caso o nó esteja inativo
                    if not host_list[id]["active"]:
                        host_list[id]["active"] = True

                except (socket.timeout, socket.error):
                    # Caso o nó não esteja ativo
                    if host_list[id]["active"]:
                        host_list[id]["active"] = False

        # Verificar se há outro nó ativo
        if self.check_active_nodes():
            # Inicia eleição, já que há outros nós ativos
            self.start_election()

    def check_active_nodes(self) -> bool:
        """Método para verificar se há pelo menos outro nó ativo."""
        for id in host_list:
            if id != self.id_node and host_list[id]["active"]:
                return True
        return False

    def check_leader(self, id) -> None:
        """Método para verificar continuamente se o líder está ativo."""
        while True:
            try:
                timeout = 5
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                sock.close()

            except (socket.timeout, socket.error):
                # Caso o líder caia
                print("\n| Líder caiu! ", id, "\n")
                Thread(target=self.check_online_nodes).start()
                break
            sleep(5)

    def get_info(self) -> dict:
        """Método para retornar o ID do nó e se é líder."""
        return {"id": self.id_node, "is_leader": self.is_leader}

    def syncronize_clock(self) -> None:
        """Verificação periódica, caso seja o líder."""

        sleep(20)
        while self.is_leader:

            print("hora atual lider ", self.control_clock.clock.get_time())
            self.control_clock.is_sync = True
            host_list[self.id_node]["time"] = self.control_clock.clock.get_time()

            threads_list = []
            for id in host_list:
                if id != self.id_node:
                    thread = Thread(target=self.request_get_time, args=(id,))
                    thread.start()
                    threads_list.append(thread)

            # Aguarda o término de todas as threads
            for thread in threads_list:
                thread.join()

            if not self.check_time_node():
                self.is_leader = False
                self.control_clock.is_sync = False
                print("O líder caiu!")

            else:
                time_sync, final_time = self.calculate_time_sync()

                threads_list = []
                for id in host_list:
                    if id != self.id_node and host_list[id]["time"] != -1:
                        thread = Thread(target=self.send_times, args=(id, time_sync, final_time))
                        thread.start()
                        threads_list.append(thread)

                for thread in threads_list:
                    thread.join()

                self.receive_times(time_sync, final_time)
                while self.control_clock.is_sync:
                    pass
                sleep(20)

    def calculate_average(self) -> int:
        """Método para calcular a média dos relógios."""

        sum_time = 0
        num_nodes = 0
        for id in host_list:
            if host_list[id]["time"] != -1:
                sum_time += host_list[id]["time"]
                num_nodes += 1
        return int(sum_time / num_nodes)

    def calculate_time_sync(self) -> tuple[int, int]:
        """Método para calcular o tempo de sincronização."""

        bigger = max([host_list[id]["time"] for id in host_list])
        # print("\nmaior \n", bigger)
        average = self.calculate_average()
        # print("\nmedia \n", average)
        if floor((abs(bigger - average) / 2)) == 0:
            div_time = 1
        else:
            div_time = floor(abs(bigger - average) / 2)

        time_sync = abs(bigger - average) + div_time
        final_time = int(average) + time_sync
        return time_sync, final_time

    def check_time_node(self) -> bool:
        """Método para verificar se há pelo menos outro nó ativo."""

        for id in host_list:
            if id != self.id_node and host_list[id]["time"] != -1:
                return True
        return False

    def request_get_time(self, id) -> None:
        """Método para fazer a requisição do tempo de um nó."""

        try:
            get_time = requests.get(f"http://{host_list[id]['host']}:{host_list[id]['port']}/get_time", timeout=5)
            host_list[id]["time"] = get_time.json()["message"]
        except requests.exceptions.RequestException:
            host_list[id]["active"] = False
            host_list[id]["time"] = -1

    def receive_times(self, time_sync, final_time) -> None:
        """Método para receber os tempos dos outros nós."""

        print("\nTempos recebidos: sincronização - ", time_sync, " final - ", final_time)
        print("Tempo atual:", self.control_clock.clock.get_time(), "\n")

        if (final_time - self.control_clock.clock.get_time()) != 0:
            new_drift = time_sync / abs(final_time - self.control_clock.clock.get_time())
            self.control_clock.clock.set_sync_drift(new_drift)
            Thread(target=self.control_clock.sync_clock, args=(final_time,)).start()
        else:
            self.control_clock.is_sync = False

    def send_times(self, id, time_sync, final_time) -> None:
        """Método para enviar os tempos para os outros nós."""

        try:
            requests.post(f"http://{host_list[id]['host']}:{host_list[id]['port']}"
                          f"/{time_sync}/{final_time}/receive_times", timeout=5)
        except requests.exceptions.RequestException:
            pass
