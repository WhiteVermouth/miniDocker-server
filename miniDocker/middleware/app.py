from flask import Flask, request, jsonify
from wtforms import Form, StringField, PasswordField, validators
import requests
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/auth", methods=['POST'])
def auth_server():
    form = ServerForm(request.form)
    address = form.address.data
    password = form.password.data
    res = requests.post(url=("http://" + address + "/auth_server"), json={"password": password})
    return jsonify(json.loads(res.text))


class ServerForm(Form):
    address = StringField("address", [validators.Length(max=50)])
    password = PasswordField("password", [validators.Length(max=20)])


@app.route("/list_containers", methods=['POST'])
def standalone_list_containers():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/list_containers"), json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/stop_container", methods=['POST'])
def standalone_stop_container():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/stop_container/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/start_container", methods=['POST'])
def standalone_start_container():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/start_container/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/remove_container", methods=['POST'])
def standalone_remove_container():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/remove_container/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/switch_pause_status", methods=['POST'])
def standalone_switch_pause_status():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/switch_pause_status/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/get_logs", methods=['POST'])
def standalone_get_logs():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/get_logs/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))


@app.route("/get_stats", methods=['POST'])
def standalone_get_stats():
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + "/get_stats/" + args["name"]),
                       json={"token": args["token"]})
    return jsonify(json.loads(res.text))
