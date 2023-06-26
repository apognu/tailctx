from tailctx import tailscale


def start(context):
    tailscale.start(context)


def stop():
    tailscale.stop()
