import sys

from prettytable import PrettyTable
from typing import List

from .colors import *


def exit(message: str) -> None:
    print(message.strip(), file=sys.stderr)
    sys.exit(0)


def fatal(message: str) -> None:
    print(f"{red('ERROR:')} {message.strip()}", file=sys.stderr)
    sys.exit(1)


def info(message: str) -> None:
    print(f"{blue('INFO:')} {message.strip()}")


def create_table(headers: List[str]) -> PrettyTable:
    table = PrettyTable()
    table.field_names = headers
    table.align = "l"
    table.padding_width = 2
    table.border = False

    return table
