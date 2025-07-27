from sys import argv, exit
from requests import ConnectionError
from time import sleep

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

    tries = 0
    while (True):
        try:
            version = determine_dbms(
                opts.URL, opts.SUCCESS_STR, opts.ERROR_STR, int(opts.COLUMNS or "0"), brute_force)
            break
        except ConnectionError:
            sleep(1)
            tries += 1

            if tries >= 5:
                print("\n[x] Could not connect to specified URL")
                exit(1)

    if version is not None:
        print("\n[*] Got version " + version.name)
    else:
        column_error()
        exit(1)
