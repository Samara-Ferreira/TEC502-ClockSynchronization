
from NetworkConfig import host_list
from API import app, Id
from os import system, name


def get_clear_prompt() -> None:
    if name == 'nt':
        system('cls') or None
    else:
        system('clear') or None


if __name__ == "__main__":
    # get_clear_prompt()

    app.run(host="0.0.0.0", port=host_list[Id]["port"], debug=False, threaded=True)
