from printer import usage
from re import search as rx_search
import json


# Options
class Options():
    URL = None
    DBMS_TYPE = None
    ERROR_STR = None
    COLUMNS = None
    SUCCESS_STR = None
    METHOD = 'get'
    DATA = None
    QUERY_TYPE = None
    INCLUDE_SYSTEM_TABLES = False


METHODS = ["get", "post"]


# Coroutine
def parse_args(args):
    opt = Options()

    i = 1
    while i < len(args):
        descriptor = args[i]

        if descriptor in ("-u", "--url"):
            opt.URL = args[i + 1]
            i += 2
        elif descriptor in ("-d", "--dbms"):
            opt.DBMS_TYPE = args[i + 1]
            i += 2
        elif descriptor in ("-e", "--error"):
            opt.ERROR_STR = args[i + 1]
            i += 2
        elif descriptor in ("-s", "--success"):
            opt.SUCCESS_STR = args[i + 1]
            i += 2
        elif descriptor in ("-c", "--columns"):
            opt.COLUMNS = args[i + 1]
            i += 2
        elif descriptor in ("--data"):
            opt.DATA = args[i + 1]
            opt.METHOD = "post"
            i += 2
        elif descriptor in ("-m", "--method"):
            if args[i + 1] not in METHODS:
                print("[x] Unknown method '" + args[i+1] +
                      "'. Valid methods: \n    + " + "\n    + ".join(METHODS))
                exit(1)

            opt.METHOD = args[i + 1]
            i += 2
        elif descriptor == "--include-system-tables":
            opt.INCLUDE_SYSTEM_TABLES = True
            i += 1
        # TODO: add option to output to a file
        else:
            raise ValueError(f"Unknown option: {descriptor}")

    if opt.URL is None or ("FUZZ" not in opt.URL and opt.DATA is None):
        usage()
        return exit(1)

    return opt


def parse_data(data):
    # can be either urlencoded or json
    rx_is_urlencoded = r"^([^=&]+=[^=&]*)(?:&[^=&]+=[^=&]*)*$"
    is_urlencoded = rx_search(rx_is_urlencoded, data)
    is_json = is_valid_json(data)

    if is_urlencoded:
        return parse_urlencoded(data)
    elif is_json:
        return json.loads(data)


def parse_urlencoded(data=""):
    parts = data.split("&")

    json_data = {}
    for part in parts:
        [key, value] = part.split("=")

        json_data[key] = value

    return json_data


def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False
