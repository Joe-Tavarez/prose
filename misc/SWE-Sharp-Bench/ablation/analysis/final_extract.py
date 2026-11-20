"""Final analysis, step 1 of 2 (runs in the sandbox, where the run records are): one JSON line per run of the
nine gpt-oss passes fix-r{1,2,3}-{text,roslyn,enforced}.

    python3 final_extract.py > final_runs.jsonl

Step 2 (final_combine.py, in Ubuntu next to the harness) joins these with the grading reports.

Definitions (SETUP_NOTES.md):
- model turns = driver.modelTurns (what the 100-step limit counts); actions = ActionEvents
- hit step limit = the SDK's MaxIterationsReached event (step_limit.py), not run.json's hitStepLimit
- successful edits = file_editor create/str_replace/insert/undo_edit that did not error, plus terminal
  commands that write files and exited 0 (pilot2_summary.terminal_writes)
- malformed tool calls = driver.malformedToolCalls (Ollama could not parse; recovered by the driver)
- invalid tool calls = AgentErrorEvents (unknown tool or bad arguments, rejected by the SDK)
- agent Roslyn analysis calls = the agent's own roslyn_analyze_* + roslyn_diagnostics calls (toolCalls holds
  agent-initiated calls only); runner automatic calls (roslyn-enforced) are counted apart
- compile errors added = finalBuild errors minus the same run's baselineBuild errors, matched on
  id + file + message (not line). NU1900 (NuGet vulnerability audit, which fails because the sandbox has no
  network) is also reported separately so it can be left out.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from step_limit import hit_step_limit, load_events, successful_edits  # noqa: E402
from pilot2_summary import terminal_writes  # noqa: E402

RUNS = Path.home() / "ablation" / "runs"
PASSES = [(r, c, f"fix-r{r}-{s}") for r in (1, 2, 3) for c, s in (("text", "text"), ("roslyn", "roslyn"),
                                                                   ("roslyn-enforced", "enforced"))]
ERR = re.compile(r"^(?P<file>[^:]*?)(?::\d+)?: (?P<id>[A-Z]+\d+): (?P<msg>.*)$", re.S)


def err_key(s):
    m = ERR.match(s.strip())
    return (m["id"], m["file"], m["msg"].strip()) if m else ("?", "", s.strip())


def main():
    for rnd, cond, rid in PASSES:
        for rj in sorted((RUNS / rid / cond).glob("*/run.json")):
            rec = json.loads(rj.read_text())
            d = rec.get("driver") or {}
            ev = load_events(rj.parent)
            tools = d.get("toolCalls") or {}
            auto = d.get("roslynEnforced") or {}
            gate = auto.get("gate") or {}
            fg = d.get("finishGate") or {}
            base = {err_key(e) for e in (rec.get("baselineBuild") or {}).get("errors") or []}
            final = (rec.get("finalBuild") or {}).get("errors") or []
            added = sorted({err_key(e) for e in final} - base)
            fe = successful_edits(ev)
            tw = terminal_writes(ev)
            # runs killed by the 2-hour wall clock have no driver summary: count from the events instead
            # (distinct LLM responses = a lower bound on model turns, since turns with no tool call or a
            # malformed one leave no agent event; on finished runs it equals actions exactly)
            turns, acts, src = d.get("modelTurns"), d.get("actions"), "driver"
            if turns is None:
                turns = len({e.get("llm_response_id") for e in ev if e.get("source") == "agent" and e.get("llm_response_id")})
                acts = sum(1 for e in ev if e.get("kind") == "ActionEvent")
                src = "events (lower bound)"
            print(json.dumps({
                "round": rnd, "condition": cond, "runId": rid, "instance": rec["instance_id"],
                "modelTurns": turns, "actions": acts, "modelTurnsSource": src,
                "hitStepLimit": hit_step_limit(ev), "timedOut": bool(rec.get("timedOut")),
                "driverStatus": d.get("status"), "invalidRun": rec.get("invalid") or [], "runError": rec.get("error"),
                "agentMinutes": round((rec.get("agentSeconds") or 0) / 60, 1),
                "patchLines": rec.get("patchLines") or 0, "patchFiles": len(rec.get("patchFiles") or []),
                "successfulEdits": fe + tw, "fileEditorEdits": fe, "terminalWrites": tw,
                "malformedToolCalls": d.get("malformedToolCalls") or 0,
                "invalidToolCalls": sum(1 for e in ev if e.get("kind") == "AgentErrorEvent"),
                "agentRoslynAnalysisCalls": sum(n for t, n in tools.items()
                                                if t.startswith("roslyn_analyze") or t == "roslyn_diagnostics"),
                "agentRoslynCallsAll": sum(n for t, n in tools.items() if t.startswith("roslyn")),
                "autoRoslynCalls": sum((auto.get("calls") or {}).values()) if auto else None,
                "autoRoslynAnalysisCalls": sum(n for t, n in (auto.get("calls") or {}).items()
                                               if t.startswith("roslyn_analyze") or t == "roslyn_diagnostics") if auto else None,
                "enforcedGateChecks": gate.get("checks") if auto else None,
                "enforcedGateRefusals": gate.get("refusals") if auto else None,
                "enforcedGateAllowedWithIntroducedErrors": gate.get("allowedWithIntroducedErrors") if auto else None,
                "finishGateTriggered": fg.get("triggered") if fg else None,
                "baselineBuildErrors": len(base), "finalBuildExit": (rec.get("finalBuild") or {}).get("exit"),
                "compileErrorsAdded": len(added),
                "compileErrorsAddedExclNU1900": sum(1 for k in added if k[0] != "NU1900"),
                "addedErrorIds": sorted({k[0] for k in added}),
                "condensations": d.get("condensations"),
                "maxPromptPlusReply": (rec.get("ollamaLog") or {}).get("maxPromptPlusReply"),
            }))


if __name__ == "__main__":
    main()
