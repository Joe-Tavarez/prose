"""Check oh_driver.py --enforce (condition roslyn-enforced) end to end with a scripted fake LLM and a fake
Roslyn MCP server (no model, no Roslyn, no network). Run as runner in the sandbox:
    /opt/openhands/tools/openhands/bin/python sandbox/test_enforce.py

Fake Roslyn: the workspace has Old.cs, which has a pre-existing error (in the baseline). Any .cs file
containing BROKEN has an error. roslyn_diagnostics reads the files on disk, but only as of the last
roslyn_reload (like the real service), so the gate's own reload is tested too.

Scenarios (scripted model replies, in order):
  never-fixes  view Old.cs, create New.cs with BROKEN, agent calls roslyn_diagnostics, then finish x5:
               refused 3 times (errors attached, baseline error not listed), 4th finish allowed
  fixes        same start, finish (refused once), str_replace removes BROKEN, finish -> allowed
  no-cs        create notes.txt, roslyn_diagnostics, finish -> allowed at once (no compile needed)
  narrowed     agent reloads a project that hides New.cs (roslyn_reload path=Narrow.csproj), creates New.cs
               with BROKEN + TRUNC (fake diagnostics then say truncated), finish: the gate reloads the
               original App.sln, still sees the error and says "1 or more"; fix, finish -> allowed
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LLM_PORT, MCP_PORT = 18083, 18084
state = {"script": [], "requests": []}


# ---- fake Roslyn MCP server (separate process: --serve-mcp WORKDIR) -------------------------------------
def serve_mcp(workdir):
    from fastmcp import FastMCP
    mcp = FastMCP("roslyn")
    loaded = {}  # path -> text as of the last reload
    sln = os.path.join(workdir, "App.sln")
    current = {"path": sln}  # the loaded solution/project; Narrow.csproj only contains Old.cs
    calls = Path(workdir).parent / "mcp-calls.jsonl"

    def log(tool, args):
        with open(calls, "a") as f:
            f.write(json.dumps({"tool": tool, "args": args}) + "\n")

    def snapshot(files=None):
        for p in (files or [str(p) for p in Path(workdir).rglob("*.cs")]):
            loaded[os.path.abspath(p)] = Path(p).read_text() if Path(p).exists() else ""
        for p in list(loaded):
            if not Path(p).exists():
                loaded.pop(p)

    def errors(files=None):
        out = []
        for p, text in sorted(loaded.items()):
            if current["path"] != sln and not p.endswith("Old.cs"):
                continue
            if files and os.path.abspath(p) not in {os.path.abspath(os.path.join(workdir, f)) for f in files}:
                continue
            if p.endswith("Old.cs"):
                out.append({"filePath": p, "project": "P", "id": "CS0246", "severity": "Error",
                            "message": "pre-existing error", "line": 1, "column": 1})
            if "BROKEN" in text:
                out.append({"filePath": p, "project": "P", "id": "CS0103", "severity": "Error",
                            "message": "The name 'BROKEN' does not exist in the current context", "line": 2, "column": 5})
        return out

    @mcp.tool(name="roslyn_health")
    def health() -> str:
        log("roslyn_health", {})
        return json.dumps({"status": "ready", "solutionPath": current["path"]})

    @mcp.tool(name="roslyn_reload")
    def reload(files: list[str] | None = None, path: str | None = None, restore: bool | None = None) -> str:
        log("roslyn_reload", {"files": files, "path": path})
        if path:
            current["path"] = os.path.abspath(path)
        snapshot(None if path else files)
        return json.dumps({"status": "ready", "reloaded": files or "all"})

    @mcp.tool(name="roslyn_analyze_file")
    def analyze_file(filePath: str, includeDiagnostics: bool = True) -> str:
        log("roslyn_analyze_file", {"filePath": filePath})
        return json.dumps({"filePath": filePath, "types": [{"name": "Old", "methods": ["void Run(int x)"]}],
                           "diagnostics": errors([filePath])})

    @mcp.tool(name="roslyn_diagnostics")
    def diagnostics(files: list[str] | None = None, projects: list[str] | None = None,
                    includeWarnings: bool = False, maxResults: int = 100) -> str:
        log("roslyn_diagnostics", {"files": files})
        e = errors(files)
        return json.dumps({"scope": "files" if files else "projects", "errorCount": len(e), "warningCount": 0,
                           "projects": [], "diagnostics": e,
                           "truncated": any("TRUNC" in t for t in loaded.values()), "elapsedMs": 1, "notes": []})

    snapshot()
    mcp.run(transport="http", host="127.0.0.1", port=MCP_PORT, show_banner=False)


# ---- fake LLM ---------------------------------------------------------------------------------------------
def tool_call(name, args):
    return {"id": f"call_{len(state['requests'])}", "type": "function",
            "function": {"name": name, "arguments": json.dumps(args)}}


class FakeLLM(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        state["requests"].append(body)
        name, args = state["script"].pop(0) if state["script"] else ("finish", {"message": "done"})
        out = json.dumps({"id": "r", "object": "chat.completion", "created": 0, "model": body.get("model"),
                          "choices": [{"index": 0, "finish_reason": "tool_calls",
                                       "message": {"role": "assistant", "content": "",
                                                   "tool_calls": [tool_call(name, args)]}}],
                          "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


def wait_port(port, seconds=30):
    end = time.time() + seconds
    while time.time() < end:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.2)
    raise RuntimeError(f"port {port} not listening")


def messages_text():
    return json.dumps([r.get("messages") for r in state["requests"]])


def run_driver(script_for):
    tmp = Path(tempfile.mkdtemp())
    work, persist = tmp / "repo", tmp / "openhands"
    work.mkdir()
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    (work / "Old.cs").write_text("class Old {\n  void Run(int x) { }\n}\n")
    subprocess.run(["git", "-C", str(work), "add", "."], check=True)
    subprocess.run(["git", "-C", str(work), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"], check=True)
    mcp = subprocess.Popen([sys.executable, "-W", "ignore", __file__, "--serve-mcp", str(work)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_port(MCP_PORT)
        shutil.copytree(Path.home() / "ablation/openhands/roslyn", persist)  # tested settings, endpoints -> fakes
        s = json.loads((persist / "agent_settings.json").read_text())
        for llm in (s["llm"], s["condenser"]["llm"]):
            llm["base_url"] = f"http://127.0.0.1:{LLM_PORT}/v1"
            llm["num_retries"] = 0
        (persist / "agent_settings.json").write_text(json.dumps(s))
        m = json.loads((persist / "mcp.json").read_text())
        m["mcpServers"]["roslyn"]["url"] = f"http://127.0.0.1:{MCP_PORT}/mcp"
        (persist / "mcp.json").write_text(json.dumps(m))
        (tmp / "task.md").write_text("Fix it and finish.")
        state["script"], state["requests"] = script_for(work), []
        env = dict(os.environ, OPENHANDS_PERSISTENCE_DIR=str(persist), OPENHANDS_SUPPRESS_BANNER="1",
                   LITELLM_LOCAL_MODEL_COST_MAP="True")
        p = subprocess.run([sys.executable, "-W", "ignore", str(HERE / "oh_driver.py"), "--workdir", str(work),
                            "--task-file", str(tmp / "task.md"), "--events", str(tmp / "events.jsonl"),
                            "--summary", str(tmp / "summary.json"), "--max-steps", "20",
                            "--finish-gate", "roslyn", "--enforce"],
                           env=env, capture_output=True, text=True, timeout=600)
        summary = json.loads((tmp / "summary.json").read_text()) if (tmp / "summary.json").exists() else {}
        mcp_calls = [json.loads(l) for l in open(tmp / "mcp-calls.jsonl")] if (tmp / "mcp-calls.jsonl").exists() else []
        return p, summary, mcp_calls
    finally:
        mcp.terminate()
        mcp.wait(10)
        shutil.rmtree(tmp) if not os.environ.get("KEEP") else print("kept", tmp)


def report(name, checks, p):
    for k, v in checks.items():
        print(f"  {name:12} {'ok  ' if v else 'FAIL'} {k}")
    if not all(checks.values()):
        print(p.stdout[-2500:], p.stderr[-2500:])
    return all(checks.values())


def start(work):
    return [("file_editor", {"command": "view", "path": f"{work}/Old.cs", "security_risk": "LOW"}),
            ("file_editor", {"command": "create", "path": f"{work}/New.cs", "security_risk": "LOW",
                             "file_text": "class New {\n  int X = BROKEN;\n}\n"}),
            ("roslyn_diagnostics", {"files": ["New.cs"], "security_risk": "LOW"})]


def main():
    srv = HTTPServer(("127.0.0.1", LLM_PORT), FakeLLM)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ok = True

    p, s, calls = run_driver(lambda w: start(w) + [("finish", {"message": "done"})] * 5)
    e, g = s.get("roslynEnforced") or {}, (s.get("roslynEnforced") or {}).get("gate") or {}
    txt = messages_text()
    ok &= report("never-fixes", {
        "driver exit 0, status finished": p.returncode == 0 and s.get("status") == "finished",
        "view of .cs: roslyn_analyze_file appended": "[Automatic Roslyn analysis of Old.cs" in txt,
        "edit of .cs: reload + diagnostics appended (shows the new error)":
            "[Automatic Roslyn check after your edit: roslyn_reload + roslyn_diagnostics on New.cs]" in txt
            and "BROKEN' does not exist" in txt,
        "baseline taken before the agent (1 pre-existing error)": (e.get("baseline") or {}).get("errorCount") == 1,
        "refused exactly 3 times, then allowed": g.get("refusals") == 3 and g.get("allowedWithIntroducedErrors") is True
                                                 and s.get("toolCalls", {}).get("finish") == 4,
        "refusal lists the introduced error, not the baseline one":
            "compile error(s) you introduced" in txt and "New.cs:2: CS0103" in txt and "Old.cs:1: CS0246" not in txt,
        "agent-initiated roslyn calls counted apart (toolCalls roslyn_diagnostics == 1)":
            s.get("toolCalls", {}).get("roslyn_diagnostics") == 1,
        "auto calls counted (analyze_file 1; reload, diagnostics from edit + gate + baseline)":
            e.get("calls", {}).get("roslyn_analyze_file") == 1 and e.get("viewAppends") == 1 and e.get("editChecks") == 1
            and e.get("calls", {}).get("roslyn_diagnostics") == 1 + 1 + 4 and not e.get("failures"),
        "fake Roslyn saw exactly agent + auto calls": sum(c["tool"] == "roslyn_diagnostics" for c in calls) == 1 + 1 + 4 + 1,
    }, p)

    p, s, calls = run_driver(lambda w: start(w) + [
        ("finish", {"message": "done"}),
        ("file_editor", {"command": "str_replace", "path": f"{w}/New.cs", "old_str": "BROKEN", "new_str": "1",
                         "security_risk": "LOW"}),
        ("finish", {"message": "done"})])
    g = ((s.get("roslynEnforced") or {}).get("gate") or {})
    ok &= report("fixes", {
        "driver exit 0, status finished": p.returncode == 0 and s.get("status") == "finished",
        "refused once, then allowed after the fix": g.get("refusals") == 1 and g.get("lastIntroduced") == 0
                                                     and not g.get("allowedWithIntroducedErrors"),
        "two edit checks appended (create + str_replace)": (s.get("roslynEnforced") or {}).get("editChecks") == 2,
    }, p)

    p, s, calls = run_driver(lambda w: [
        ("file_editor", {"command": "create", "path": f"{w}/notes.txt", "file_text": "x\n", "security_risk": "LOW"}),
        ("roslyn_diagnostics", {"security_risk": "LOW"}), ("finish", {"message": "done"})])
    e = s.get("roslynEnforced") or {}
    ok &= report("no-cs", {
        "driver exit 0, status finished": p.returncode == 0 and s.get("status") == "finished",
        "no .cs view/edit hooks fired": e.get("viewAppends") == 0 and e.get("editChecks") == 0,
        "finish allowed at once, no compile at the gate": (e.get("gate") or {}).get("refusals") == 0
                                                           and (e.get("gate") or {}).get("checks") == 0,
    }, p)
    p, s, calls = run_driver(lambda w: [
        ("roslyn_reload", {"path": f"{w}/Narrow.csproj", "security_risk": "LOW"}),
        ("file_editor", {"command": "create", "path": f"{w}/New.cs", "security_risk": "LOW",
                         "file_text": "class New {\n  int X = BROKEN; // TRUNC\n}\n"}),
        ("finish", {"message": "done"}), ("finish", {"message": "done"}),
        ("file_editor", {"command": "str_replace", "path": f"{w}/New.cs", "old_str": "BROKEN", "new_str": "1",
                         "security_risk": "LOW"}),
        ("finish", {"message": "done"})])
    g = ((s.get("roslynEnforced") or {}).get("gate") or {})
    txt = messages_text()
    reloads = [c["args"] for c in calls if c["tool"] == "roslyn_reload"]
    sln = ((s.get("roslynEnforced") or {}).get("baseline") or {}).get("solutionPath") or ""
    # after the agent's narrowing reload and the create hook's reload; the str_replace hook reloads files=[New.cs]
    gate_reloads = [r for r in reloads[2:] if not r.get("files")]
    ok &= report("narrowed", {
        "driver exit 0, status finished": p.returncode == 0 and s.get("status") == "finished",
        "baseline recorded the original solution": sln.endswith("/App.sln"),
        "agent narrowed the loaded project": reloads[:1] and str(reloads[0].get("path")).endswith("Narrow.csproj"),
        "both gate checks did a full reload of App.sln": len(gate_reloads) == 2
            and all(r.get("path") == sln and not r.get("files") for r in gate_reloads),
        "gate still refused despite the agent's narrower project (once, then fixed)": g.get("refusals") == 1
            and g.get("lastIntroduced") == 0,
        "truncated list -> '1 or more compile error(s)'": "1 or more compile error(s) you introduced" in txt
            and "possibly more (diagnostics list capped)" in txt,
    }, p)
    print("roslyn-enforced test:", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--serve-mcp":
        serve_mcp(sys.argv[2])
    else:
        main()
