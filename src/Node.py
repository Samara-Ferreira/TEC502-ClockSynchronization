
import socket
from NetworkConfig import host_list
from threading import Thread, Lock


class Node:
    def __init__(self, id):
        self.id = id
        self.has_leader = False
        self.id_leader = None
        self.lock = Lock()

    def start_election(self):

    # Método para verificar se outros nós estão ativos
    def check_nodes(self):
        for id in host_list:
            if id != self.id:
                try:
                    timeout = 5
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                    sock.close()

                    with self.lock:
                        host_list[id]["active"] = True
                        # Verifica se existe lider - requisição para saber se tem lider


                except (socket.timeout, socket.error):
                    with self.lock:
                        host_list[id]["active"] = False

    # Método para enviar o heartbeat
    def heart_beat(self):
        for id in host_list:
            if id != self.id:
                Thread(target=self.check_server, args=(id,)).start()

    def check_server(self, id):
        while True:
            try:
                timeout = 5
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host_list[id]["host"], (host_list[id]["port"] - 1000)))
                sock.close()

                if not host_list[id]["active"]:
                    return_first = self.is_first_node()
                    if return_first:
                        self.start_election()

                    with self.lock:
                        host_list[id]["active"] = True

            except (socket.timeout, socket.error):
                if host_list[id]["active"]:
                    with self.lock:
                        host_list[id]["active"] = False
