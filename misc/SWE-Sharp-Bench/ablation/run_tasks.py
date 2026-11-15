"""Per-task runner for the IS755 Roslyn ablation (OpenHands text-only vs. text + Roslyn MCP).

For each (condition, instance), identically in both conditions unless noted:
  1. fresh checkout of the task repo at base_commit (+ submodules) in WORK/<owner>__<name>, cloned
     from a per-instance repo holding ONLY the history up to base_commit + the tags merged into it
     (version tools need history; nothing later may exist: the upstream fix). No remote, checked.
     In the sandbox distro the agent phase runs as the `agent` user (see SETUP_NOTES.md "Sandbox")
  2. per-repo setup steps (Avalonia: build Avalonia.Desktop.slnf), then `dotnet restore` of the solution
  3. roslyn only: frozen agent/AGENTS.md copied to the repo root (git-excluded), Roslyn API (:5050)
     loads the solution, MCP wrapper (:5051) started; both health-checked
  4. agent: oh_driver.py with OPENHANDS_PERSISTENCE_DIR=<openhands>/<condition>, explicit step limit
     and wall-clock timeout  (skipped with --dry-run; the driver builds the agent and checks MCP instead)
  5. patch = `git diff` of everything the agent changed vs base_commit (AGENTS.md excluded), written to
     predictions.jsonl in SWE-Sharp-Bench harness format
  6. optional compile check: `dotnet build` of the solution, error count compared with the baseline
  7. servers stopped, workspace deleted (--keep-workspace to keep it)

Outputs: RUNS/<run_id>/<condition>/<instance_id>/{task.md, run.json, events.jsonl, patch.diff, ...}
         RUNS/<run_id>/<condition>/predictions.jsonl, RUNS/<run_id>/summary.md

    python run_tasks.py --run-id dry1 --dry-run --conditions text roslyn --instances serilog__serilog-1906
    python run_tasks.py --run-id main --conditions text roslyn            # all 36 sample tasks
"""
import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HOME = Path.home()
ABLATION = HOME / "ablation"
HERE = Path(__file__).resolve().parent
# Sandbox distro layout (sandbox/provision_root.sh): the runner user owns the repo cache, the sample
# (gold patches!) and the run records under /home/runner (mode 750); the agent user can only read
# /opt (SDKs, OpenHands, Roslyn binaries) and /srv/nuget, and write /srv/ablation/{work,agent}.
SANDBOX = Path("/srv/ablation/agent").is_dir() and Path("/opt/roslyn").is_dir()
if SANDBOX:
    ROSLYN_REPO = HOME / "src" / "RoslynAnalyzerApi"         # AGENTS.md + loadcheck helpers + commit
    ROSLYN_API_DIR, ROSLYN_MCP_DIR = Path("/opt/roslyn/api"), Path("/opt/roslyn/mcp")
    API_DOTNET, SDK_ROOTS = Path("/opt/dotnet"), Path("/opt/dotnet-sdks")
    NUGET_PACKAGES = "/srv/nuget/"   # trailing slash: becomes a SourceRoot, which must end with '/'
    WORK, AGENT_SCRATCH, AGENT_BIN = Path("/srv/ablation/work"), Path("/srv/ablation/agent"), Path("/srv/ablation/bin")
    OH_PYTHON = Path("/opt/openhands/tools/openhands/bin/python")
else:
    ROSLYN_REPO = Path("/mnt/c/Repos/RoslynAnalyzerApi")      # AGENTS.md + loadcheck helpers (source of truth)
    _build = HOME / "build" / "RoslynAnalyzerApi"              # WSL build of the API + MCP wrapper
    ROSLYN_API_DIR, ROSLYN_MCP_DIR = _build / "bin/Debug/net8.0", _build / "mcp/RoslynAnalyzerMcp/bin/Debug/net8.0"
    API_DOTNET, SDK_ROOTS = HOME / ".dotnet", HOME / ".dotnet-sdks"
    NUGET_PACKAGES = None
    WORK, AGENT_SCRATCH, AGENT_BIN = ABLATION / "work", None, None
    OH_PYTHON = HOME / ".local/share/uv/tools/openhands/bin/python"
ROSLYN_COMMIT_REPO = ROSLYN_REPO if SANDBOX else HOME / "build" / "RoslynAnalyzerApi"
# This folder lives at misc/SWE-Sharp-Bench/ablation in the prose fork, next to the harness.
HARNESS = HERE.parent / "harness" if (HERE.parent / "harness").is_dir() else Path("/mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness")
DEFAULTS = dict(
    sample=HARNESS / "data/tasks/sample.json",
    cache=HOME / "swe-repos",
    work=WORK,
    runs=ABLATION / "runs",
    openhands=ABLATION / "openhands",
    oh_python=OH_PYTHON,
    agents_md=ROSLYN_REPO / "agent" / "AGENTS.md",
)
API_PORT, MCP_PORT = 5050, 5051
CONDITIONS = ("text", "roslyn")
MODEL_NAME = "openhands-1.16.0__qwen3.5-9b"   # replaced in main() from the agent settings' model


def settings_model(openhands_dir):
    """The LLM model both conditions' agent_settings.json use (must be the same)."""
    models = {c: json.loads((openhands_dir / c / "agent_settings.json").read_text())["llm"]["model"] for c in CONDITIONS}
    if len(set(models.values())) != 1:
        raise SystemExit(f"conditions use different models: {models}")
    return models["text"]
THIRD_PARTY_AGENT_FILES = {".cursorrules", "agents.md", "agent.md", "claude.md", "gemini.md"}  # loaded by OpenHands


