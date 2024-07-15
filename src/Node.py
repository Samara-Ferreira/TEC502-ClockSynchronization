
import socket
import requests
from time import sleep
from threading import Thread, Lock
from NetworkConfig import host_list


class Node:
    def __init__(self, id_node):
        self.id_node = id_node
        self.is_leader = False
        self.id_leader = None
        self.lock = Lock()
        Thread(target=self.start_server).start()
        Thread(target=self.check_nodes).start()

    # Método para iniciar o servidor
    def start_server(self):
        try:
            # Inicializa o servidor
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_port = host_list[self.id_node]["port"] - 1000
            server.bind((host_list[self.id_node]["host"], new_port))
            server.listen(5)
            print(f"Servidor iniciado no ip {host_list[self.id_node]['host']} e porta {host_list[self.id_node]['port']}!")
            while True:
                server.accept()

        except OSError:
            print("Erro ao iniciar o servidor.")

    # Método para iniciar a eleição
    def start_election(self):
        # Encontrar o nó ativo com maior id
        max_id = self.find_max_id()

        # Mensagem para o próprio líder: nó que iniciou a eleição
        if self.id_node == max_id:
            self.set_leader()

        # Mensagem para o líder: outro nó
        else:
            try:
                requests.post(f"http://{host_list[max_id]['host']}:{host_list[max_id]['port']}/elect_leader",
                              timeout=5)
            except requests.exceptions.RequestException:
                pass

    # Método para atribuir os dados do líder
    def set_leader(self):
        if not self.is_leader:
            self.is_leader = True
            self.id_leader = self.id_node
            print(f"O nó {self.id_node} é o líder!")

            # Depois da atualização, envia confirmação para os outros nós
            for id in host_list:
                if id != self.id_node and host_list[id]["active"]:
                    try:
                        requests.post(f"http://{host_list[id]['host']}:{host_list[id]['port']}/{self.id_node}"
                                      f"/confirm_leader", timeout=5)
                    except requests.exceptions.RequestException:
                        pass

    # Método para confirmar o líder
    def confirm_leader(self, id):
        self.id_leader = id
        self.is_leader = False
        print(f"O nó {self.id_node} confirmou o líder {id}!")
        Thread(target=self.check_leader, args=(id,)).start()

        return "Líder confirmado com sucesso! ID do node: " + str(self.id_node)

    # Método para encontrar o nó ativo com maior id
    def find_max_id(self):
        max_id = self.id_node
        for id in host_list:
            if id != self.id_node and host_list[id]["active"] and id > max_id:
                max_id = id
        return max_id

    # Método para verificar se outros nós estão ativos
    def check_nodes(self):
        for id in host_list:
            # Não é necessário verificar o próprio nó
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

                    try:
                        # Verifica se o nó é o líder
                        check_leader = requests.get(f"http://{host_list[id]['host']}:{host_list[id]['port']}"
                                                    f"/get_leader", timeout=5)
                    except requests.exceptions.RequestException:
                        continue

                    # Caso seja o lider
                    if check_leader.json()["is_leader"]:
                        self.id_leader = id
                        print(f"Na função check_nodes, o nó {id} é o líder!")
                        # Inicia verificação continua se o líder está ativo
                        Thread(target=self.check_leader, args=(id,)).start()
                        return

                except (socket.timeout, socket.error):
                    # Caso o nó não esteja ativo
                    print("Nó inativo! ", id)
                    if host_list[id]["active"]:
                        host_list[id]["active"] = False

        # Verificar se há outro nó ativo
        if self.check_active_nodes():
            # Inicia eleição, já que há outros nós ativos
            self.start_election()

    def check_online_nodes(self):
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

    # Método para verificar se há pelo menos outro nó ativo
    def check_active_nodes(self):
        for id in host_list:
            if id != self.id_node and host_list[id]["active"]:
                return True
        return False

    # Método para verificar continuamente se o líder está ativo
    def check_leader(self, id):
        while True:
            try:
                timeout = 5
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                sock.close()

            except (socket.timeout, socket.error):
                # Caso o líder caia
                print("Líder caiu! ", id)
                Thread(target=self.check_online_nodes).start()
                break
            sleep(5)

    # Método para retornar informações do nó
    def get_info(self):
        return {"id": self.id_node, "is_leader": self.is_leader}
