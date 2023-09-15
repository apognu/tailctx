import sys

from typing import List, Optional
from argparse import ArgumentParser, Namespace

from tailctx import commands
from tailctx.util.display import fatal


def main(args: Optional[List[str]] = None) -> None:
    cli = parse_args(args)

    if cli.command is None:
        fatal("no command provided")

    if cli.command in ["start", "up", "connect"]:
        commands.connect.start(cli.context)
    elif cli.command in ["stop", "down", "disconnect"]:
        commands.connect.stop()
    elif cli.command == "status":
        commands.status.status()
    elif cli.command == "context":
        commands.status.context()
    elif cli.command == "exit":
        commands.config.exit(cli.set, cli.lan, cli.unset)
    else:
        fatal(f"unknown command: `{cli.command}`")


def parse_args(args: Optional[List[str]]) -> Namespace:
    cli = ArgumentParser(prog="tailctx")

    commands = cli.add_subparsers(dest="command", metavar="COMMAND")

    cmd_start = commands.add_parser("start", aliases=["up", "connect"], help="connect to a tailscale context")
    cmd_start.add_argument("context", metavar="CONTEXT")

    commands.add_parser("stop", aliases=["down", "disconnect"], help="disconnect from a tailscale context")
    commands.add_parser("status", help="get connection status")
    commands.add_parser("context", help="print current context")

    cmd_exit = commands.add_parser("exit", help="set exit node")
    cmd_exit.add_argument("-u", "--unset", action="store_true", help="unset the exit node")
    cmd_exit.add_argument("-s", "--set", type=str, metavar="NODE")
    cmd_exit.add_argument("--lan", action="store_true", help="allow LAN access when exit node is used")

    return cli.parse_args(args)
