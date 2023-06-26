from tailctx import tailscale
from tailctx.util.display import create_table
from tailctx.util import colors


def status():
    status = tailscale.status()

    if not status.state:
        print(colors.key_value("State", colors.red("disconnected")))
    else:
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
                    lambda host: [
                        f"{'✓' if host['Online'] else ''} {'🌐' if host['ExitNode'] else ''}",
                        host["HostName"],
                        host["TailscaleIPs"][0],
                        host["DNSName"],
                        f"{'✓' if host['ExitNodeOption'] else ''}",
                    ],
                    status.hosts.values(),
                )
            )
        )

        print(colors.bold("Hosts:"))
        print()
        print(table)
