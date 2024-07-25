"""Módulo principal da aplicação."""

import __init__
import requests
import NetworkConfig
from os import system, name
from threading import Thread


def get_clear_prompt() -> None:
    """Função para limpar o terminal no Windows ou no Linux."""

    if name == 'nt':
        system('cls') or None
    else:
        system('clear') or None


def choose_clock() -> str:
    """Função para escolher um dos relógios disponíveis."""

    get_clear_prompt()
    print("\t| Escolha um dos relógios disponíveis: ")

    for host in NetworkConfig.host_list:
        print(f"\t{host} - {NetworkConfig.host_list[host]['host']}:{NetworkConfig.host_list[host]['port']}")

    print("\tDigite o número do relógio correspondente:")
    clock = input("\t> ")
    get_clear_prompt()
    return clock


def change_time() -> None:
    """Função para mudar o tempo atual do relógio."""

    get_clear_prompt()
    print("\tDigite o novo tempo do relógio:")
    new_time = input("\t> ")
    get_clear_prompt()

    try:
        new_time = int(new_time)
    except ValueError:
        print("\tValor inválido.")
        return

    clock = choose_clock()
    host1, port1 = NetworkConfig.host_list[clock]["host"], NetworkConfig.host_list[clock]["port"]

    threads_list = []
    for clock in NetworkConfig.host_list:
        host, port = NetworkConfig.host_list[clock]["host"], NetworkConfig.host_list[clock]["port"]
        thread = Thread(target=request_post_sync, args=(host, port))
        thread.start()
        threads_list.append(thread)

    for thread in threads_list:
        thread.join()

    try:
        response = requests.post(f"http://{host1}:{port1}/{new_time}/change_time", timeout=5)
    except requests.exceptions.RequestException as e:
        print("\tErro ao alterar o tempo do relógio: ", e)
        return

    if response.status_code != 200:
        print("\tErro ao alterar o tempo do relógio.")
    else:
        print("\tTempo do relógio alterado com sucesso.")


def request_post_sync(host, port) -> None:
    """Função para enviar uma requisição POST para sincronizar os relógios."""

    try:
        requests.post(f"http://{host}:{port}/change_sync", timeout=5)
    except requests.exceptions.RequestException:
        print("\tErro ao sincronizar os relógios.")


def change_drift() -> None:
    """Função para mudar o drift do relógio."""

    get_clear_prompt()
    print("\tDigite o novo drift do relógio:")
    new_drift = input("\t> ")
    get_clear_prompt()

    try:
        new_drift = float(new_drift)
    except ValueError:
        print("\tValor inválido.")
        return

    clock = choose_clock()
    host, port = NetworkConfig.host_list[clock]["host"], NetworkConfig.host_list[clock]["port"]

    try:
        response = requests.post(f"http://{host}:{port}/{new_drift}/change_drift")
    except requests.exceptions.RequestException:
        print("\tErro ao alterar o drift do relógio.")
        return

    if response.status_code != 200:
        print("\tErro ao alterar o drift do relógio.")
    else:
        print("\tDrift do relógio alterado com sucesso.")


if __name__ == "__main__":
    get_clear_prompt()
    print("\t| Bem-vindo ao sistema de sincronização de relógios |")
    print("\n\t|Escolha uma das opções abaixo:")

    while True:
        print("\n\t[1] Mudar o tempo do relógio")
        print("\t[2] Mudar o drift do relógio")
        print("\t[0] Sair")

        option = input("\t> ")

        if option == "0":
            print("\tSaindo do sistema.")
            break
        elif option == "1":
            change_time()
        elif option == "2":
            change_drift()
        else:
            print("\tOpção inválida.")
