"""Second-model pilot summary (requested 2026-11-18): per model x condition and per run.

    python3 pilot2_summary.py OUT_DIR RUN_DIR:HARNESS_REPORT_DIR [...]

RUN_DIR is ~/ablation/runs/pilot2-<model>; HARNESS_REPORT_DIR holds that run id's harness reports
(openhands-1.16.0__<model>__<cond>.pilot2-<model>-<cond>.json). Writes OUT_DIR/pilot2_summary.{json,md}.

Columns:
- successful edits: file_editor create/str_replace/insert/undo_edit that did not error (step_limit.py)
  + terminal commands that write files (sed -i, heredoc/redirect into a source file, ...) and exited 0
- malformed tool calls: calls Ollama could not parse (driver.malformedToolCalls)
- invalid tool calls: calls the SDK rejected, i.e. unknown tool or bad arguments (AgentErrorEvents)
- minutes: agent wall clock per run
- Roslyn analysis calls: agent-initiated roslyn_analyze_* / roslyn_diagnostics calls; for
  roslyn-enforced also the runner's automatic calls
- hit step limit: the SDK's MaxIterationsReached event (not run.json's hitStepLimit; SETUP_NOTES)
- invalid run: Ollama truncated a prompt or cut a reply (context budget check), or the condenser check failed
- ollama ps: what /api/ps reported right after the run (name, size, size_vram, context_length)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from step_limit import hit_step_limit, load_events, successful_edits  # noqa: E402

WRITE_RE = re.compile(r"sed\s+-i|perl\s+-pi|>\s*[\w./-]+\.(cs|csproj|props|targets|xml|json)\b|\btee\s|git\s+apply|patch\s+-p|"
                      r"open\([^)]*['\"][wa]['\"]|write_text|cat\s*<<|python3?\s+-\s*<<")


def terminal_writes(events):
    obs = {e.get("action_id"): e for e in events if e.get("kind") == "ObservationEvent"}
    n = 0
    for e in events:
        a = e.get("action") or {}
        if e.get("kind") == "ActionEvent" and a.get("kind") == "TerminalAction" and WRITE_RE.search(a.get("command") or ""):
            if ((obs.get(e["id"]) or {}).get("observation") or {}).get("exit_code") == 0:
                n += 1
    return n


def gb(x):
    return round(x / 2**30, 1) if isinstance(x, (int, float)) else x


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in sys.argv[2:]:
        run_dir, rep_dir = (Path(p).expanduser() for p in spec.split(":", 1))
        resolved, graded = set(), set()
        for rep in rep_dir.glob(f"*.{run_dir.name}-*.json"):
            r = json.loads(rep.read_text())
            cond = re.search(r"__(text|roslyn-enforced|roslyn)\.", rep.name).group(1)
            resolved |= {(cond, i) for i in r.get("resolved_ids", [])}
            graded |= {(cond, i) for k in ("completed_ids", "empty_patch_ids", "error_ids") for i in r.get(k, [])}
        for rj in sorted(p for p in run_dir.glob("*/*/run.json") if not p.parts[-3].startswith("_")):
            rec = json.loads(rj.read_text())
            d = rec.get("driver") or {}
            ev = load_events(rj.parent)
            cond, inst = rec["condition"], rec["instance_id"]
            tools = d.get("toolCalls") or {}
            auto = d.get("roslynEnforced") or {}
            ps = rec.get("ollamaPs")
            rows.append({
                "model": (json.loads((run_dir / "config.json").read_text()).get("model") or "").split("/", 1)[-1],
                "condition": cond, "instance": inst,
                "resolved": "yes" if (cond, inst) in resolved else ("no" if (cond, inst) in graded else "not graded"),
                "successfulEdits": successful_edits(ev) + terminal_writes(ev),
                "fileEditorEdits": successful_edits(ev), "terminalWrites": terminal_writes(ev),
                "malformedToolCalls": d.get("malformedToolCalls") or 0,
                "invalidToolCalls": sum(1 for e in ev if e.get("kind") == "AgentErrorEvent"),
                "minutes": round((rec.get("agentSeconds") or 0) / 60, 1),
                "roslynAnalysisCalls": sum(n for t, n in tools.items() if t.startswith("roslyn_analyze") or t == "roslyn_diagnostics"),
                "roslynAutoCalls": auto.get("calls"),
                "modelTurns": d.get("modelTurns"), "actions": d.get("actions"),
                "hitStepLimit": hit_step_limit(ev), "timedOut": rec.get("timedOut"),
                "status": d.get("status"), "patchLines": rec.get("patchLines"),
                "invalidRun": rec.get("invalid") or [], "runError": rec.get("error"),
                "maxPromptPlusReply": (rec.get("ollamaLog") or {}).get("maxPromptPlusReply"),
                "condensations": (d.get("condenserCheck") or {}).get("condensations"),
                "ollamaPs": [{"name": m.get("name"), "sizeGB": gb(m.get("size")), "vramGB": gb(m.get("size_vram")),
                              "gpuPct": round(100 * m["size_vram"] / m["size"]) if m.get("size") else None,
                              "context": m.get("context_length")} for m in ps] if isinstance(ps, list) else ps,
            })
    (out / "pilot2_summary.json").write_text(json.dumps(rows, indent=1))
    md = ["| model | condition | task | resolved | edits | malformed | invalid calls | min | Roslyn analysis (auto) | turns | limit | invalid run | max prompt+reply | ollama ps |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        ps = r["ollamaPs"]
        pss = "; ".join(f"{m['name']} {m['sizeGB']}GB {m['gpuPct']}% GPU ctx {m['context']}" for m in ps) if isinstance(ps, list) else str(ps)
        md.append(f"| {r['model']} | {r['condition']} | {r['instance']} | {r['resolved']} | {r['successfulEdits']} | {r['malformedToolCalls']} | "
                  f"{r['invalidToolCalls']} | {r['minutes']} | {r['roslynAnalysisCalls']}" + (f" ({r['roslynAutoCalls']})" if r['roslynAutoCalls'] is not None else "") +
                  f" | {r['modelTurns']} | {'yes' if r['hitStepLimit'] else ''}{' TIMEOUT' if r['timedOut'] else ''} | {'; '.join(r['invalidRun'])[:60]} | "
                  f"{r['maxPromptPlusReply']} | {pss} |")
    md += ["", "| model | condition | runs | resolved | edits | malformed | invalid calls | mean min | Roslyn analysis | hit limit | invalid runs |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    keys = sorted({(r["model"], r["condition"]) for r in rows}, key=lambda k: (k[0], ["text", "roslyn", "roslyn-enforced"].index(k[1])))
    for m, c in keys:
        g = [r for r in rows if (r["model"], r["condition"]) == (m, c)]
        md.append(f"| {m} | {c} | {len(g)} | {sum(r['resolved'] == 'yes' for r in g)} | {sum(r['successfulEdits'] for r in g)} | "
                  f"{sum(r['malformedToolCalls'] for r in g)} | {sum(r['invalidToolCalls'] for r in g)} | "
                  f"{round(sum(r['minutes'] for r in g) / len(g), 1)} | {sum(r['roslynAnalysisCalls'] for r in g)} | "
                  f"{sum(r['hitStepLimit'] for r in g)} | {sum(bool(r['invalidRun']) for r in g)} |")
    (out / "pilot2_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
