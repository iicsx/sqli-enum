from sys import argv, exit
from requests import ConnectionError
from time import sleep
from handler import handler, Poison
from colored_printer import Color, ColoredPrinter as CP


# Local Modules
from determine import determine_dbms
from parser import parse_args
import printer


if __name__ == "__main__":
    if "--help" in argv or "-h" in argv:
        printer.usage()
        exit(1)

    opts = parse_args(argv)

    printer.banner()

    print(r"[ ] Running version check...")

    brute_force = opts.COLUMNS is None
    if brute_force:
        CP.print(r"[!] Columns missing, using brute force mode", Color.YELLOW)

    tries = 0
    version = None
    while (True):
        try:
            opts.QUERY_TYPE = Poison.ALNUM.name
            version = determine_dbms(opts, Poison.ALNUM.value, int(
                opts.COLUMNS or "0"), brute_force)
            if version is None:
                opts.QUERY_TYPE = Poison.NUMERIC.name
                version = determine_dbms(opts, Poison.NUMERIC.value, int(
                    opts.COLUMNS or "0"), brute_force)

            break
        except ConnectionError:
            sleep(1)
            tries += 1

            if tries >= 5:
                print("\n[x] Could not connect to specified URL")
                exit(1)

    if version is not None:
        print("[*] Got version " + version.name)
        opts.DBMS_TYPE = version

        if brute_force:
            print("[*] Determined column size: ", opts.COLUMNS)

    elif brute_force:
        printer.brute_force_error()
        exit(1)
    else:
        printer.column_error()
        exit(1)

    handler(opts)
