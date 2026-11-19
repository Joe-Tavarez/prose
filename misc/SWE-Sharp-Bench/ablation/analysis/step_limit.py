"""Step-limit accounting for the analysis (added 2026-11-18). Use this, never run.json's hitStepLimit.

The SDK's step limit (max_iteration_per_run = 100) counts model turns: every LLM call, including turns
whose tool call was malformed or named an unknown tool. oh_driver.py writes driver.hitStepLimit as
`actions >= max_steps`, i.e. it counts only tool calls that became ActionEvents, so a run that used its
100 turns with a few rejected calls reads False (fix-r1-text autofac-1424: 97 actions, 100 turns).
The runner is left unchanged (mid-experiment); the reliable signal is the SDK's own
ConversationErrorEvent with code MaxIterationsReached in events.jsonl.

    python3 step_limit.py RUN_DIR [RUN_DIR ...]     # per pass: runs, hit the limit, never edited
RUN_DIR is ~/ablation/runs/<run id>; folders starting with "_" (_interrupted, _sandbox_refused) are skipped.
"""
import json
import sys
from pathlib import Path

EDIT_CMDS = {"create", "str_replace", "insert", "undo_edit"}


def load_events(run_dir):
    p = Path(run_dir) / "events.jsonl"
    return [json.loads(l) for l in open(p)] if p.exists() else []


def hit_step_limit(events):
    """True when the SDK stopped the conversation at its iteration (model-turn) limit."""
    return any(e.get("kind") == "ConversationErrorEvent" and e.get("code") == "MaxIterationsReached" for e in events)


def successful_edits(events):
    """file_editor create/str_replace/insert/undo_edit calls whose observation was not an error.
    Edits made through the terminal (sed -i, heredocs) are not counted; see limit_extract.py for those."""
    obs = {e.get("action_id"): e for e in events if e.get("kind") == "ObservationEvent"}
    n = 0
    for e in events:
        a = e.get("action") or {}
        if e.get("kind") != "ActionEvent" or a.get("kind") != "FileEditorAction" or a.get("command") not in EDIT_CMDS:
            continue
        o = (obs.get(e["id"]) or {}).get("observation") or {}
        text = "".join(c.get("text", "") for c in (o.get("content") or []) if isinstance(c, dict))
        if not (o.get("is_error") or text.startswith("ERROR") or "No replacement was performed" in text):
            n += 1
    return n


def main():
    for rd in sys.argv[1:]:
        for cond_dir in sorted(p for p in Path(rd).iterdir() if p.is_dir() and not p.name.startswith("_")):
            runs = sorted(p for p in cond_dir.iterdir() if (p / "run.json").exists())
            hit = [r for r in runs if hit_step_limit(load_events(r))]
            flag_hit = sum(bool((json.loads((r / "run.json").read_text()).get("driver") or {}).get("hitStepLimit")) for r in runs)
            no_edit = [r for r in hit if not successful_edits(load_events(r)) and not (json.loads((r / "run.json").read_text()).get("patchLines"))]
            print(f"{Path(rd).name}/{cond_dir.name}: {len(runs)} runs, {len(hit)} hit the step limit "
                  f"(run.json flag says {flag_hit}), {len(no_edit)} of those never edited (empty patch)")


if __name__ == "__main__":
    main()
