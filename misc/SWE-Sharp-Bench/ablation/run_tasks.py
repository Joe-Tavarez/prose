"""Per-task runner for the IS755 Roslyn ablation (OpenHands text-only vs. text + Roslyn MCP).

For each (condition, instance), identically in both conditions unless noted:
  1. fresh checkout of the task repo at base_commit (+ submodules) in WORK/<owner>__<name>,
     cloned from a local full-clone cache (Nerdbank.GitVersioning needs full history)
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
ROSLYN_REPO = Path("/mnt/c/Repos/RoslynAnalyzerApi")      # AGENTS.md + loadcheck helpers (source of truth)
ROSLYN_BUILD = HOME / "build" / "RoslynAnalyzerApi"         # WSL build of the API + MCP wrapper
# This folder lives at misc/SWE-Sharp-Bench/ablation in the prose fork, next to the harness.
HARNESS = HERE.parent / "harness" if (HERE.parent / "harness").is_dir() else Path("/mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness")
DEFAULTS = dict(
    sample=HARNESS / "data/tasks/sample.json",
    cache=HOME / "swe-repos",
    work=ABLATION / "work",
    runs=ABLATION / "runs",
    openhands=ABLATION / "openhands",
    oh_python=HOME / ".local/share/uv/tools/openhands/bin/python",
    agents_md=ROSLYN_REPO / "agent" / "AGENTS.md",
)
API_PORT, MCP_PORT = 5050, 5051
CONDITIONS = ("text", "roslyn")
MODEL_NAME = "openhands-1.16.0__qwen3.5-9b"
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


SDK_ROOTS = HOME / ".dotnet-sdks"
HARNESS_SDK = json.loads((HERE / "harness_sdk.json").read_text())  # from harness_sdk.py (harness's own table)


def dotnet_env(sdk=None):
    """Environment with exactly one dotnet on PATH. sdk=None: the API's own install (~/.dotnet, SDK 8).
    sdk='8.0.404': the isolated root with only the SDK the harness image uses for the task."""
    root = HOME / ".dotnet" if sdk is None else SDK_ROOTS / sdk
    if not (root / "dotnet").exists():
        raise RuntimeError(f"no .NET root {root} (run install_sdks.sh)")
    env = dict(os.environ)
    path = [p for p in env.get("PATH", "").split(":") if p and ".dotnet" not in p]
    env.update(DOTNET_ROOT=str(root), DOTNET_MULTILEVEL_LOOKUP="0", DOTNET_CLI_TELEMETRY_OPTOUT="1",
               DOTNET_NOLOGO="1", DOTNET_SKIP_FIRST_TIME_EXPERIENCE="1",
               PATH=":".join([str(root), str(root / "tools"), *path]))
    return env


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


def prepare_workspace(task, cache_dir, work_dir):
    cached = cache_repo(task, cache_dir)
    ws = work_dir / cached.name
    if ws.exists():
        shutil.rmtree(ws)
    work_dir.mkdir(parents=True, exist_ok=True)
    git(["clone", "-q", "--no-checkout", str(cached), str(ws)], work_dir)
    # The agent sees a normal GitHub clone; relative submodule URLs resolve against it.
    git(["remote", "set-url", "origin", f"https://github.com/{task['repo']}.git"], ws)
    if not git(["config", "--get-regexp", r"^extensions\."], ws, check=False).strip():
        git(["config", "core.repositoryformatversion", "0"], ws)  # old libgit2 (SourceLink) rejects 1
    git(["checkout", "-q", "-f", "--detach", task["base_commit"]], ws)
    git(["clean", "-q", "-ffdx"], ws)
    if (ws / ".gitmodules").exists():
        git(["submodule", "update", "-q", "--init", "--recursive", "--force"], ws)
    return ws


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
    def __init__(self, name, cmd, cwd, log_path):
        self.name = name
        self.log = open(log_path, "w", encoding="utf8")
        self.proc = subprocess.Popen(cmd, cwd=cwd, stdout=self.log, stderr=subprocess.STDOUT,
                                     env=dotnet_env(), start_new_session=True)

    def stop(self):
        if self.proc.poll() is None:
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)  # API + Roslyn build hosts / MCP wrapper
            except ProcessLookupError:
                pass
        self.proc.wait()
        self.log.close()


def start_roslyn(ws, sln, out, run_tag, load_timeout):
    for port in (API_PORT, MCP_PORT):
        if not port_free(port):
            raise RuntimeError(f"port {port} is already in use (stale server?)")
    api_dir = ROSLYN_BUILD / "bin/Debug/net8.0"
    mcp_dir = ROSLYN_BUILD / "mcp/RoslynAnalyzerMcp/bin/Debug/net8.0"
    api = Server("api", ["dotnet", str(api_dir / "RoslynAnalyzerApi.dll"),
                         "--urls", f"http://127.0.0.1:{API_PORT}",
                         "--solution", str(sln),
                         "--Roslyn:RestoreOnLoad", "false",       # the runner already restored (both conditions)
                         "--Roslyn:RunId", run_tag,
                         "--Roslyn:CallLogPath", str(out / "roslyn-calls.jsonl")],
                 api_dir, out / "roslyn-api.log")
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
                     mcp_dir, out / "roslyn-mcp.log")
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
           "maxSteps": args.max_steps, "timeoutMinutes": args.timeout_minutes}
    servers = []
    ws = None
    t_all = time.time()
    try:
        t0 = time.time()
        ws = prepare_workspace(task, args.cache, args.work)
        rec["workspace"] = str(ws)
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
            log("  starting Roslyn API + MCP wrapper")
            servers, rec["roslyn"] = start_roslyn(ws, sln, out, f"{args.run_id}/{task['instance_id']}", args.load_timeout)
            r = rec["roslyn"]
            log(f"    ready in {r['loadSeconds']}s: {r['projectCount']} projects, {r['documentCount']} docs, "
                f"{r['workspaceDiagnosticCount']} workspace diag, {len(r['warnings'] or [])} warnings")
        else:
            for port in (API_PORT, MCP_PORT):
                if not port_free(port):
                    raise RuntimeError(f"text condition but port {port} is in use: a Roslyn server is still running")

        prompt = PROMPT.format(workdir=ws, problem_statement=task["problem_statement"].strip())
        (out / "task.md").write_text(prompt, encoding="utf8")

        # The agent's terminal inherits this: only the task's harness SDK is on PATH.
        env = dict(env)
        env.update(OPENHANDS_PERSISTENCE_DIR=str(args.openhands / condition), OPENHANDS_SUPPRESS_BANNER="1",
                   PYTHONWARNINGS="ignore")
        # Same kind of shell the OpenHands terminal tool starts (interactive bash, reads ~/.bashrc).
        shell = subprocess.run(["bash", "-i", "-c", "dotnet --version"], cwd=ws, env=env,
                               capture_output=True, text=True, timeout=120)
        rec["agentShellDotnet"] = (shell.stdout.strip().splitlines() or [""])[-1]
        driver = [str(args.oh_python), "-W", "ignore", str(HERE / "oh_driver.py"), "--workdir", str(ws),
                  "--summary", str(out / ("driver-dry.json" if args.dry_run else "driver.json"))]
        if args.dry_run:
            driver.append("--dry-run")
        else:
            driver += ["--task-file", str(out / "task.md"), "--events", str(out / "events.jsonl"),
                       "--max-steps", str(args.max_steps)]
        rec["driverCommand"] = " ".join(driver)
        log("  agent: " + ("dry run (build agent, check MCP; no LLM calls)" if args.dry_run else "running"))
        t0 = time.time()
        # Wall clock is a safety net only; the step limit is meant to end runs. On timeout the whole
        # process group (driver + agent terminal/tmux children) is killed and the run is marked.
        rec["timedOut"] = False
        with open(out / "driver.log", "w", encoding="utf8") as dlog:
            proc = subprocess.Popen(driver, cwd=ws, env=env, stdout=dlog, stderr=subprocess.STDOUT,
                                    start_new_session=True)
            try:
                rec["driverExit"] = proc.wait(timeout=args.timeout_minutes * 60)
            except subprocess.TimeoutExpired:
                rec["timedOut"] = True
                rec["driverExit"] = "timeout"
                log(f"  TIMEOUT after {args.timeout_minutes} min; killing the agent")
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        rec["agentSeconds"] = round(time.time() - t0, 1)
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
        if not args.dry_run:
            pred = {"instance_id": task["instance_id"], "model_name_or_path": f"{MODEL_NAME}__{condition}",
                    "model_patch": patch}
            with open(out.parent / "predictions.jsonl", "a", encoding="utf8") as f:
                f.write(json.dumps(pred) + "\n")

        if not args.no_build_check and not args.dry_run:
            log("  final build")
            rec["finalBuild"] = build_check(ws, sln, args.build_timeout, dotnet_env(rec["sdk"]))
    except Exception as ex:
        rec["error"] = f"{type(ex).__name__}: {ex}"
        log(f"  ERROR {rec['error'][:400]}")
    finally:
        for s in servers:
            s.stop()
        if ws is not None and ws.exists() and not args.keep_workspace:
            shutil.rmtree(ws, ignore_errors=True)
    rec["totalSeconds"] = round(time.time() - t_all, 1)
    (out / "run.json").write_text(json.dumps(rec, indent=2), encoding="utf8")
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
    if d and d.get("model") != "openai/qwen3.5:9b":
        problems.append(f"model {d.get('model')}")
    if rec.get("sdk") and rec.get("agentShellDotnet") != rec["sdk"]:
        problems.append(f"agent shell dotnet {rec.get('agentShellDotnet')!r}, harness SDK {rec['sdk']}")
    if rec.get("solutionDiffersFromGoldPick"):
        problems.append("no-gold solution pick differs from the gold-aware pick")
    if rec.get("patchLines"):
        problems.append(f"non-empty patch with no agent ({rec['patchFiles']})")
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
    for key, value in DEFAULTS.items():
        ap.add_argument("--" + key.replace("_", "-"), type=Path, default=value)
    args = ap.parse_args()

    sample = json.loads(args.sample.read_text())
    tasks = [t for t in sample if not args.instances or t["instance_id"] in args.instances]
    if args.instances and len(tasks) != len(args.instances):
        sys.exit(f"unknown instance ids: {set(args.instances) - {t['instance_id'] for t in tasks}}")
    for path in (args.oh_python, args.agents_md, ROSLYN_BUILD / "bin/Debug/net8.0/RoslynAnalyzerApi.dll"):
        if not path.exists():
            sys.exit(f"missing {path}")

    run_dir = args.runs / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(json.dumps(
        {k: str(v) for k, v in vars(args).items()} | {"argv": sys.argv,
         "roslynApiCommit": git(["rev-parse", "HEAD"], ROSLYN_BUILD).strip()}, indent=2))

    records = []
    for i, task in enumerate(tasks, 1):
        for condition in args.conditions:
            log(f"[{i}/{len(tasks)}] {condition}: {task['instance_id']}")
            rec = run_one(task, condition, args, run_dir / condition / task["instance_id"])
            if args.dry_run:
                rec["checks"] = dry_checks(rec)
                (run_dir / condition / task["instance_id"] / "run.json").write_text(json.dumps(rec, indent=2))
            log(f"  => {'; '.join(rec.get('checks', [])) or 'OK'} ({rec['totalSeconds']}s)")
            records.append(rec)
            write_summary(run_dir, records)
    log(f"done: {run_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
