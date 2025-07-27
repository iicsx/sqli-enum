from printer import usage


# Options
class Options():
    URL = None
    DBMS_TYPE = None
    ERROR_STR = None
    COLUMNS = None
    SUCCESS_STR = None
    METHOD = 'get'


# Coroutine
def parse_args(args):
    opt = Options()

    for i in range(1, len(args), 2):
        descriptor = args[i]
        value = args[i + 1]

        if descriptor == "-u" or descriptor == "--url":
            opt.URL = value
        elif descriptor == "-d" or descriptor == "--dbms":
            opt.DBMS_TYPE = value
        elif descriptor == "-e" or descriptor == "--error":
            opt.ERROR_STR = value
        elif descriptor == "-s" or descriptor == "--success":
            opt.SUCCESS_STR = value
        elif descriptor == "-c" or descriptor == "--columns":
            opt.COLUMNS = value
        elif descriptor == "-m" or descriptor == "--method":
            opt.METHOD = value

        if opt.URL is None or "FUZZ" not in opt.URL:
            usage()
            return exit(1)

    return opt
