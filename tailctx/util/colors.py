from termcolor import colored


def red(string: str) -> str:
    return colored(string, "red")


def yellow(string: str) -> str:
    return colored(string, "yellow")


def blue(string: str) -> str:
    return colored(string, "blue")


def green(string: str) -> str:
    return colored(string, "green")


def bold(string: str) -> str:
    return colored(string, attrs=["bold"])


def dim(string: str) -> str:
    return colored(string, attrs=["dark"])


def key_value(key: str, value: str) -> str:
    return f"{colored(key, attrs=['bold'])}: {value}"
