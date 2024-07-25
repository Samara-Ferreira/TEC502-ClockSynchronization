"""Módulo principal do projeto."""

from tkinter import *
from os import system, name
from threading import Thread
from datetime import datetime
from API import app, Id, Node
from NetworkConfig import host_list


# pyglet.font.add_file('DS-DIGIB.ttf')

dict_colors = {"1": ["#f461ab", "#ff7ac4"], "2": ["#abf561", "#c5ff7a"], "3": ["#bd13ec", "#dd63ff"],
               "4": ["#6bb5ff", "#8093f1"]}

color_black = "#000000"  # preta
color_white = "#ffffff"  # branca

color = dict_colors[Id][0]
color_light = dict_colors[Id][1]
background = color_black

window = Tk()
window.title("Relógio 1")
window.geometry('435x200')
window.resizable(width=FALSE, height=FALSE)
window.configure(background=background)


def get_clear_prompt() -> None:
    """Função para limpar o terminal no Windows ou no Linux."""

    if name == 'nt':
        system('cls') or None
    else:
        system('clear') or None


def digital_clock() -> None:
    # tempo = datetime.now()
    # hora = tempo.strftime("%H:%M:%S")
    # dia_semana = tempo.strftime("%A")

    time = datetime.now()
    day, hour = Node.control_clock.clock.convert_time()

    l1.config(text=("Relógio " + Id + " | Host: " + host_list[Id]["host"] + " | Porta: " +
                    str(host_list[Id]["port"])).center(50))
    l2.config(text=hour.center(8))
    l2.after(200, digital_clock)
    l3.config(text=("   " + str(day) + " dia(s)").center(23))


def init_server():
    app.run(host="0.0.0.0", port=host_list[Id]["port"], debug=False, threaded=True)


if __name__ == "__main__":
    get_clear_prompt()

    l1 = Label(window, font=("Fixedsys", 10), bg=background, fg=color_light)
    l1.grid(row=0, column=0, sticky=NW, padx=5)
    l2 = Label(window, text="10:05:05", font=('DS-Digital', 90), bg=background, fg=color)
    l2.grid(row=1, column=0, sticky=NW, padx=5)
    l3 = Label(window,  font=("Fixedsys", 23), bg=background, fg=color_light)
    l3.grid(row=2, column=0, sticky=NW, padx=5)

    Thread(target=init_server).start()

    digital_clock()
    window.mainloop()
