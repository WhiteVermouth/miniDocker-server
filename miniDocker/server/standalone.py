from docker.errors import APIError
from docker import from_env

client = from_env()


def list_containers():
    res = []
    containers = client.containers.list(all=True)
    for container in containers:
        c = {}
        if len(container.image.tags) != 0:
            c['image'] = container.image.tags[0]
        else:
            c['image'] = container.image.short_id
        c['name'] = container.name
        c['status'] = container.status
        c['short_id'] = container.short_id
        res.append(c)
    return res


def start_container(name):
    try:
        client.containers.get(name).start()
        return {"status": "success"}
    except(APIError):
        return {"status": "failed"}


def stop_container(name):
    try:
        client.containers.get(name).stop()
        return {"status": "success"}
    except(APIError):
        return {"status": "failed"}


def switch_container_pause_status(name):
    try:
        c = client.containers.get(name)
        if c.status == "paused":
            c.unpause()
        else:
            c.pause()
        return {"status": "success"}
    except(APIError):
        return {"status": "failed"}


def remove_container(name):
    try:
        container = client.containers.get(name)
        if container.status != "exited":
            stop_container(name)
        container.remove(v=True)
        return {"status": "success"}
    except(APIError):
        return {"status": "failed"}


def get_logs(name):
    try:
        logs = client.containers.get(name).logs()
        return {
            "status": "success",
            "logs": logs.decode("utf-8")
        }
    except(APIError):
        return {"status": "failed"}


def get_stats(name):
    try:
        stats = client.containers.get(name).stats(stream=False)
        (r, t) = calculate_network_bytes(stats)
        memory_usage = stats["memory_stats"]["usage"] >> 20
        return {
            "status": "success",
            "stats": {
                "cpu_percent": calculate_cpu_percent(stats),
                "memory_usage": memory_usage,
                "network_usage": {
                    "download": r >> 20,
                    "upload": t >> 20
                }
            }
        }
    except(APIError):
        return {"status": "failed"}


def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return "%.2f" % cpu_percent


def calculate_network_bytes(d):
    """
    :param d:
    :return: (received_bytes, transceived_bytes), ints
    """
    networks = graceful_chain_get(d, "networks")
    if not networks:
        return 0, 0
    r = 0
    t = 0
    for if_name, data in networks.items():
        r += data["rx_bytes"]
        t += data["tx_bytes"]
    return r, t


def graceful_chain_get(d, *args, default=None):
    t = d
    for a in args:
        try:
            t = t[a]
        except (KeyError, ValueError, TypeError, AttributeError):
            return default
    return t
