"""Per-run results table for a run id: resolved (from harness reports), steps, wall clock, NEW compile
errors (final build minus the same run's baseline, matched on id + file + message, not line), timeout,
and Roslyn tool use.

    python3 pilot_report.py RUN_DIR [HARNESS_REPORT.json ...]
"""
import json
import re
import sys
from pathlib import Path

ROSLYN = ("roslyn", "roslyn-enforced")
LINE = re.compile(r"^(?P<file>[^:]+):\d+: ")  # "path:LINE: ID: msg" -> drop the line number


def error_keys(build):
    return {LINE.sub(r"\g<file>: ", e) for e in (build or {}).get("errors", [])}


def main():
    run_dir = Path(sys.argv[1])
    resolved, graded = set(), set()
    for rep in sys.argv[2:]:
        r = json.loads(Path(rep).read_text())
        cond = re.search(r"__(text|roslyn-enforced|roslyn)\.", Path(rep).name).group(1)
        resolved |= {(cond, i) for i in r.get("resolved_ids", [])}
        graded |= {(cond, i) for i in r.get("completed_ids", []) + r.get("empty_patch_ids", []) + r.get("error_ids", [])}
    rows = []
    for rj in sorted(p for p in run_dir.glob("*/*/run.json") if not p.parts[-3].startswith("_")):  # skip _interrupted
        rec = json.loads(rj.read_text())
        d = rec.get("driver") or {}
        cond, inst = rec["condition"], rec["instance_id"]
        tools = d.get("toolCalls") or {}
        auto = d.get("roslynEnforced") or {}
        roslyn_calls = sum(n for t, n in tools.items() if "roslyn" in t.lower())
        api_log = rj.parent / "roslyn-calls.jsonl"
        # The SDK's step limit (max_iteration_per_run) counts iterations = model turns, including
        # turns without a tool call (corrective "use a tool" feedback); actions = tool calls.
        events = [json.loads(l) for l in open(rj.parent / "events.jsonl")] if (rj.parent / "events.jsonl").exists() else []
        hit_limit = any(e.get("code") == "MaxIterationsReached" for e in events)
        no_tool_turns = sum(1 for e in events if e.get("kind") == "MessageEvent" and e.get("source") == "user"
                            and "did not include a function call" in json.dumps(e.get("llm_message")))
        agent_errors = [e.get("error", "")[:90] for e in events if e.get("kind") == "AgentErrorEvent"]
        new_errors = sorted(error_keys(rec.get("finalBuild")) - error_keys(rec.get("baselineBuild")))
        rows.append({
            "condition": cond, "instance": inst,
            "resolved": "yes" if (cond, inst) in resolved else ("no" if (cond, inst) in graded else "not graded"),
            "steps": d.get("actions", rec.get("stepsFromEvents")),
            "hitIterationLimit": hit_limit, "noToolCallTurns": no_tool_turns, "agentErrors": agent_errors,
            # invalid tool calls = calls the SDK rejected (unknown tool, bad/missing arguments)
            # + tool calls Ollama couldn't parse at all (recovered by the driver, see SETUP_NOTES)
            "invalidToolCalls": len(agent_errors) + (d.get("malformedToolCalls") or 0),
            "malformedToolCalls": d.get("malformedToolCalls"),
            "roslynAnalysisCalls": sum(n for t, n in tools.items() if t.startswith("roslyn_analyze") or t == "roslyn_diagnostics")
            if cond in ROSLYN else None,
            "ollamaPs": rec.get("ollamaPs"),
            "finishGate": d.get("finishGate"),
            "agentMinutes": round(rec.get("agentSeconds", 0) / 60, 1),
            "totalMinutes": round(rec.get("totalSeconds", 0) / 60, 1),
            "newCompileErrors": len(new_errors), "newErrorSample": new_errors[:3],
            "finalBuildExit": (rec.get("finalBuild") or {}).get("exit"),
            "timedOut": rec.get("timedOut"),
            # agent-initiated roslyn_* tool calls; runner auto-calls (roslyn-enforced) are counted separately
            "roslynToolCalls": roslyn_calls if cond in ROSLYN else None,
            "roslynAutoCalls": auto.get("calls"), "roslynAutoFailures": auto.get("failures"),
            "enforcedGate": auto.get("gate"), "enforcedBaseline": auto.get("baseline"),
            "autoViewAppends": auto.get("viewAppends"), "autoEditChecks": auto.get("editChecks"),
            # API requests in roslyn-calls.jsonl include the runner's auto-calls
            "roslynApiRequests": (sum(1 for _ in open(api_log)) if api_log.exists() else 0) if cond in ROSLYN else None,
            "toolCalls": tools, "status": d.get("status"), "driverError": d.get("error"), "runError": rec.get("error"),
            "patchLines": rec.get("patchLines"), "patchFiles": rec.get("patchFiles"),
            "tokens": d.get("tokens"), "interopRemovals": rec.get("interopHandlerRemovedDuringAgent"),
        })
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
