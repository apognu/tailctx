import json
import os
import requests
import subprocess

from os import path

from tailctx.util.display import info, fatal
from tailctx.util.sock import SnapdAdapter

CONTEXTS_PATH = path.expanduser("~/.local/state/tailscale")
STATE_PATH = "/var/lib/tailscale"
SOCKET_PATH = "/var/run/tailscale"


session = requests.Session()
session.mount("http://ts/", SnapdAdapter())


class Status:
    def __init__(self, payload):
        self.state = payload["BackendState"] == "Running"
        self.hostname = None
        self.ip_address = None
        self.dns_name = None
        self.hosts = {}

        if self.state:
            self.hostname = payload["Self"]["HostName"]
            self.ip_address = payload["TailscaleIPs"][0]
            self.dns_name = payload["Self"]["DNSName"]
            self.hosts = payload["Peer"]

    @classmethod
    def offline(cls):
        return Status({"BackendState": "offline"})


def prefs():
    try:
        response = session.get("http://ts/localapi/v0/prefs")

        if response.status_code != 200:
            return None
        else:
            return response.json()
    except:
        return None


def set_prefs(prefs):
    response = session.patch("http://ts/localapi/v0/prefs", data=json.dumps(prefs))

    if response.status_code == 200:
        return True
    else:
        return False


def status():
    try:
        response = session.get("http://ts/localapi/v0/status")

        if response.status_code != 200:
            status = Status.offline()
        else:
            status = Status(response.json())
    except:
        status = Status.offline()

    return status


def start(context):
    if status().state:
        fatal("tailscale is already up")

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
    if not status().state:
        fatal("tailscale is not running")

    info("stopping tailscale")

    subprocess.Popen(["/usr/bin/pkill", "tailscaled"])


def get_current_context() -> str:
    with open(f"{CONTEXTS_PATH}/current-context", "r") as f:
        return f.read().strip()


def set_current_context(context: str):
    with open(f"{CONTEXTS_PATH}/current-context", "w") as fw:
        fw.write(context)
