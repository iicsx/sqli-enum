from printer import usage


# Options
class Options():
    URL = None
    DBMS_TYPE = None
    ERROR_STR = None
    COLUMNS = None
    SUCCESS_STR = None
    METHOD = 'get'
    QUERY_TYPE = None
    INCLUDE_SYSTEM_TABLES = False


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
        elif descriptor in ("-m", "--method"):
            opt.METHOD = args[i + 1]
            i += 2
        elif descriptor == "--include-system-tables":
            opt.INCLUDE_SYSTEM_TABLES = True
            i += 1
        # TODO: add option to output to a file
        else:
            raise ValueError(f"Unknown option: {descriptor}")

        if opt.URL is None or "FUZZ" not in opt.URL:
            usage()
            return exit(1)

    return opt
