import os
import subprocess

from os import path
from tailscale_localapi import TailscaleAPI, TailscaleException

from tailctx.util.display import info, fatal

CONTEXTS_PATH = path.expanduser("~/.local/state/tailscale")
STATE_PATH = "/var/lib/tailscale"
SOCKET_PATH = "/var/run/tailscale"


def client():
    return TailscaleAPI.v0()


def start(context):
    if os.geteuid() != 0:
        fatal("should be run as root")

    try:
        if client().is_connected():
            fatal("tailscale is already up")
    except TailscaleException:
        pass

    if os.path.isdir(f"{CONTEXTS_PATH}/{context}"):
        info(f"using existing tailscale context `{context}`")
    else:
        info(f"creating new tailscale context `{context}`")

    os.makedirs(f"{CONTEXTS_PATH}/{context}", exist_ok=True)

    set_current_context(context)

    cmd = [
        "/usr/sbin/tailscaled",
        f"--state={CONTEXTS_PATH}/{context}/tailscaled.state",
        f"--statedir={CONTEXTS_PATH}/{context}",
        f"--socket={SOCKET_PATH}/tailscaled.sock",
        "--port=41641",
    ]

    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def stop():
    if os.geteuid() != 0:
        fatal("should be run as root")

    info("stopping tailscale")

    subprocess.Popen(["/usr/bin/pkill", "tailscaled"])


def get_current_context() -> str:
    with open(f"{CONTEXTS_PATH}/current-context", "r") as f:
        return f.read().strip()


def set_current_context(context: str):
    with open(f"{CONTEXTS_PATH}/current-context", "w") as fw:
        fw.write(context)
