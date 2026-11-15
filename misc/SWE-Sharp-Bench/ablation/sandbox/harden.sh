#!/bin/sh
# Boot-time hardening of the ablation-sandbox WSL distro (run as root by ablation-harden.service).
#  1. Firewall: processes of the `agent` user may only open TCP connections to loopback ports
#     11434 (Ollama), 5050 (Roslyn API) and 5051 (Roslyn MCP wrapper). Everything else (internet,
#     DNS, other Windows/WSL localhost services) is rejected. Replies on connections other users
#     opened to the agent's servers are allowed (ESTABLISHED).
#  2. Windows file systems and WSLg sockets are unmounted / covered in this distro's mount
#     namespace (other distros are unaffected). /mnt/c is already off via wsl.conf automount.
set -eu
AGENT=agent
PORTS=11434,5050,5051

for ipt in iptables ip6tables; do
  $ipt -N ABL_AGENT 2>/dev/null || $ipt -F ABL_AGENT
  $ipt -C OUTPUT -m owner --uid-owner "$AGENT" -j ABL_AGENT 2>/dev/null \
    || $ipt -I OUTPUT 1 -m owner --uid-owner "$AGENT" -j ABL_AGENT
  $ipt -A ABL_AGENT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
done
iptables  -A ABL_AGENT -d 127.0.0.1 -p tcp -m multiport --dports "$PORTS" -j ACCEPT
ip6tables -A ABL_AGENT -d ::1       -p tcp -m multiport --dports "$PORTS" -j ACCEPT
iptables  -A ABL_AGENT -j REJECT
ip6tables -A ABL_AGENT -j REJECT

# Windows interop: wsl.conf turns it off, but WSL's init still leaves a world-writable interop
# socket in /run/WSL (this distro's own /run). The binfmt handler for Windows .exe files (MZ ->
# /init) is KERNEL-WIDE, shared by all WSL distros: do NOT unregister it here, that breaks interop
# (and Docker Desktop's credential helper) in every other distro. /init can only launch a Windows
# process through the interop socket, so making /run/WSL root-only blocks it for the agent.
chmod 700 /run/WSL 2>/dev/null || true
rmdir /mnt/c 2>/dev/null || true          # empty mount point left by the image

# Windows file systems (9p/drvfs/virtiofs), e.g. the read-only DriverStore at /usr/lib/wsl/drivers.
awk '$3 ~ /^(9p|drvfs|virtiofs)$/ {print $2}' /proc/mounts | sort -r | while read -r m; do
  umount -l "$m" || true
done
# WSLg (X11/Wayland/PulseAudio sockets into the Windows desktop, incl. the shared clipboard)
# and /mnt/wsl (a tmpfs shared by all WSL distros). resolv.conf is static (wsl.conf).
for m in /tmp/.X11-unix /mnt/wslg /mnt/wsl; do
  [ -d "$m" ] && mount -t tmpfs -o mode=755,size=1m tmpfs "$m"
done
echo "ablation-harden: firewall for $AGENT ($PORTS on loopback only), Windows mounts removed"
