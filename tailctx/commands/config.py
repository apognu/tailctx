from tailctx import tailscale
from tailctx.util.display import fatal, info


def exit(node, lan_access: bool = False, unset: bool = False):
    try:
        if unset:
            tailscale.client().unset_exit_node()

            info("exit node was unset")
        else:
            tailscale.client().set_exit_node(node, allow_lan=lan_access)

            info(f"exit node was set as `{node}`")
    except Exception as e:
        fatal(f"an error occured while changing your exit node: ${e}")
