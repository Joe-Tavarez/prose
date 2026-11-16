"""Check oh_driver.py's finish gate and malformed-tool-call recovery end to end with a scripted fake
LLM (no model, no network). Run as runner in the sandbox:
    /opt/openhands/tools/openhands/bin/python sandbox/test_finish_gate.py

Scenarios (scripted model replies, in order):
  gate      create a file -> finish (gate must send it back once with the condition's message)
            -> finish again (must be allowed: gate only once)
  malformed Ollama's HTTP 500 "error parsing tool call" (what gpt-oss caused in pilot 2) -> the run
            must continue with "Your tool call was malformed; ..." -> finish -> gate -> finish
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from oh_driver import GATE_MESSAGES, MALFORMED_MESSAGE  # noqa: E402

PORT = 18081
state = {"script": [], "requests": []}
OLLAMA_500 = {"error": {"message": "error parsing tool call: raw='It seems the grep command syntax might need "
                                   "quoting.{\"command\":\"grep -R x\"}', err=invalid character 'I' looking for "
                                   "beginning of value", "type": "api_error"}}


def tool_call(name, args):
    return {"id": f"call_{len(state['requests'])}", "type": "function",
            "function": {"name": name, "arguments": json.dumps(args)}}


class FakeLLM(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        state["requests"].append(body)
        step = state["script"][0] if state["script"] else ("finish",)
        # Like gpt-oss in pilot 2: the same context keeps producing the same unparseable call, so the
        # 500 persists through every client/litellm retry until the conversation changes (our message).
        recovered = MALFORMED_MESSAGE in json.dumps(body.get("messages"))
        if step[0] != "500" or recovered:
            state["script"].pop(0) if state["script"] else None
            if step[0] == "500":
                step = state["script"].pop(0) if state["script"] else ("finish",)
        if step[0] == "500":
            out, code = json.dumps(OLLAMA_500).encode(), 500
        else:
            call = (tool_call("file_editor", {"command": "create", "path": f"{os.environ['GATE_TEST_WORKDIR']}/new.txt",
                                              "file_text": "x\n", "security_risk": "LOW"})
                    if step[0] == "edit" else tool_call("finish", {"message": "done"}))
            out, code = json.dumps({"id": "r", "object": "chat.completion", "created": 0, "model": body.get("model"),
                                    "choices": [{"index": 0, "finish_reason": "tool_calls",
                                                 "message": {"role": "assistant", "content": "", "tool_calls": [call]}}],
                                    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}).encode(), 200
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


def user_texts():
    return [json.dumps(m.get("content")) for r in state["requests"] for m in r.get("messages", []) if m.get("role") == "user"]


def run_driver(condition, script):
    state["script"], state["requests"] = list(script), []
    tmp = Path(tempfile.mkdtemp())
    work, persist = tmp / "repo", tmp / "openhands"
    work.mkdir()
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    shutil.copytree(Path.home() / "ablation/openhands/text", persist)  # tested settings, LLM -> fake server
    s = json.loads((persist / "agent_settings.json").read_text())
    for llm in (s["llm"], s["condenser"]["llm"]):
        llm["base_url"] = f"http://127.0.0.1:{PORT}/v1"
        llm["num_retries"] = 0
    (persist / "agent_settings.json").write_text(json.dumps(s))
    (tmp / "task.md").write_text("Create new.txt and finish.")
    os.environ["GATE_TEST_WORKDIR"] = str(work)
    env = dict(os.environ, OPENHANDS_PERSISTENCE_DIR=str(persist), OPENHANDS_SUPPRESS_BANNER="1",
               LITELLM_LOCAL_MODEL_COST_MAP="True")
    p = subprocess.run([sys.executable, "-W", "ignore", str(HERE / "oh_driver.py"), "--workdir", str(work),
                        "--task-file", str(tmp / "task.md"), "--events", str(tmp / "events.jsonl"),
                        "--summary", str(tmp / "summary.json"), "--max-steps", "10", "--finish-gate", condition],
                       env=env, capture_output=True, text=True, timeout=300)
    summary = json.loads((tmp / "summary.json").read_text()) if (tmp / "summary.json").exists() else {}
    shutil.rmtree(tmp)
    return p, summary


def report(name, checks, p):
    for k, v in checks.items():
        print(f"  {name:17} {'ok  ' if v else 'FAIL'} {k}")
    if not all(checks.values()):
        print(p.stdout[-1500:], p.stderr[-1500:])
    return all(checks.values())


def main():
    srv = HTTPServer(("127.0.0.1", PORT), FakeLLM)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ok = True
    for condition in ("text", "roslyn"):
        p, s = run_driver(condition, [("edit",), ("finish",), ("finish",)])
        g = s.get("finishGate") or {}
        ok &= report(f"{condition}/gate", {
            "driver exit 0": p.returncode == 0,
            "gate triggered once": g.get("triggered") is True,
            "gate message (incl. 'fix the errors you introduced') reached the LLM":
                any(GATE_MESSAGES[condition] in t for t in user_texts()),
            "finished twice, then stopped (gate once)": s.get("toolCalls", {}).get("finish") == 2
                                                         and g.get("finishedAgainWithoutCheck") is True,
            "status finished": s.get("status") == "finished",
        }, p)
        p, s = run_driver(condition, [("500",), ("finish",), ("finish",)])
        ok &= report(f"{condition}/malformed", {
            "driver exit 0 (run not ended by the 500)": p.returncode == 0 and not s.get("error"),
            "counted: malformedToolCalls == 1": s.get("malformedToolCalls") == 1,
            "malformed message reached the LLM": any(MALFORMED_MESSAGE in t for t in user_texts()),
            "agent continued and finished": s.get("status") == "finished" and s.get("toolCalls", {}).get("finish", 0) >= 1,
            # failed turn + finish + finish after the gate = 3 turns (HTTP retries are not turns)
            "failed turn counted in the budget (modelTurns == 3)": s.get("modelTurns") == 3,
        }, p)
    print("finish gate + malformed recovery test:", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
