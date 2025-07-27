from sys import argv

# Local Modules
from determine import determine_dbms
from parser import parse_args
from printer import banner


if __name__ == "__main__":
    banner()

    print(r"[ ] Processing input...")
    opts = parse_args(argv)
    if opts.COLUMNS is not None:
        print(r"[ ] Running version check...")

        version = determine_dbms(opts.URL, opts.SUCCESS_STR, opts.ERROR_STR)

        print(r"[*] Got version " + version.name)
    else:
        print(r"[ ] Attempting to determine column size...")
