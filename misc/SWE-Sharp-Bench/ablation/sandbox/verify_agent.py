"""Adversarial check of the sandbox, as the agent would try it (run as runner in ablation-sandbox):
prepares one real workspace, hands it to the agent user and tries, as agent, to reach Windows, the
internet, the runner's files and the upstream history. Prints one line per attempt; exit 1 if any got through.

    python3 sandbox/verify_agent.py [instance_id]
"""
import json
import subprocess
import sys
from pathlib import Path

sys.argv, inst = sys.argv[:1], (sys.argv[1] if len(sys.argv) > 1 else "serilog__serilog-1906")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_tasks as rt  # noqa: E402

task = next(t for t in json.loads(rt.DEFAULTS["sample"].read_text()) if t["instance_id"] == inst)
rt.reset_agent_state("agent")
ws = rt.prepare_workspace(task, rt.DEFAULTS["cache"], rt.DEFAULTS["work"])
rt.sudo("chown", "-R", "agent:agent", ws)
gold_file = next(l[6:] for l in task["patch"].splitlines() if l.startswith("+++ b/"))

# (description, shell command run as agent, it passes if the command FAILS / prints nothing)
ATTEMPTS = [
    ("list Windows drive", "ls /mnt/c/Users"),
    ("mount the Windows drive", "mkdir -p /tmp/c && mount -t drvfs 'C:' /tmp/c && ls /tmp/c"),
    ("run a real Windows exe (whoami.exe)", "o=$(timeout 15 /opt/ablation-probe/whoami.exe | tr -d '\\r'); echo \"$o\"; [ -n \"$o\" ]"),
    ("run a Windows exe copied to /tmp", "cp /opt/ablation-probe/whoami.exe /tmp/w.exe && o=$(timeout 15 /tmp/w.exe | tr -d '\\r'); [ -n \"$o\" ]"),
    ("open the interop socket", "python3 -c \"import socket,glob;s=socket.socket(socket.AF_UNIX);s.connect((glob.glob('/run/WSL/*interop')+['/run/WSL/1_interop'])[0])\""),
    ("WSLg / X11 sockets", "find /mnt/wslg /tmp/.X11-unix -type s | grep ."),
    ("HTTPS to github.com", "curl -sS --max-time 8 -o /dev/null https://github.com"),
    ("HTTPS by IP (1.1.1.1)", "curl -sS --max-time 8 -k -o /dev/null https://1.1.1.1"),
    ("UDP DNS to 8.8.8.8", "python3 -c \"import socket;s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.settimeout(4);s.sendto(b'\\x12\\x34\\x01\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x06github\\x03com\\x00\\x00\\x01\\x00\\x01',('8.8.8.8',53));print(s.recv(512))\""),
    ("system resolver", "timeout 5 getent hosts github.com"),
    ("git fetch the upstream repo", f"timeout 20 git -C {ws} fetch https://github.com/{task['repo']}.git"),
    ("other localhost port (Windows RPC 135)", "curl -sS --max-time 5 -o /dev/null http://127.0.0.1:135"),
    ("read runner's home", "ls /home/runner"),
    ("read the full-history repo cache", f"ls /home/runner/swe-repos/{task['repo'].replace('/', '__')}"),
    ("read sample.json (gold patches)", "cat /home/runner/src/prose/misc/SWE-Sharp-Bench/harness/data/tasks/sample.json > /dev/null"),
    ("sudo", "sudo -n true"),
    ("commits after base in workspace", f"cd {ws} && n=$(git rev-list --all --reflog --count ^HEAD) && [ $n -gt 0 ]"),
    ("remote-tracking refs / remotes", f"cd {ws} && git for-each-ref refs/remotes refs/heads | grep . || git remote | grep ."),
    ("unreachable objects (old fix commits)", f"cd {ws} && git fsck --unreachable --no-reflogs --connectivity-only --no-progress | grep ."),
    ("later commits touching the gold file", f"cd {ws} && git log --all --oneline ^HEAD -- {gold_file} | grep ."),
]
leaks = 0
for desc, cmd in ATTEMPTS:
    p = subprocess.run(rt.as_user("agent", ["bash", "-c", cmd], rt.agent_env()), cwd=ws,
                       capture_output=True, text=True, errors="replace", timeout=120)
    ok = p.returncode != 0
    leaks += not ok
    detail = (p.stderr or p.stdout).strip().splitlines()
    print(f"{'blocked' if ok else 'LEAK   '}  {desc:40} {(detail[-1] if detail else '')[:110]}")
# Positive control: Ollama must still work for the agent.
p = subprocess.run(rt.as_user("agent", ["curl", "-sS", "--max-time", "8", "http://localhost:11434/api/version"],
                              rt.agent_env()), cwd=ws, capture_output=True, text=True)
print(f"{'works  ' if p.returncode == 0 else 'BROKEN '}  {'Ollama localhost:11434 (must work)':40} {p.stdout.strip()[:80]}")
rt.kill_user("agent")
rt.sudo("rm", "-rf", ws)
print(f"{leaks} leak(s)")
sys.exit(1 if leaks or p.returncode else 0)
