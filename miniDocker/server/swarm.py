from docker import from_env

client = from_env()

def list_nodes():
    nodes = client.nodes.list()