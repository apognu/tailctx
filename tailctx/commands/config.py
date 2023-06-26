from tailctx import tailscale
from tailctx.util.display import fatal, info


def exit(node, unset: bool = False):
    status = tailscale.status()
    exit_node_id = None

    if unset:
        exit_node_id = ""
    else:
        for (_, host) in status.hosts.items():
            if host["HostName"] == node:
                if not host["ExitNodeOption"]:
                    fatal("this node cannot be used as an exit node")

                exit_node_id = host["ID"]

    if exit_node_id is not None:
        if tailscale.set_prefs({"ExitNodeIDSet": True, "ExitNodeID": exit_node_id}):
            if unset:
                info("exit node was unset")
            else:
                info(f"exit node was set as `{node}`")
        else:
            fatal("an error occured while changing your exit node")
