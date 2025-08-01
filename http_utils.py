from requests import request
from parser import parse_data


def request_handler(method, url, data="", poison=""):
    if method == "get":  # just in case someone passes 'get' with data
        data = None

    if data is not None:
        data = parse_data(data)

        for (key, value) in data.items():
            data[key] = value.replace("FUZZ", poison, 1)

    response = request(method, url, json=data)

    return response
