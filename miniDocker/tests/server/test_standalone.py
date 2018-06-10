from miniDocker.server.standalone import *


def test_list_containers():
    print(list_containers())


def test_stop_container(name):
    res = stop_container(name)
    if res["status"] == "success":
        print("success")


def test_start_container(name):
    res = start_container(name)
    if res["status"] == "success":
        print("success")


def test_remove_container(name):
    res = remove_container(name)
    if res["status"] == "success":
        print("success")


def test_get_logs(name):
    res = get_logs(name)
    if res["status"] == "success":
        print(res["logs"])


def test_pause(name):
    res = switch_container_pause_status(name)
    if res["status"] == "success":
        print("success")


def test_get_stats(name):
    res = get_stats(name)
    if res["status"] == "success":
        print(res["stats"])


if __name__ == '__main__':
    test_get_stats("eager_mestorf")
