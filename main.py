from sys import argv, exit

# Local Modules
from determine import determine_dbms
from parser import parse_args
from printer import banner, column_error, usage


if __name__ == "__main__":
    if "--help" in argv or "-h" in argv:
        usage()
        exit(1)

    banner()

    print(r"[ ] Processing input...")
    opts = parse_args(argv)
    print(r"[ ] Running version check...")

    brute_force = opts.COLUMNS is None
    if brute_force:
        print(r"[!] Columns missing, using brute force mode")

    version = determine_dbms(
        opts.URL, opts.SUCCESS_STR, opts.ERROR_STR, int(opts.COLUMNS or "0"), brute_force)

    if version is not None:
        print(r"[*] Got version " + version.name)
    else:
        column_error()
        exit(1)