def load_loadcheck():
    """Reuse loadcheck.py's repo-setup table and solution helpers (one definition for both scripts)."""
    spec = importlib.util.spec_from_file_location("loadcheck", ROSLYN_REPO / "loadcheck" / "loadcheck.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lc = load_loadcheck()


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


HARNESS_SDK = json.loads((HERE / "harness_sdk.json").read_text())  # from harness_sdk.py (harness's own table)
DOTNET_VARS = dict(DOTNET_MULTILEVEL_LOOKUP="0", DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1",
                   DOTNET_SKIP_FIRST_TIME_EXPERIENCE="1")


def dotnet_root(sdk=None):
    root = API_DOTNET if sdk is None else SDK_ROOTS / sdk
    if not (root / "dotnet").exists():
        raise RuntimeError(f"no .NET root {root} (run install_sdks.sh)")
    return root


def dotnet_env(sdk=None):
    """Environment with exactly one dotnet on PATH. sdk=None: the API's own install (SDK 8).
    sdk='8.0.404': the isolated root with only the SDK the harness image uses for the task."""
    root = dotnet_root(sdk)
    env = dict(os.environ)
    path = [p for p in env.get("PATH", "").split(":") if p and ".dotnet" not in p and "/opt/dotnet" not in p]
    env.update(DOTNET_ROOT=str(root), **DOTNET_VARS, PATH=":".join([str(root), str(root / "tools"), *path]))
    if NUGET_PACKAGES:
        env["NUGET_PACKAGES"] = NUGET_PACKAGES
        # NuGet's lock dir /tmp/NuGetScratch (and /tmp/.dotnet) would belong to whichever user creates
        # it first; the runner uses its own temp dir so the agent's restores can take their locks
        # (old SDKs such as 6.0.100 ignore NUGET_SCRATCH, so TMPDIR too).
        tmp = Path(f"/tmp/runner-{os.getuid()}")
        tmp.mkdir(mode=0o700, exist_ok=True)
        env.update(TMPDIR=str(tmp), NUGET_SCRATCH=str(tmp / "NuGetScratch"))
    return env


# ---- agent user (sandbox) -----------------------------------------------------------------------
# With --agent-user, everything the agent can drive (OpenHands driver, its terminal, the Roslyn
# servers it queries) runs as that user via sudo, with an explicit environment (env -i) and the
# workspace chown'ed to it for the agent phase only. Setup, restore, builds and patch extraction
# stay with the runner user.

def agent_env(sdk=None, **extra):
    root = dotnet_root(sdk)
    env = dict(HOME="/home/agent", USER="agent", LOGNAME="agent", SHELL="/bin/bash", LANG="C.UTF-8",
               PATH=":".join([str(root), str(root / "tools"),
                              "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"]),
               DOTNET_ROOT=str(root), **DOTNET_VARS)
    if NUGET_PACKAGES:
        env["NUGET_PACKAGES"] = NUGET_PACKAGES
    env.update(extra)
    return env


def as_user(user, cmd, env):
    """Command line that runs cmd as user with exactly env (sudo resets the rest)."""
    return ["sudo", "-n", "-u", user, "--", "/usr/bin/env", "-i", *[f"{k}={v}" for k, v in env.items()], *map(str, cmd)]


def sudo(*cmd, check=True):
    return run(["sudo", "-n", *map(str, cmd)], "/", env=dict(os.environ), check=check)


def kill_user(user, timeout=30):
    """SIGKILL every process of user (driver, terminals/tmux, Roslyn servers); wait until gone."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        sudo("pkill", "-KILL", "-u", user, check=False)
        if run(["pgrep", "-u", user], "/", env=dict(os.environ), check=False).returncode != 0:
            return
        time.sleep(0.5)
    raise RuntimeError(f"processes of {user} survive SIGKILL")


def reset_agent_state(user):
    """Every agent run starts from the same state: no processes, empty scratch, fresh home, no tmp files."""
    kill_user(user)
    # This distro's WSL interop socket dir must be root-only (the guard service keeps it so; re-applied
    # here). Never touch the binfmt handler: it is kernel-wide, shared with every other WSL distro.
    sudo("sh", "-c", "chmod 700 /run/WSL 2>/dev/null; true")
    home = Path("/home") / user
    sudo("find", AGENT_SCRATCH, "-mindepth", "1", "-delete")
    sudo("find", home, "-mindepth", "1", "-delete")
    sudo("cp", "-a", "/etc/skel/.", f"{home}/")
    sudo("chown", "-R", f"{user}:{user}", home)
    sudo("find", "/tmp", "/var/tmp", "/dev/shm", "-mindepth", "1", "-user", user, "-delete", check=False)


SANDBOX_PROBE = r"""
p() { printf '%s=%s\n' "$1" "$2"; }
curl -s -o /dev/null --max-time 8 https://github.com && p internet_https reachable || p internet_https blocked
curl -s -o /dev/null --max-time 8 -k https://1.1.1.1 && p internet_ip reachable || p internet_ip blocked
timeout 5 getent hosts github.com >/dev/null && p dns reachable || p dns blocked
curl -s -o /dev/null --max-time 8 http://127.0.0.1:11434/api/version && p ollama reachable || p ollama blocked
[ -e /mnt/c ] && p mnt_c present || p mnt_c absent
awk '$3 ~ /^(9p|drvfs|virtiofs)$/' /proc/mounts | grep -q . && p windows_mounts present || p windows_mounts none
ls /run/WSL/*interop* >/dev/null 2>&1 && p interop_socket present || p interop_socket none
# Functional test: a real Windows program (whoami.exe, copied in at setup). Blocked = no output.
o=$(timeout 15 /opt/ablation-probe/whoami.exe 2>/dev/null | tr -d '\r'); [ -n "$o" ] && p windows_exe ran || p windows_exe blocked
find /mnt/wslg /tmp/.X11-unix -type s 2>/dev/null | grep -q . && p wslg_sockets present || p wslg_sockets none
ls /home/runner >/dev/null 2>&1 && p runner_home readable || p runner_home denied
sudo -n true 2>/dev/null && p sudo allowed || p sudo denied
"""
SANDBOX_EXPECT = dict(internet_https="blocked", internet_ip="blocked", dns="blocked", ollama="reachable",
                      mnt_c="absent", windows_mounts="none", interop_socket="none", windows_exe="blocked",
                      wslg_sockets="none", runner_home="denied", sudo="denied")


def sandbox_probe(user, cwd):
    """What the agent user can reach, probed as that user right before the agent starts."""
    proc = run(as_user(user, ["bash", "-c", SANDBOX_PROBE], agent_env()), cwd, timeout=120,
               env=dict(os.environ), check=False)
    got = dict(l.split("=", 1) for l in proc.stdout.splitlines() if "=" in l)
    bad = {k: got.get(k) for k, v in SANDBOX_EXPECT.items() if got.get(k) != v}
    return got, bad


def task_sdk(task):
    sdk = (HARNESS_SDK.get(task["instance_id"]) or {}).get("sdk")
    if not sdk:
        raise RuntimeError(f"no harness SDK version for {task['instance_id']} in harness_sdk.json")
    return sdk


def run(cmd, cwd, timeout=3600, env=None, check=True):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env or dotnet_env())
    if check and proc.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, cmd))} failed ({proc.returncode}): {(proc.stdout + proc.stderr)[-1500:]}")
    return proc


def git(args, cwd, **kw):
    return run(["git", "-c", "core.longpaths=true", *args], cwd, **kw).stdout


# ---- workspace --------------------------------------------------------------------------------

def cache_repo(task, cache_dir):
    owner, name = task["repo"].split("/")
    repo = cache_dir / f"{owner}__{name}"
    if not (repo / ".git").is_dir():
        log(f"  caching full clone of {task['repo']}")
        cache_dir.mkdir(parents=True, exist_ok=True)
        git(["clone", "-q", f"https://github.com/{task['repo']}.git", str(repo)], cache_dir)
    try:
        git(["cat-file", "-e", f"{task['base_commit']}^{{commit}}"], repo)
    except RuntimeError:
        git(["fetch", "-q", "origin", task["base_commit"]], repo)
    return repo


def base_repo(task, cache_dir):
    """Bare repo with only the history up to base_commit, plus the tags that point into it (version
    tools such as Nerdbank.GitVersioning / MinVer read history and tags). Nothing after base_commit
    exists in it, so the agent can't find the upstream fix in git (branches, later tags, reflogs,
    unreachable objects). Built once per instance from the full-clone cache."""
    full = cache_repo(task, cache_dir)
    base = task["base_commit"]
    bare = cache_dir / "_base" / f"{task['instance_id']}.git"
    marker = bare / "ablation-base"
    if marker.exists() and marker.read_text().strip() == base:
        return bare
    if bare.exists():
        shutil.rmtree(bare)
    bare.parent.mkdir(parents=True, exist_ok=True)
    log(f"  building history-trimmed repo (up to {base[:10]})")
    git(["init", "-q", "--bare", str(bare)], bare.parent)
    upload = "git -c uploadpack.allowAnySHA1InWant=true upload-pack"
    git(["fetch", "-q", "--no-tags", f"--upload-pack={upload}", str(full), f"+{base}:refs/heads/base"], bare)
    tags = git(["tag", "--merged", base], full).split()
    if tags:
        proc = subprocess.run(["git", "fetch", "-q", "--no-tags", "--stdin", str(full)], cwd=bare, text=True,
                              input="".join(f"+refs/tags/{t}:refs/tags/{t}\n" for t in tags), capture_output=True)
        if proc.returncode != 0:
            raise RuntimeError(f"fetching {len(tags)} tags failed: {proc.stderr[-800:]}")
    git(["symbolic-ref", "HEAD", "refs/heads/base"], bare)
    marker.write_text(base + "\n")
    return bare


def trim_submodule_history(ws):
    """Submodules are cloned from GitHub at their pinned commits; drop their remotes, branches,
    later tags and everything unreachable from the pinned commit."""
    script = ("git remote | xargs -r -n1 git remote remove; "
              "git for-each-ref --format='%(refname)' refs/heads refs/remotes | xargs -r -n1 git update-ref -d; "
              "git tag --no-merged HEAD | xargs -r git tag -d >/dev/null; "
              "git reflog expire --expire=now --all; git gc -q --prune=now")
    git(["submodule", "foreach", "-q", "--recursive", script], ws)


def prepare_workspace(task, cache_dir, work_dir):
    bare = base_repo(task, cache_dir)
    owner, name = task["repo"].split("/")
    ws = work_dir / f"{owner}__{name}"
    if ws.exists():  # left over from an interrupted run; may still be owned by the agent user
        if SANDBOX:
            sudo("rm", "-rf", ws)
        else:
            shutil.rmtree(ws)
    work_dir.mkdir(parents=True, exist_ok=True)
    git(["clone", "-q", "--no-checkout", "--no-hardlinks", str(bare), str(ws)], work_dir)
    # Relative submodule URLs resolve against origin; the remote is removed after submodule init.
    git(["remote", "set-url", "origin", f"https://github.com/{task['repo']}.git"], ws)
    if not git(["config", "--get-regexp", r"^extensions\."], ws, check=False).strip():
        git(["config", "core.repositoryformatversion", "0"], ws)  # old libgit2 (SourceLink) rejects 1
    git(["checkout", "-q", "-f", "--detach", task["base_commit"]], ws)
    git(["branch", "-q", "-D", "base"], ws)
    git(["clean", "-q", "-ffdx"], ws)
    if (ws / ".gitmodules").exists():
        git(["submodule", "update", "-q", "--init", "--recursive", "--force"], ws)
    git(["remote", "remove", "origin"], ws)
    if (ws / ".gitmodules").exists():
        trim_submodule_history(ws)
    return ws


def history_check(ws, base):
    """Proof that the workspace has no history after base_commit (main repo and submodules)."""
    def one(repo, head):
        refs = git(["for-each-ref", "--format=%(refname)"], repo).split()
        return {"remotes": len(git(["remote"], repo).split()),
                "nonTagRefs": [r for r in refs if not r.startswith("refs/tags/")][:5],
                "tags": sum(r.startswith("refs/tags/") for r in refs),
                "laterCommits": int(git(["rev-list", "--count", "--all", "--reflog", f"^{head}"], repo).strip()),
                "unreachableObjects": len(git(["fsck", "--unreachable", "--no-reflogs", "--connectivity-only",
                                               "--no-progress"], repo, timeout=1800).splitlines())}
    out = {"repo": one(ws, base), "submodules": {}}
    if (ws / ".gitmodules").exists():
        for line in git(["submodule", "status", "--recursive"], ws).splitlines():
            sha, path = line[1:].split()[:2]
            out["submodules"][path] = one(ws / path, sha)
    return out


def history_problems(h):
    probs = []
    for where, r in [(".", h["repo"]), *h["submodules"].items()]:
        if r["remotes"] or r["nonTagRefs"] or r["laterCommits"] or r["unreachableObjects"]:
            probs.append(f"git history in {where}: {r}")
    return probs


def git_exclude(ws, name):
    exclude = ws / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with open(exclude, "a", encoding="utf8") as f:
        f.write(f"\n/{name}\n")


def sanitize_slnf(ws, slnf_name):
    """A solution filter can list projects its solution no longer (or not yet) has at an older
    commit (Avalonia 14013: MSB5028). Write a git-excluded copy without them and use that."""
    slnf = ws / slnf_name
    data = json.loads(slnf.read_text(encoding="utf-8-sig"))
    sln = (slnf.parent / data["solution"]["path"].replace("\\", "/")).resolve()
    in_sln = {os.path.normcase(p) for p in lc.solution_projects(str(sln))}
    keep, dropped = [], []
    for p in data["solution"]["projects"]:
        full = os.path.normcase(os.path.normpath(str(sln.parent / p.replace("\\", "/"))))
        (keep if full in in_sln else dropped).append(p)
    if not dropped:
        return slnf_name, []
    data["solution"]["projects"] = keep
    fixed = slnf_name.replace(".slnf", ".ablation.slnf")
    (ws / fixed).write_text(json.dumps(data, indent=2), encoding="utf8")
    git_exclude(ws, fixed)
    return fixed, dropped


def pick_solution(ws, task, policy):
    """no-gold (default): rank solutions by name match + size only, so the gold patch never
    influences setup. gold: loadcheck's ranking, which prefers the solution owning the fixed files."""
    setup = lc.REPO_SETUP.get(task["repo"], {})
    if "solution" in setup:
        return ws / setup["solution"], "repo-setup"
    targets = lc.changed_source_files(task["patch"]) if policy == "gold" else []
    sln, _ = lc.find_solution(str(ws), task["repo"], targets)
    if sln is None:
        raise RuntimeError("no .sln within 2 directory levels")
    return Path(sln), policy


def third_party_agent_files(ws):
    return sorted(p.name for p in ws.iterdir() if p.name.lower() in THIRD_PARTY_AGENT_FILES)


def install_agents_md(ws, agents_md):
    existing = third_party_agent_files(ws)
    if any(n.lower() == "agents.md" for n in existing):
        raise RuntimeError(f"repo already has {existing} at base_commit; refusing to overwrite it")
    shutil.copyfile(agents_md, ws / "AGENTS.md")
    git_exclude(ws, "AGENTS.md")


def dirty_files(ws):
    """Tracked or untracked (not ignored) files that differ from HEAD."""
    out = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], ws)
    entries = [e for e in out.split("\0") if e]
    return sorted({e[3:] for e in entries})


def collect_patch(ws, base, exclude=()):
    """Everything changed vs base_commit, except files the setup itself changed (restore/build
    rewrite some tracked files, e.g. BenchmarkDotNet's template.json versions)."""
    git(["add", "-A"], ws)
    pathspec = ["--", ".", *[f":(exclude,literal){p}" for p in exclude]] if exclude else []
    patch = git(["diff", "--cached", "--binary", base, *pathspec], ws)
    git(["reset", "-q"], ws)
    return patch


# ---- build check ------------------------------------------------------------------------------

ERROR_RE = re.compile(r"^(?P<file>[^\s(][^(]*?)\((?P<line>\d+),\d+\): error (?P<id>[A-Z]+\d+): (?P<msg>.*?)(?: \[(?P<proj>[^\]]+)\])?$")
# Errors without a source location, e.g. "CSC : error RS2003: ... [/path/X.csproj]" or "X.csproj : error NU1101: ..."
TOOL_ERROR_RE = re.compile(r"^(?P<origin>.*?)\s*: error (?P<id>[A-Z]+\d+): (?P<msg>.*?)(?: \[(?P<proj>[^\]]+)\])?$")


def build_check(ws, sln, timeout, env):
    started = time.time()
    proc = run(["dotnet", "build", str(sln), "--no-restore", *lc.DOTNET_FLAGS, "-clp:ErrorsOnly", "-v:q"],
               ws, timeout=timeout, env=env, check=False)
    errors = set()
    for line in (proc.stdout + proc.stderr).splitlines():
        line = line.strip()
        m = ERROR_RE.match(line)
        if m:
            rel = os.path.relpath(m["file"], ws) if os.path.isabs(m["file"]) else m["file"]
            errors.add(f"{rel}:{m['line']}: {m['id']}: {m['msg'][:200]}")
            continue
        m = TOOL_ERROR_RE.match(line)
        if m:
            where = m["proj"] or m["origin"]
            where = os.path.relpath(where, ws) if os.path.isabs(where) else where
            errors.add(f"{where}: {m['id']}: {m['msg'][:200]}")
    return {"exit": proc.returncode, "seconds": round(time.time() - started, 1),
            "errorCount": len(errors), "errors": sorted(errors)[:50],
            "tail": None if proc.returncode == 0 else (proc.stdout + proc.stderr)[-1500:]}


# ---- Roslyn servers -----------------------------------------------------------------------------

def http_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read() or b"null")


def port_free(port):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
    except urllib.error.HTTPError:
        return False
    except Exception:
        return True
    return False


class Server:
    def __init__(self, name, cmd, cwd, log_path, agent_user=None):
        self.name = name
        self.agent_user = agent_user
        self.log = open(log_path, "w", encoding="utf8")
        if agent_user:  # runs as the agent user; stopped by kill_user (the runner can't signal it)
            cmd = as_user(agent_user, cmd, agent_env())
        self.proc = subprocess.Popen(cmd, cwd=cwd, stdout=self.log, stderr=subprocess.STDOUT,
                                     env=dotnet_env(), start_new_session=True)

    def stop(self):
        if self.proc.poll() is None:
            if self.agent_user:
                kill_user(self.agent_user)
            else:
                try:
                    os.killpg(self.proc.pid, signal.SIGKILL)  # API + Roslyn build hosts / MCP wrapper
                except ProcessLookupError:
                    pass
        self.proc.wait()
        self.log.close()


def start_roslyn(ws, sln, out, run_tag, load_timeout, agent_user=None, call_log=None):
    for port in (API_PORT, MCP_PORT):
        if not port_free(port):
            raise RuntimeError(f"port {port} is already in use (stale server?)")
    api_dir, mcp_dir = ROSLYN_API_DIR, ROSLYN_MCP_DIR
    api = Server("api", ["dotnet", str(api_dir / "RoslynAnalyzerApi.dll"),
                         "--urls", f"http://127.0.0.1:{API_PORT}",
                         "--solution", str(sln),
                         "--Roslyn:RestoreOnLoad", "false",       # the runner already restored (both conditions)
                         "--Roslyn:RunId", run_tag,
                         "--Roslyn:CallLogPath", str(call_log or out / "roslyn-calls.jsonl")],
                 api_dir, out / "roslyn-api.log", agent_user)
    servers = [api]
    try:
        started, health = time.time(), None
        while time.time() - started < load_timeout:
            if api.proc.poll() is not None:
                raise RuntimeError(f"Roslyn API exited ({api.proc.returncode}); see roslyn-api.log")
            try:
                health = http_json(f"http://127.0.0.1:{API_PORT}/api/Analyze/health")
                if health["status"] in ("ready", "failed"):
                    break
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                pass
            time.sleep(1)
        if not health or health["status"] != "ready":
            raise RuntimeError(f"Roslyn API not ready: {health and (health.get('status'), health.get('error'))}")
        load_seconds = round(time.time() - started, 1)
        mcp = Server("mcp", ["dotnet", str(mcp_dir / "RoslynAnalyzerMcp.dll"),
                             "--urls", f"http://127.0.0.1:{MCP_PORT}",
                             "--RoslynApi:BaseUrl", f"http://127.0.0.1:{API_PORT}",
                             "--RoslynApi:RunId", run_tag],
                     mcp_dir, out / "roslyn-mcp.log", agent_user)
        servers.append(mcp)
        deadline = time.time() + 60
        while time.time() < deadline and port_free(MCP_PORT):
            if mcp.proc.poll() is not None:
                raise RuntimeError(f"MCP wrapper exited ({mcp.proc.returncode}); see roslyn-mcp.log")
            time.sleep(0.5)
        if port_free(MCP_PORT):
            raise RuntimeError("MCP wrapper did not start listening within 60s")
        info = {k: health.get(k) for k in ("status", "solutionPath", "projectCount", "documentCount",
                                           "workspaceDiagnosticCount", "warnings", "skippedProjects")}
        info["loadSeconds"] = load_seconds
        return servers, info
    except Exception:
        for s in servers:
            s.stop()
        raise


# ---- prompt -----------------------------------------------------------------------------------

PROMPT = """<uploaded_files>
{workdir}
</uploaded_files>

I've uploaded a C# code repository in the directory {workdir}. Consider the following issue description:

<issue_description>
{problem_statement}
</issue_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <issue_description> are met?
I've already taken care of all changes to any of the test files described in the <issue_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!
Your task is to make the minimal changes to non-test files in the {workdir} directory to ensure the <issue_description> is satisfied.
"""


# ---- one task ---------------------------------------------------------------------------------

def run_one(task, condition, args, out):
    out.mkdir(parents=True, exist_ok=True)
    rec = {"instance_id": task["instance_id"], "repo": task["repo"], "condition": condition,
           "dryRun": args.dry_run, "startedAt": dt.datetime.now().isoformat(timespec="seconds"),
           "maxSteps": args.max_steps, "timeoutMinutes": args.timeout_minutes,
           "agentUser": args.agent_user or None}
    agent = args.agent_user or None
    servers = []
    ws = None
    t_all = time.time()
    try:
        t0 = time.time()
        if agent:
            reset_agent_state(agent)
        ws = prepare_workspace(task, args.cache, args.work)
        rec["workspace"] = str(ws)
        rec["history"] = history_check(ws, task["base_commit"])
        if history_problems(rec["history"]):
            raise RuntimeError("; ".join(history_problems(rec["history"])))
        rec["thirdPartyAgentFiles"] = third_party_agent_files(ws)

        rec["sdk"] = task_sdk(task)
        env = dotnet_env(rec["sdk"])
        rec["dotnetVersion"] = run(["dotnet", "--version"], ws, env=env).stdout.strip()
        if rec["dotnetVersion"] != rec["sdk"]:
            raise RuntimeError(f"dotnet --version is {rec['dotnetVersion']}, harness uses {rec['sdk']} (global.json?)")

        setup = lc.REPO_SETUP.get(task["repo"], {})
        sln, how = pick_solution(ws, task, args.solution_policy)
        prepare = [list(cmd) for cmd in setup.get("prepare", [])]
        if sln.suffix == ".slnf":
            fixed, dropped = sanitize_slnf(ws, sln.name)
            if dropped:
                log(f"  {sln.name} lists {len(dropped)} project(s) missing from its .sln; using {fixed}")
                rec["slnfDroppedProjects"] = dropped
                prepare = [[fixed if a == sln.name else a for a in cmd] for cmd in prepare]
                sln = ws / fixed
        gold_sln, _ = pick_solution(ws, task, "gold")
        rec["solution"] = str(sln.relative_to(ws))
        rec["solutionPolicy"] = how
        rec["solutionDiffersFromGoldPick"] = how != "repo-setup" and gold_sln != sln
        log(f"  sdk {rec['sdk']}, solution {rec['solution']} ({how}"
            f"{'; gold pick differs: ' + str(gold_sln.relative_to(ws)) if rec['solutionDiffersFromGoldPick'] else ''})")
        for cmd in prepare:
            log(f"  prepare: {' '.join(cmd)}")
            run(cmd, ws, timeout=3600, env=env)
        run(["dotnet", "restore", str(sln), *lc.DOTNET_FLAGS], ws, timeout=1800, env=env)
        rec["prepareSeconds"] = round(time.time() - t0, 1)

        if not args.no_build_check:
            log("  baseline build")
            rec["baselineBuild"] = build_check(ws, sln, args.build_timeout, env)
            log(f"    baseline: exit {rec['baselineBuild']['exit']}, {rec['baselineBuild']['errorCount']} errors"
                f" ({rec['baselineBuild']['seconds']}s)")
        rec["setupDirtyFiles"] = [f for f in dirty_files(ws) if not f.endswith(".ablation.slnf")]
        if rec["setupDirtyFiles"]:
            log(f"  setup changed {len(rec['setupDirtyFiles'])} tracked/untracked file(s); excluded from the patch")

        if condition == "roslyn":
            install_agents_md(ws, args.agents_md)

        # Agent phase: hand the workspace and a fresh scratch dir to the agent user.
        scratch = AGENT_SCRATCH if agent else out
        persistence = (scratch / "openhands") if agent else (args.openhands / condition)
        prompt = PROMPT.format(workdir=ws, problem_statement=task["problem_statement"].strip())
        (out / "task.md").write_text(prompt, encoding="utf8")
        if agent:
            shutil.copytree(args.openhands / condition, persistence)   # pristine settings every run
            shutil.copyfile(HERE / "oh_driver.py", AGENT_BIN / "oh_driver.py")
            shutil.copyfile(out / "task.md", scratch / "task.md")      # before the chown below
            sudo("chown", "-R", f"{agent}:{agent}", ws, scratch)
            rec["sandbox"], bad = sandbox_probe(agent, ws)
            if bad:
                raise RuntimeError(f"sandbox check failed for user {agent}: {bad}")
        driver_py = (AGENT_BIN if agent else HERE) / "oh_driver.py"

        if condition == "roslyn":
            log("  starting Roslyn API + MCP wrapper")
            servers, rec["roslyn"] = start_roslyn(ws, sln, out, f"{args.run_id}/{task['instance_id']}", args.load_timeout,
                                                  agent, scratch / "roslyn-calls.jsonl")
            r = rec["roslyn"]
            log(f"    ready in {r['loadSeconds']}s: {r['projectCount']} projects, {r['documentCount']} docs, "
                f"{r['workspaceDiagnosticCount']} workspace diag, {len(r['warnings'] or [])} warnings")
        else:
            for port in (API_PORT, MCP_PORT):
                if not port_free(port):
                    raise RuntimeError(f"text condition but port {port} is in use: a Roslyn server is still running")

        # The agent's terminal inherits this: only the task's harness SDK is on PATH.
        oh_vars = dict(OPENHANDS_PERSISTENCE_DIR=str(persistence), OPENHANDS_SUPPRESS_BANNER="1",
                       PYTHONWARNINGS="ignore")
        if agent:
            # The model cost map is bundled with litellm; don't try to fetch the live one (no internet).
            env = agent_env(rec["sdk"], **oh_vars, LITELLM_LOCAL_MODEL_COST_MAP="True")
            wrap = lambda cmd: as_user(agent, cmd, env)
            spawn_env = dict(os.environ)
        else:
            env = dict(env)
            env.update(oh_vars)
            wrap = lambda cmd: cmd
            spawn_env = env
        # Same kind of shell the OpenHands terminal tool starts (interactive bash, reads ~/.bashrc).
        shell = subprocess.run(wrap(["bash", "-i", "-c", "dotnet --version"]), cwd=ws, env=spawn_env,
                               capture_output=True, text=True, timeout=120)
        rec["agentShellDotnet"] = (shell.stdout.strip().splitlines() or [""])[-1]
        if agent and args.dry_run:
            # The agent's own `dotnet build/test` restores implicitly; it must work offline from /srv/nuget.
            r = subprocess.run(wrap(["dotnet", "restore", str(sln), *lc.DOTNET_FLAGS]), cwd=ws, env=spawn_env,
                               capture_output=True, text=True, timeout=1800)
            rec["agentOfflineRestore"] = {"exit": r.returncode,
                                          "tail": None if r.returncode == 0 else (r.stdout + r.stderr)[-1200:]}
        summary_file = scratch / ("driver-dry.json" if args.dry_run else "driver.json")
        events_file = scratch / "events.jsonl"
        driver = [str(args.oh_python), "-W", "ignore", str(driver_py), "--workdir", str(ws),
                  "--summary", str(summary_file)]
        if args.dry_run:
            driver.append("--dry-run")
        else:
            driver += ["--task-file", str(scratch / "task.md"), "--events", str(events_file),
                       "--max-steps", str(args.max_steps)]
        rec["driverCommand"] = " ".join(driver)
        log("  agent: " + ("dry run (build agent, check MCP; no LLM calls)" if args.dry_run else "running"))
        t0 = time.time()
        # Wall clock is a safety net only; the step limit is meant to end runs. On timeout the whole
        # process group (driver + agent terminal/tmux children) is killed and the run is marked.
        rec["timedOut"] = False
        with open(out / "driver.log", "w", encoding="utf8") as dlog:
            proc = subprocess.Popen(wrap(driver), cwd=ws, env=spawn_env, stdout=dlog, stderr=subprocess.STDOUT,
                                    start_new_session=True)
            try:
                rec["driverExit"] = proc.wait(timeout=args.timeout_minutes * 60)
            except subprocess.TimeoutExpired:
                rec["timedOut"] = True
                rec["driverExit"] = "timeout"
                log(f"  TIMEOUT after {args.timeout_minutes} min; killing the agent")
                if agent:
                    kill_user(agent)
                else:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                proc.wait()
        rec["agentSeconds"] = round(time.time() - t0, 1)
        try:  # what the model ran as (size vs size_vram = GPU/CPU split, context_length); still loaded now
            rec["ollamaPs"] = [{k: m.get(k) for k in ("name", "size", "size_vram", "context_length")}
                               for m in http_json("http://127.0.0.1:11434/api/ps").get("models", [])]
        except Exception as ex:
            rec["ollamaPs"] = f"unavailable: {ex}"
        if agent:
            # Did /run/WSL become accessible while the agent ran? (the guard re-locks it within ~1 s
            # and logs each time)
            since = dt.datetime.fromtimestamp(t0).strftime("%Y-%m-%d %H:%M:%S")
            j = sudo("journalctl", "-q", "-o", "cat", "-u", "ablation-interop-guard", "--since", since, check=False)
            rec["interopSocketRelockedDuringAgent"] = j.stdout.count("re-locked /run/WSL")
            # End of the agent phase: nothing of the agent user keeps running (Roslyn servers too),
            # then the workspace and the scratch dir go back to the runner.
            for s in servers:
                s.stop()
            servers = []
            kill_user(agent)
            sudo("chown", "-R", f"{os.getuid()}:{os.getgid()}", ws, scratch)
            for name in ("driver-dry.json", "driver.json", "events.jsonl", "roslyn-calls.jsonl"):
                if (scratch / name).exists():
                    shutil.copyfile(scratch / name, out / name)
            if (persistence / "conversations").is_dir():
                shutil.copytree(persistence / "conversations", out / "conversations", dirs_exist_ok=True)
        summary_file = out / ("driver-dry.json" if args.dry_run else "driver.json")
        rec["driver"] = json.loads(summary_file.read_text()) if summary_file.exists() else None
        if rec["driver"] is None and (out / "events.jsonl").exists():
            # Killed before the driver wrote its summary: count steps from the event log.
            actions = 0
            with open(out / "events.jsonl", encoding="utf8") as f:
                for line in f:
                    try:
                        actions += json.loads(line).get("kind") == "ActionEvent"
                    except ValueError:
                        pass
            rec["stepsFromEvents"] = actions

        patch = collect_patch(ws, task["base_commit"], exclude=rec["setupDirtyFiles"])
        (out / "patch.diff").write_text(patch, encoding="utf8")
        rec["patchLines"] = patch.count("\n")
        rec["patchFiles"] = re.findall(r"^\+\+\+ b/(.+)$", patch, re.M)

        if not args.no_build_check and not args.dry_run:
            log("  final build")
            rec["finalBuild"] = build_check(ws, sln, args.build_timeout, dotnet_env(rec["sdk"]))
    except Exception as ex:
        rec["error"] = f"{type(ex).__name__}: {ex}"
        log(f"  ERROR {rec['error'][:400]}")
    finally:
        for s in servers:
            s.stop()
        if agent:
            try:
                kill_user(agent)
                if ws is not None and ws.exists():
                    sudo("chown", "-R", f"{os.getuid()}:{os.getgid()}", ws, AGENT_SCRATCH)
            except Exception as ex:
                rec.setdefault("error", f"cleanup: {type(ex).__name__}: {ex}")
        if ws is not None and ws.exists() and not args.keep_workspace:
            shutil.rmtree(ws, ignore_errors=True)
    rec["totalSeconds"] = round(time.time() - t_all, 1)
    rec["finishedAt"] = dt.datetime.now().isoformat(timespec="seconds")
    write_json(out / "run.json", rec)  # last: its presence marks the run as done (resume skips it)
    return rec


# ---- dry-run checks + summary -----------------------------------------------------------------

def dry_checks(rec):
    """What a dry run must show before agents are allowed to run."""
    problems = []
    d = rec.get("driver") or {}
    if rec.get("error"):
        problems.append(rec["error"][:160])
    if rec.get("driverExit") != 0:
        problems.append(f"driver exit {rec.get('driverExit')}")
    if d and d.get("model") != EXPECTED_MODEL:
        problems.append(f"model {d.get('model')}, settings say {EXPECTED_MODEL}")
    if rec.get("sdk") and rec.get("agentShellDotnet") != rec["sdk"]:
        problems.append(f"agent shell dotnet {rec.get('agentShellDotnet')!r}, harness SDK {rec['sdk']}")
    if rec.get("solutionDiffersFromGoldPick"):
        problems.append("no-gold solution pick differs from the gold-aware pick")
    if rec.get("patchLines"):
        problems.append(f"non-empty patch with no agent ({rec['patchFiles']})")
    if "history" in rec:
        problems += history_problems(rec["history"])
    else:
        problems.append("no git history check")
    if rec.get("agentUser"):
        bad = {k: (rec.get("sandbox") or {}).get(k) for k, v in SANDBOX_EXPECT.items()
               if (rec.get("sandbox") or {}).get(k) != v}
        if bad:
            problems.append(f"sandbox: {bad}")
        if (rec.get("agentOfflineRestore") or {}).get("exit") != 0:
            problems.append(f"agent's offline restore: {rec.get('agentOfflineRestore')}")
    if rec["condition"] == "roslyn":
        mcp = (d.get("mcpCheck") or {}).get("roslyn", {})
        if len(mcp.get("tools", [])) != 7:
            problems.append(f"roslyn MCP tools: {mcp.get('tools') or mcp.get('error')}")
        if (mcp.get("health") or {}).get("status") != "ready":
            problems.append(f"roslyn_health via MCP: {mcp.get('health')}")
        if d.get("skills") != ["agents"]:
            problems.append(f"skills should be exactly ['agents'] (AGENTS.md), got {d.get('skills')}")
        if (rec.get("roslyn") or {}).get("warnings"):
            problems.append(f"health warnings: {rec['roslyn']['warnings'][:2]}")
    else:
        if d.get("mcpServers"):
            problems.append(f"text condition has MCP servers {d['mcpServers']}")
        if d.get("skills") and not rec.get("thirdPartyAgentFiles"):
            problems.append(f"text condition should load no skills, got {d.get('skills')}")
    if d.get("publicSkills"):
        problems.append("public skills are enabled")
    if rec.get("thirdPartyAgentFiles"):
        problems.append(f"repo ships agent instruction files {rec['thirdPartyAgentFiles']} (loaded in both conditions)")
    b = rec.get("baselineBuild")
    if b and (b["exit"] != 0 or b["errorCount"]):
        problems.append(f"baseline build exit {b['exit']}, {b['errorCount']} errors")
    return problems


def write_summary(run_dir, records):
    lines = [f"# Run {run_dir.name}", "",
             "| Condition | Instance | Solution | Prep s | Baseline build | Roslyn load | Driver | Steps | Patch | Checks |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in records:
        b = r.get("baselineBuild")
        rs = r.get("roslyn")
        d = r.get("driver") or {}
        lines.append("| {c} | {i} | {s} | {p} | {b} | {rl} | {de} | {st} | {pl} | {ck} |".format(
            c=r["condition"], i=r["instance_id"], s=f"{r.get('solution', '')} (SDK {r.get('sdk', '?')})",
            p=r.get("prepareSeconds", ""),
            b=f"exit {b['exit']}, {b['errorCount']} err, {b['seconds']}s" if b else "",
            rl=f"{rs['projectCount']} proj, {rs['workspaceDiagnosticCount']} diag, {rs['loadSeconds']}s" if rs else "",
            de=r.get("driverExit", ""), st=d.get("actions", ""), pl=r.get("patchLines", ""),
            ck="; ".join(r.get("checks", [])) or "OK"))
    timed_out = [f"{r['condition']}/{r['instance_id']}" for r in records if r.get("timedOut")]
    lines += ["", f"Timed out (wall clock, safety net): {len(timed_out)}" + (f" — {', '.join(timed_out)}" if timed_out else "")]
    interrupted = sorted(f"{p.parent.name}/{p.name}" for p in run_dir.glob("_interrupted/*/*"))
    lines += [f"Interrupted and redone (e.g. PC restart): {len(interrupted)}" + (f" — {', '.join(interrupted)}" if interrupted else "")]
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--conditions", nargs="+", choices=CONDITIONS, default=list(CONDITIONS))
    ap.add_argument("--instances", nargs="*", help="instance ids (default: the whole sample)")
    ap.add_argument("--dry-run", action="store_true", help="everything except the agent; no LLM calls")
    ap.add_argument("--max-steps", type=int, default=100)
    ap.add_argument("--timeout-minutes", type=float, default=120,
                    help="wall clock per agent run; a safety net only (the step limit should end runs)")
    ap.add_argument("--no-build-check", action="store_true",
                    help="skip the baseline build (setup) and the final build (compile-error metric)")
    ap.add_argument("--build-timeout", type=int, default=1800)
    ap.add_argument("--load-timeout", type=int, default=1200, help="seconds for the Roslyn API to load")
    ap.add_argument("--solution-policy", choices=("no-gold", "gold"), default="no-gold")
    ap.add_argument("--keep-workspace", action="store_true")
    ap.add_argument("--agent-user", default="agent" if SANDBOX else "",
                    help="run the agent (and the Roslyn servers) as this sandboxed user; default 'agent' "
                         "in the sandbox distro. Real (non-dry) runs refuse to start without it.")
    for key, value in DEFAULTS.items():
        ap.add_argument("--" + key.replace("_", "-"), type=Path, default=value)
    args = ap.parse_args()
    if not args.dry_run and not args.agent_user:
        sys.exit("refusing to run agents unsandboxed: run inside the ablation-sandbox distro (--agent-user)")
    if args.agent_user and not SANDBOX:
        sys.exit("--agent-user needs the sandbox layout (/srv/ablation, /opt/roslyn); see SETUP_NOTES.md")

    sample = json.loads(args.sample.read_text())
    tasks = [t for t in sample if not args.instances or t["instance_id"] in args.instances]
    if args.instances and len(tasks) != len(args.instances):
        sys.exit(f"unknown instance ids: {set(args.instances) - {t['instance_id'] for t in tasks}}")
    for path in (args.oh_python, args.agents_md, ROSLYN_API_DIR / "RoslynAnalyzerApi.dll",
                 ROSLYN_MCP_DIR / "RoslynAnalyzerMcp.dll"):
        if not path.exists():
            sys.exit(f"missing {path}")

    global MODEL_NAME, EXPECTED_MODEL
    EXPECTED_MODEL = settings_model(args.openhands)                     # e.g. openai/qwen3.5:9b
    MODEL_NAME = "openhands-1.16.0__" + re.sub(r"[^A-Za-z0-9.]+", "-", EXPECTED_MODEL.split("/", 1)[-1])
    run_dir = args.runs / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    config = {k: str(v) for k, v in vars(args).items()} | {
        "argv": sys.argv, "sandbox": SANDBOX, "model": EXPECTED_MODEL, "predictionsModelName": MODEL_NAME,
        "roslynApiCommit": git(["rev-parse", "HEAD"], ROSLYN_COMMIT_REPO).strip()}
    config_file = run_dir / "config.json"
    if config_file.exists():
        # Resuming the same run id (e.g. after a PC restart): settings that change results must match.
        old = json.loads(config_file.read_text())
        diff = {k: (old.get(k), config[k]) for k in RESUME_MUST_MATCH if old.get(k) != config[k]}
        if diff:
            sys.exit(f"run {args.run_id} exists with different settings {diff}; use a new --run-id")
        config = old | {"resumes": old.get("resumes", []) + [{"at": dt.datetime.now().isoformat(timespec="seconds"),
                                                                "argv": sys.argv}]}
        log(f"resuming run {args.run_id}")
    write_json(config_file, config)

    records = []
    for i, task in enumerate(tasks, 1):
        for condition in args.conditions:
            out = run_dir / condition / task["instance_id"]
            if (out / "run.json").exists():
                # Finished before (run.json is written last, atomically): keep it, don't rerun.
                rec = json.loads((out / "run.json").read_text())
                log(f"[{i}/{len(tasks)}] {condition}: {task['instance_id']} already done, skipped")
            else:
                if out.exists():
                    # Interrupted mid-run (no run.json): keep its files for the record, redo from scratch.
                    stash = run_dir / "_interrupted" / condition / f"{task['instance_id']}-{time.strftime('%Y%m%d-%H%M%S')}"
                    stash.parent.mkdir(parents=True, exist_ok=True)
                    out.rename(stash)
                    log(f"[{i}/{len(tasks)}] {condition}: {task['instance_id']} was interrupted; moved to {stash}, redoing")
                log(f"[{i}/{len(tasks)}] {condition}: {task['instance_id']}")
                rec = run_one(task, condition, args, out)
                if args.dry_run:
                    rec["checks"] = dry_checks(rec)
                    write_json(out / "run.json", rec)
                if args.dry_run:
                    log(f"  => {'; '.join(rec['checks']) or 'OK'} ({rec['totalSeconds']}s)")
                else:
                    d = rec.get("driver") or {}
                    log(f"  => {'ERROR ' + rec['error'][:200] if rec.get('error') else 'finished'}: "
                        f"steps {d.get('actions', rec.get('stepsFromEvents'))}, status {d.get('status')}, "
                        f"timedOut {rec.get('timedOut')}, patch {rec.get('patchLines')} lines ({rec['totalSeconds']}s)")
            records.append(rec)
            write_summary(run_dir, records)
            if not args.dry_run:
                write_predictions(run_dir, condition)
    log(f"done: {run_dir / 'summary.md'}")


EXPECTED_MODEL = None
RESUME_MUST_MATCH = ("model", "dry_run", "max_steps", "timeout_minutes", "no_build_check", "build_timeout", "load_timeout",
                     "solution_policy", "agent_user", "sample", "openhands", "oh_python", "agents_md",
                     "roslynApiCommit")


def write_json(path, obj):
    """Atomic: a crash or power loss leaves either the old file or the new one, never half of it."""
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf8") as f:
        f.write(json.dumps(obj, indent=2))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_predictions(run_dir, condition):
    """predictions.jsonl for a condition, rebuilt from every finished run (idempotent on resume)."""
    lines = []
    for run_json in sorted((run_dir / condition).glob("*/run.json")):
        rec = json.loads(run_json.read_text())
        patch_file = run_json.parent / "patch.diff"
        if rec.get("dryRun") or not patch_file.exists():
            continue
        lines.append(json.dumps({"instance_id": rec["instance_id"], "model_name_or_path": f"{MODEL_NAME}__{condition}",
                                 "model_patch": patch_file.read_text(encoding="utf8")}))
    write_text = "".join(l + "\n" for l in lines)
    tmp = run_dir / condition / "predictions.jsonl.tmp"
    tmp.write_text(write_text, encoding="utf8")
    os.replace(tmp, run_dir / condition / "predictions.jsonl")
    # The harness (swe_sharp_bench.cli --predictions_path) reads a JSON array.
    write_json(run_dir / condition / "predictions.json", [json.loads(l) for l in lines])


if __name__ == "__main__":
    main()
