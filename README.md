# tailctx - Tailscale context manager

`tailctx` is a tool to help manage several environment for your Tailscale VPNs.

Traditionally, Tailscale only supports connecting to one login server, requiring to delete the state in order to connect to another one, which makes it unpractical when having several separate corporate environments, or a corporate and personal VPNS. `tailctx` runs `tailscaled` with a separate state directory, stored in the user's home directory, in order to persist the distinct states.

Once a context is launched, it can be used and configured as any other Tailscale connection, though the `tailscale` command.

## Install

```shell
# Install from HEAD
$ pip install --force-reinstall git+https://github.com/apognu/tailctx.git
```

## Usage

```shell
$ sudo tailctx start personal
INFO: creating new tailscale context `personal`
$ sudo tailscale up --login-server=...
$ sudo tailctx stop

$ sudo tailctx start personal
INFO: using existing tailscale context `personal`

$ tailctx status
State: connected
Context: personal

Hostname: hostname
DNS name: hostname.ns.example.com
IP address: 100.64.0.100

Hosts:

        Hostname       DNS name      IP address                            Exitable
  ✓     otherhost      100.64.0.3    otherhost.ns.example.com              ✓

$ sudo tailctx exit -s otherhost
INFO: exit node was set as `otherhost`

$ tailctx status
State: connected
Context: personal

Hostname: hostname
DNS name: hostname.ns.example.com
IP address: 100.64.0.100

Hosts:

        Hostname       DNS name      IP address                            Exitable
  ✓ 🌐  otherhost      100.64.0.3    otherhost.ns.example.com              ✓
```
