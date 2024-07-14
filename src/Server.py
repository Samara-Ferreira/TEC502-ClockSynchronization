

import socket
from NetworkConfig import host_list


class Server:
    def __init__(self, id):
        self.id = id
        self.start_server()

    # Método para iniciar o servidor
    def start_server(self):
        try:
            # Inicializa o servidor
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_port = host_list[self.id]["port"] - 1000
            server.bind((host_list[self.id]["host"], new_port))
            server.listen(5)
            print(f"Servidor iniciado no ip {host_list[self.id]['host']} e porta {host_list[self.id]['port']}!")

            while True:
                server.accept()

        except OSError:
            print("Erro ao iniciar o servidor.")
