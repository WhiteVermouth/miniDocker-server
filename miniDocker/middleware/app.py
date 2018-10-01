from flask import Flask, request, jsonify
from wtforms import Form, StringField, PasswordField, validators
import requests
import json

app = Flask(__name__)


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


@app.route("/<function>", methods=['POST'])
def standalone_function(function):
    args = request.get_json()
    res = requests.get(url=("http://" + args["address"] + function + args["name"]), json={"token": args["token"]})
    return jsonify(json.loads(res.text))
