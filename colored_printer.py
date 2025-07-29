from enum import Enum


class Color(Enum):
    YELLOW = '\x1b[33m'
    GREEN = '\x1b[32m'
    RED = '\x1b[31m'
    BLUE = '\x1b[34m'
    BLACK = '\x1b[30m'
    RESET = '\x1b[0m'


class ColoredPrinter():
    @staticmethod
    def print(message, color=Color.RESET):
        print(color.value + message + Color.RESET.value)
