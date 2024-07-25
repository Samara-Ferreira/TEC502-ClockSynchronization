"""Módulo para a API do sistema."""

from os import getenv
from Node import Node
from threading import Thread
from flask import Flask, jsonify


Id = getenv("ID", "1")
Node = Node(Id)

app = Flask(__name__)


@app.route("/elect_leader", methods=["POST"])
def elect_leader():
    """Rota para eleger um líder."""
    Thread(target=Node.set_leader).start()
    return jsonify({"message": "Líder eleito com sucesso! ID do líder:" + str(Node.id_node)})


@app.route("/<string:id>/confirm_leader", methods=["POST"])
def confirm_leader(id):
    """Rota para confirmar o líder."""
    return jsonify({"message": Node.confirm_leader(id)})


@app.route("/<int:time_sync>/<int:final_time>/receive_times", methods=["POST"])
def receive_times(time_sync, final_time):
    """Rota para receber a média dos tempos dos relógios."""
    return jsonify({"message": Node.receive_times(time_sync, final_time)})


@app.route("/<int:time>/change_time", methods=["POST"])
def change_time(time):
    """Rota para mudar o tempo do relógio."""
    return jsonify({"message": Node.control_clock.clock.set_time(time)})


@app.route("/<float:drift>/change_drift", methods=["POST"])
def change_drift(drift):
    """Rota para mudar o drift do relógio."""
    return jsonify({"message": Node.control_clock.clock.set_drift(drift)})


@app.route("/change_sync", methods=["POST"])
def change_sync():
    """Rota para mudar a flag de sincronização."""
    return jsonify({"message": Node.control_clock.set_is_sync()})


@app.route("/get_leader", methods=["GET"])
def get_leader():
    """Rota para obter o líder."""
    return jsonify(Node.get_info())


@app.route("/get_time", methods=["GET"])
def get_time():
    """Rota para obter o horário atual de um relógio."""
    return jsonify({"message": Node.control_clock.get_time()})
