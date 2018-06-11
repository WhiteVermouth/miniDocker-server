from flask import Flask, request
from flask import jsonify
import os
from miniDocker.server.standalone import list_containers
from miniDocker.server.standalone import stop_container
from miniDocker.server.standalone import start_container
from miniDocker.server.standalone import remove_container
from miniDocker.server.standalone import get_logs
from miniDocker.server.standalone import switch_container_pause_status
from miniDocker.server.standalone import get_stats

app = Flask(__name__)
env_var = "MINIDOCKER_CONF"
if os.getenv(env_var) is not None:
    app.config.from_json(os.getenv(env_var))
else:
    app.config.from_json("config.default.json")


@app.before_request
def check_token():
    if str(request.url_rule) == "/auth_server":
        return
    else:
        args = request.get_json()
        if args != None and "token" in args and args["token"] == app.config["TOKEN"]:
            return
    return jsonify({
        "warn": "You have no permission"
    })


@app.route("/auth_server", methods=['POST'])
def auth_server():
    if request.get_json()["password"] == app.config['PASSWORD']:
        return jsonify({
            "status": "success",
            "token": app.config["TOKEN"]
        })
    else:
        return jsonify({
            "status": "failed"
        })


@app.route("/list_containers")
def standalone_list_containers():
    containers = list_containers()
    return jsonify(containers)


@app.route("/stop_container/<name>")
def standalone_stop_container(name):
    return jsonify(stop_container(name))


@app.route("/start_container/<name>")
def standalone_start_container(name):
    return jsonify(start_container(name))


@app.route("/remove_container/<name>")
def standalone_remove_container(name):
    return jsonify(remove_container(name))


@app.route("/switch_pause_status/<name>")
def standalone_switch_pause_status(name):
    return jsonify(switch_container_pause_status(name))


@app.route("/get_logs/<name>")
def standalone_get_logs(name):
    return jsonify(get_logs(name))


@app.route("/get_stats/<name>")
def standalone_get_stats(name):
    res = get_stats(name)
    return jsonify(res)
