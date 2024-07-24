
import __init__
import requests
import NetworkConfig
from os import system, name


def get_clear_prompt() -> None:
    if name == 'nt':
        system('cls') or None
    else:
        system('clear') or None

def choose_clock():
    """Função para escolher um dos relógios disponíveis."""
    get_clear_prompt()
    print("\tEscolha um dos relógios disponíveis:")

    for host in NetworkConfig.host_list:
        print(f"\t{host} - {NetworkConfig.host_list[host]['host']}:{NetworkConfig.host_list[host]['port']}")

    print("\tDigite o número do relógio correspondene:")
    clock = input("\t> ")
    get_clear_prompt()
    return clock


def change_time():
    """Opção para mudar o tempo atual do relógio."""
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
    host, port = NetworkConfig.host_list[clock]["host"], NetworkConfig.host_list[clock]["port"]

    # Requisição para mudar o tempo do relógio
    response = requests.post(f"http://{host}:{port}/{new_time}/change_time")
    if response.status_code != 200:
        print("\tErro ao alterar o tempo do relógio.")
    else:
        print("\tTempo do relógio alterado com sucesso.")


def change_drift():
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
    response = requests.post(f"http://{host}:{port}/{new_drift}/change_drift")
    if response.status_code != 200:
        print("\tErro ao alterar o drift do relógio.")
    else:
        print("\tDrift do relógio alterado com sucesso.")


if __name__ == "__main__":
    get_clear_prompt()
    print("\tBem-vindo ao sistema de sincronização de relógios.")
    print("\tEscolha uma das opções abaixo:")

    while True:
        print("\t1 - Mudar tempo")
        print("\t2 - Mudar drift")
        print("\t3 - Sair")

        option = input("\t> ")

        if option == "1":
            change_time()
        elif option == "2":
            change_drift()
        elif option == "3":
            print("\tSaindo do sistema.")
            break
        else:
            print("\tOpção inválida.")
