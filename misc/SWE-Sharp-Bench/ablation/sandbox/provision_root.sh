#!/bin/bash
# Provision the ablation-sandbox WSL distro (run as root inside it; see SETUP_NOTES.md "Sandbox").
#   provision_root.sh          packages, users, directories (while /mnt/c is still mounted for copying)
#   provision_root.sh --lock   install wsl.conf (no /mnt/c, no Windows interop) + the boot hardening
#                              service; then `wsl --terminate ablation-sandbox` from Windows
# Users: runner (uid 1000, setup + restore + the runner itself, passwordless sudo) and
#        agent  (uid 1001, no sudo; OpenHands, its terminal and the Roslyn servers run as agent).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "--lock" ]; then
  # The sandbox probe runs a real Windows program as the agent and expects it NOT to run. Copy one in
  # first (from Windows: `wsl -d ablation-sandbox -u root -e sh -c 'mkdir -p /opt/ablation-probe;
  # cat > /opt/ablation-probe/whoami.exe' < C:\Windows\System32\whoami.exe`, in cmd.exe).
  chmod 755 /opt/ablation-probe/whoami.exe
  install -m 755 "$HERE/harden.sh" /usr/local/sbin/ablation-harden.sh
  install -m 644 "$HERE/ablation-harden.service" /etc/systemd/system/ablation-harden.service
  install -m 644 "$HERE/ablation-interop-guard.service" /etc/systemd/system/ablation-interop-guard.service
  systemctl enable ablation-harden.service ablation-interop-guard.service
  # binfmt_misc is kernel-wide (shared by all WSL distros). systemd-binfmt.service unregisters ALL
  # handlers when this distro shuts down (ExecStop=--unregister), which removes Windows interop
  # (WSLInterop) from the user's other distros and Docker Desktop. Not needed here: mask it.
  systemctl mask systemd-binfmt.service
  # Static resolver (the generated one is a symlink into /mnt/wsl, which harden.sh covers).
  ns=$(awk '/^nameserver/ {print $2; exit}' /etc/resolv.conf)
  rm -f /etc/resolv.conf
  printf 'nameserver %s\n' "${ns:-10.255.255.254}" > /etc/resolv.conf
  install -m 644 "$HERE/wsl.conf" /etc/wsl.conf
  echo "locked; run 'wsl --terminate ablation-sandbox' on Windows for wsl.conf to take effect"
  exit 0
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q git tmux curl ca-certificates sudo iptables acl python3 python3-psutil libicu78 procps less

id runner >/dev/null 2>&1 || useradd -m -u 1000 -s /bin/bash runner
id agent  >/dev/null 2>&1 || useradd -m -u 1001 -s /bin/bash agent
chmod 750 /home/runner /home/agent          # agent can't read the runner's cache/sample/run records
cat > /etc/sudoers.d/ablation <<'EOF'
runner ALL=(ALL:ALL) NOPASSWD: ALL
Defaults:runner !use_pty
EOF
chmod 440 /etc/sudoers.d/ablation
visudo -cf /etc/sudoers.d/ablation

# Shared, agent-readable software (owned by runner, read-only for agent):
#   /opt/dotnet-sdks/<ver>  one isolated .NET root per harness SDK version (agent builds)
#   /opt/dotnet             the Roslyn API's own .NET install
#   /opt/openhands          uv tool env with openhands==1.16.0 (+ its Python)
#   /opt/roslyn/{api,mcp}   Roslyn API + MCP wrapper binaries
#   /srv/nuget              NuGet global packages folder (restored by runner)
# Agent-writable during a run: /srv/ablation/work/<repo> and /srv/ablation/agent (per-run scratch).
mkdir -p /opt/dotnet-sdks /opt/dotnet /opt/openhands /opt/roslyn /srv/nuget \
         /srv/ablation/work /srv/ablation/agent /srv/ablation/bin
chown runner:runner /opt/dotnet-sdks /opt/dotnet /opt/openhands /opt/roslyn /srv/nuget \
         /srv/ablation /srv/ablation/work /srv/ablation/agent /srv/ablation/bin
chmod 755 /opt/dotnet-sdks /opt/dotnet /opt/openhands /opt/roslyn /srv/nuget /srv/ablation \
         /srv/ablation/work /srv/ablation/agent /srv/ablation/bin
# Legacy DotNetCliToolReference restores (Ocelot) write lock/tmp files under the packages folder's
# .tools; only that subfolder is agent-writable.
mkdir -p /srv/nuget/.tools && chown runner:runner /srv/nuget/.tools
setfacl -R -m u:agent:rwX -m d:u:agent:rwX /srv/nuget/.tools
printf '[boot]\nsystemd=true\n\n[user]\ndefault=runner\n' > /etc/wsl.conf
echo "provisioned"
