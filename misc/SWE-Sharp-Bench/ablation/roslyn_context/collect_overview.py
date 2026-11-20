"""roslyn-context scoping, step 1 of 2 (runs in the sandbox as the runner user; no agent, no model calls):
for each task, a fresh workspace at base_commit (the runner's own prepare_workspace + history check), the
runner's no-gold solution pick and restore with the task's harness SDK, then the Roslyn API built from the
overview-endpoint branch (port 5060, as the runner user) and POST /api/Analyze/overview. Also collects the
non-Roslyn control's inputs: `git ls-files` and the root README, at base_commit.

    python3 collect_overview.py API_DIR OUT_DIR [INSTANCE ...]

Leakage rules (the design's constraint): the only task fields passed on are instance_id, repo and base_commit
(any code path that wanted the gold patch or test patch would fail with KeyError); the task text is the
<issue_description> of the task.md the agents received (runs/fix-r1-text/text/<iid>/task.md); the workspace has
no history after base_commit (history_check) and the task's future test files are never applied.
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

RUNNER = Path.home() / "ablation" / "runner"
sys.path.insert(0, str(RUNNER))
import run_tasks as rt  # noqa: E402  (the runner's functions; nothing in the runner is changed)

PORT = 5060
STOP = {"should", "would", "could", "there", "their", "which", "where", "when", "what", "this", "that", "these",
        "those", "with", "without", "from", "into", "have", "has", "been", "being", "will", "also", "only", "then",
        "than", "them", "they", "some", "such", "other", "about", "after", "before", "because", "while", "does",
        "doesn", "isn", "aren", "make", "made", "using", "used", "uses", "like", "just", "more", "most", "very",
        "here", "issue", "description", "expected", "actual", "behavior", "behaviour", "version", "example", "code",
        "steps", "reproduce", "following", "currently", "however", "instead", "case", "cases", "work", "works",
        "working", "need", "needs", "want", "able", "following", "value", "values", "type", "types", "class",
        "method", "methods", "string", "return", "returns", "true", "false", "null", "public", "private", "static",
        "void", "var", "new", "get", "set", "the", "and", "for", "not", "but", "are", "was", "you", "can", "all",
        "any", "use", "one", "two", "its", "it's", "see", "add", "fix", "bug", "error", "exception", "test", "tests"}


def issue_text(iid):
    md = (rt.ABLATION / "runs" / "fix-r1-text" / "text" / iid / "task.md").read_text(encoding="utf8")
    m = re.search(r"<issue_description>\n(.*)\n</issue_description>", md, re.S)
    return m.group(1).strip()


def terms_from(text):
    """Code-like identifiers first (CamelCase, dotted, backticked), then other words of 4+ letters."""
    code, words = [], []
    text = re.sub(r"https?://\S+", " ", text)  # URLs are not symbols
    for tok in re.findall(r"`([^`\n]{2,80})`", text):
        code += [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", tok) if t.lower() not in STOP]
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", text):
        parts = tok.split(".")
        for p in parts:
            if len(p) < 3 or p.lower() in STOP:
                continue
            # code-shaped: part of a dotted name, CamelCase, ALLCaps+lower (XMLReader), or with an underscore
            if (len(parts) > 1 and p[0].isupper()) or re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]|[A-Za-z]_[A-Za-z]", p):
                code.append(p)
            elif len(p) >= 4:
                words.append(p.lower())
    dedup = lambda xs: list(dict.fromkeys(xs))
    code = dedup(code)
    return code, [w for w in dedup(words) if w.lower() not in {c.lower() for c in code}]


def post(path, body, timeout=1800):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def collect(task, api_dir, out):
    iid = task["instance_id"]
    rec = {"instance": iid, "repo": task["repo"], "baseCommit": task["base_commit"], "startedAt": time.strftime("%FT%T")}
    work = rt.ABLATION / "ctx" / "work"
    ws = rt.prepare_workspace(task, rt.DEFAULTS["cache"], work)
    try:
        rec["history"] = rt.history_check(ws, task["base_commit"])
        if rt.history_problems(rec["history"]):
            raise RuntimeError("; ".join(rt.history_problems(rec["history"])))
        sdk = rt.task_sdk(task)
        env = rt.dotnet_env(sdk)
        setup = rt.lc.REPO_SETUP.get(task["repo"], {})
        sln, how = rt.pick_solution(ws, task, "no-gold")
        prepare = [list(c) for c in setup.get("prepare", [])]
        if sln.suffix == ".slnf":
            fixed, dropped = rt.sanitize_slnf(ws, sln.name)
            if dropped:
                prepare = [[fixed if a == sln.name else a for a in c] for c in prepare]
                sln = ws / fixed
        rec.update(sdk=sdk, solution=str(sln.relative_to(ws)), solutionPolicy=how)
        for c in prepare:
            rt.run(c, ws, timeout=3600, env=env)
        rt.run(["dotnet", "restore", str(sln), *rt.lc.DOTNET_FLAGS], ws, timeout=1800, env=env)

        # control inputs (non-Roslyn): tracked files and the root README, at base_commit
        rec["files"] = rt.git(["ls-files"], ws).splitlines()
        readmes = sorted((p for p in ws.iterdir() if p.is_file() and p.name.lower().startswith("readme")),
                         key=lambda p: (p.suffix.lower() != ".md", p.name))
        rec["readmeName"] = readmes[0].name if readmes else None
        rec["readme"] = readmes[0].read_text(encoding="utf8", errors="replace") if readmes else None

        text = issue_text(iid)
        code, words = terms_from(text)
        rec.update(issueText=text, codeTerms=code, wordTerms=words)
        api = rt.Server("overview-api", ["dotnet", str(Path(api_dir) / "RoslynAnalyzerApi.dll"),
                                         "--urls", f"http://127.0.0.1:{PORT}", "--solution", str(sln),
                                         "--Roslyn:RestoreOnLoad", "false", "--Roslyn:RunId", f"ctx-{iid}",
                                         "--Roslyn:CallLogPath", str(out / f"{iid}.calls.jsonl")],
                        api_dir, out / f"{iid}.api.log")
        try:
            t0, health = time.time(), None
            while time.time() - t0 < 1200:
                if api.proc.poll() is not None:
                    raise RuntimeError(f"API exited ({api.proc.returncode})")
                try:
                    health = rt.http_json(f"http://127.0.0.1:{PORT}/api/Analyze/health")
                    if health["status"] in ("ready", "failed"):
                        break
                except Exception:
                    pass
                time.sleep(1)
            rec["health"] = {k: (health or {}).get(k) for k in ("status", "projectCount", "documentCount",
                                                               "workspaceDiagnosticCount", "warnings", "error")}
            rec["loadSeconds"] = round(time.time() - t0, 1)
            if not health or health["status"] != "ready":
                raise RuntimeError(f"API not ready: {rec['health']}")
            t1 = time.time()
            rec["overview"] = post("/api/Analyze/overview", {"maxTypesPerProject": 300, "maxMembersPerType": 40,
                                                             "priorityTerms": code})
            rec["overviewSeconds"] = round(time.time() - t1, 1)
        finally:
            api.stop()
    finally:
        rt.shutil.rmtree(ws, ignore_errors=True)
    return rec


def main():
    api_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    sample = json.loads(rt.DEFAULTS["sample"].read_text())
    wanted = set(sys.argv[3:])
    for t in sample:
        iid = t["instance_id"]
        if (wanted and iid not in wanted) or iid == "spectreconsole__spectre-console-1303":  # excluded task
            continue
        dest = out / f"{iid}.json"
        if dest.exists():
            continue
        task = {"instance_id": iid, "repo": t["repo"], "base_commit": t["base_commit"]}  # nothing else
        rt.log(f"{iid}: collecting")
        try:
            rec = collect(task, api_dir, out)
        except Exception as ex:  # record and go on
            rec = {"instance": iid, "error": f"{type(ex).__name__}: {ex}"[:2000]}
        dest.write_text(json.dumps(rec))
        rt.log(f"{iid}: {'ERROR ' + rec['error'][:200] if 'error' in rec else 'ok'}")


if __name__ == "__main__":
    main()
