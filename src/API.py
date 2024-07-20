
from flask import Flask, jsonify
from Node import Node
from os import getenv
from threading import Thread


# Variáveis globais
Id = getenv("ID", "1")
Node = Node(Id)

app = Flask(__name__)


# Rota para verificar se é o líder
@app.route("/get_leader", methods=["GET"])
def get_leader():
    return jsonify(Node.get_info())


# Rota para eleger um lider
@app.route("/elect_leader", methods=["POST"])
def elect_leader():
    Thread(target=Node.set_leader).start()
    return jsonify({"message": "Líder eleito com sucesso! ID do líder:" + str(Node.id_node)})


# Rota para confirmar o líder
@app.route("/<string:id>/confirm_leader", methods=["POST"])
def confirm_leader(id):
    return jsonify({"message": Node.confirm_leader(id)})


# Rota para obter o horário atual dos relógios
@app.route("/get_time", methods=["GET"])
def get_time():
    return jsonify({"message": Node.control_clock.get_time()})


# Rota para receber a média dos relógios
@app.route("/<int:time_sync>/<int:final_time>/receive_times", methods=["POST"])
def receive_times(time_sync, final_time):
    return jsonify({"message": Node.receive_times(time_sync, final_time)})
