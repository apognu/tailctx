import sys

from tailscale_localapi import TailscaleException
from requests.exceptions import ConnectionError

from tailctx import tailscale
from tailctx.util.display import create_table
from tailctx.util import colors


def status():
    try:
        if not tailscale.client().is_connected():
            print(colors.key_value("State", colors.red("disconnected")))

            sys.exit(1)
        else:
            status = tailscale.client().self()
            peers = tailscale.client().peers()

            print(colors.key_value("State", colors.green("connected")))
            print(colors.key_value("Context", tailscale.get_current_context()))
            print()
            print(colors.key_value("Hostname", status.hostname))
            print(colors.key_value("DNS name", status.dns_name))
            print(colors.key_value("IP address", status.ip_address))
            print()

            table = create_table(["", colors.dim("Hostname"), colors.dim("DNS name"), colors.dim("IP address"), colors.dim("Exitable")])

            table.add_rows(
                list(
                    map(
                        lambda peer: [
                            f"{'✓' if peer.online else ''} {'🌐' if peer.exit_node else ''}",
                            peer.hostname,
                            peer.ip_address,
                            peer.dns_name,
                            f"{'✓' if peer.can_be_exit_node else ''}",
                        ],
                        peers,
                    )
                )
            )

            print(colors.bold("Hosts:"))
            print()
            print(table)
    except (ConnectionError, TailscaleException):
        print(colors.key_value("State", colors.red("disconnected")))

        sys.exit(1)


def context():
    print(tailscale.get_current_context())
