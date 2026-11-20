"""Data files for the shared results page (the "Roslyn Ablation Results" dashboard), from final_combine.py's output.

    python3 final_dashboard_data.py RESULTS_DIR

Reads RESULTS_DIR/final_stats.json and final_runs.csv; writes RESULTS_DIR/dashboard/<dataset>.json, each
{rows, meta}. No numbers are computed here beyond regrouping and rounding; final_combine.py computes them.
"""
import csv
import json
import sys
from pathlib import Path

CONDS = [("text", "Text"), ("roslyn", "Roslyn"), ("roslyn-enforced", "Roslyn-enforced")]
OUTCOMES = [
    ("resolved", "Resolved"),
    ("empty patch", "Empty patch"),
    ("grading error", "Grading error"),
    ("no tests ran: build failure, agent's code does not compile", "Build failure: agent's code does not compile"),
    ("no tests ran: build failure, tests do not compile against the patch", "Build failure: the task's tests don't compile against the patch"),
    ("no test results: other", "No test results (other)"),
    ("regression (previously passing test fails)", "Regression: a previously passing test fails"),
    ("target tests failing", "Target tests still failing"),
]
PROCESS = [
    ("empty patches", "Empty patches"),
    ("never made a successful edit", "Never made a successful edit"),
    ("hit the 100-step limit (MaxIterationsReached)", "Hit the 100-turn limit"),
    ("2-hour timeouts", "2-hour timeouts"),
    ("invalid runs (context budget check)", "Invalid runs (context check)"),
    ("malformed tool calls (total)", "Malformed tool calls, total"),
    ("runs with >= 1 malformed tool call", "Runs with a malformed tool call"),
    ("invalid tool calls (total)", "Invalid tool calls, total"),
    ("runs with >= 1 invalid tool call", "Runs with an invalid tool call"),
    ("agent Roslyn analysis calls (total)", "Agent Roslyn analysis calls, total"),
    ("agent Roslyn analysis calls per run (median)", "Agent Roslyn analysis calls per run, median"),
    ("runs with 0 agent Roslyn analysis calls", "Runs with no agent analysis call"),
    ("agent Roslyn calls, all roslyn_* tools (total)", "Agent Roslyn calls, all tools, total"),
    ("enforced automatic Roslyn calls (total)", "Automatic Roslyn calls by the runner, total"),
    ("enforced automatic analysis calls (analyze/diagnostics)", "Automatic analysis calls, total"),
    ("Roslyn finish gate fired (runs)", "Finish gate fired (runs)"),
    ("enforced gate refusals (total)", "New-error gate refusals, total"),
    ("runs with >= 1 enforced gate refusal", "Runs refused by the new-error gate"),
    ("enforced gate: stop allowed with introduced errors", "Stopped with errors after 3 refusals"),
    ("agent minutes per run (median)", "Agent minutes per run, median"),
    ("model turns per run (median)", "Model turns per run, median"),
]


def num(v):
    return None if v in ("-", None) else v


def main():
    res = Path(sys.argv[1])
    st = json.loads((res / "final_stats.json").read_text())
    runs = list(csv.DictReader(open(res / "final_runs.csv")))
    out = res / "dashboard"
    out.mkdir(exist_ok=True)
    meta = [{"label": "Made by", "value": "prose ablation/analysis/final_combine.py, then final_dashboard_data.py"},
            {"label": "Input", "value": "the nine gpt-oss passes fix-r{1,2,3}-{text,roslyn,enforced}; 35 tasks "
                                        "(spectre-console-1303 excluded), 105 runs per condition"},
            {"label": "final_dashboard_data.py", "value": Path(__file__).read_text(), "type": "code", "lang": "python"}]

    def write(name, rows):
        (out / f"{name}.json").write_text(json.dumps({"rows": rows, "meta": meta}, indent=1))

    conds = []
    for c, label in CONDS:
        r, p = st["resolved"][c], st["proposal"][c]
        f = st["compileErrorFisher"]
        row = {"condition": c, "label": label, "runs": r["pooledN"], "resolved": r["pooled"],
               "resolvedPct": round(100 * r["pooled"] / r["pooledN"], 1),
               "r1": r["perRound"][0], "r2": r["perRound"][1], "r3": r["perRound"][2],
               "turnsMedian": p["turnsResolvedMedian"], "turnsMean": round(p["turnsResolvedMean"], 1),
               "nResolved": p["nResolved"], "nonEmpty": p["nonEmpty"], "compileErrRuns": p["withCompileErrors"],
               "compileErrPct": round(100 * p["withCompileErrors"] / p["nonEmpty"], 1),
               "compileErrRunsExclNU": p["withCompileErrorsExclNU1900"],
               "compileErrPctExclNU": round(100 * p["withCompileErrorsExclNU1900"] / p["nonEmpty"], 1),
               "fisherP": round(f[f"{c} all added errors"], 3) if c != "text" else None,
               "fisherPExclNU": round(f[f"{c} without NU1900"], 3) if c != "text" else None,
               "neverSolvedTasks": st["solveCountHistogram"][c].get("0", 0)}
        for k in ("0", "1", "2", "3"):
            row[f"solved{k}of3"] = st["solveCountHistogram"][c].get(k, 0)
        conds.append(row)
    write("conditions", conds)

    passes = []
    for c, label in CONDS:
        for k in (1, 2, 3):
            g = [x for x in runs if x["excluded"] == "False" and x["condition"] == c and x["round"] == str(k)]
            ne = [x for x in g if int(x["patchLines"]) > 0]
            ce = sum(int(x["compileErrorsAdded"]) > 0 for x in ne)
            passes.append({"pass": f"{c} r{k}", "condition": c, "label": label, "round": k, "runs": len(g),
                           "resolved": sum(x["resolved"] == "True" for x in g), "emptyPatches": len(g) - len(ne),
                           "nonEmpty": len(ne), "compileErrRuns": ce, "compileErrPct": round(100 * ce / len(ne), 1),
                           "hitStepLimit": sum(x["hitStepLimit"] == "True" for x in g)})
    write("passes", passes)

    sv = st["perTaskSolved"]
    tasks = [{"task": t, "text": sv["text"][t], "roslyn": sv["roslyn"][t], "enforced": sv["roslyn-enforced"][t],
              "total": sv["text"][t] + sv["roslyn"][t] + sv["roslyn-enforced"][t]} for t in sorted(sv["text"])]
    tasks.sort(key=lambda r: (-r["total"], r["task"]))
    write("tasks", tasks)

    tests = []
    for c, label in CONDS[1:]:
        q = st["paired"][c]
        tests.append({"id": f"{c} wilcoxon", "comparison": f"{label} vs text", "test": "Wilcoxon signed-rank, per task (pooled rounds)",
                      "better": q["better"], "worse": q["worse"], "tied": q["tied"],
                      "statistic": f"W+ {q['wilcoxonWplus']:g}, W- {q['wilcoxonWminus']:g}, n = {q['n']}", "p": round(q["wilcoxonP"], 3)})
        tests.append({"id": f"{c} sign", "comparison": f"{label} vs text", "test": "Sign test, per task (pooled rounds)",
                      "better": q["better"], "worse": q["worse"], "tied": q["tied"],
                      "statistic": f"{q['better']} better, {q['worse']} worse", "p": round(q["signP"], 3)})
        for k in (1, 2, 3):
            m = st["mcnemar"][f"{c} r{k}"]
            tests.append({"id": f"{c} mcnemar r{k}", "comparison": f"{label} vs text", "test": f"McNemar, round {k}",
                          "better": m["b"], "worse": m["c"], "tied": m["both"] + m["neither"],
                          "statistic": f"both {m['both']}, only {label} {m['b']}, only text {m['c']}, neither {m['neither']}",
                          "p": round(m["p"], 3)})
    write("tests", tests)

    write("process", [{"metric": label, "text": num(st["process"][k]["text"]), "roslyn": num(st["process"][k]["roslyn"]),
                       "enforced": num(st["process"][k]["roslyn-enforced"])} for k, label in PROCESS])
    write("outcomes", [{"outcome": label, "text": st["outcomes"]["text"].get(k, 0), "roslyn": st["outcomes"]["roslyn"].get(k, 0),
                        "enforced": st["outcomes"]["roslyn-enforced"].get(k, 0)} for k, label in OUTCOMES])

    def typed(v):
        if v in ("True", "False"):
            return v == "True"
        if v == "":
            return None
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                return v
    write("runs", [{k: typed(v) for k, v in r.items()} for r in runs])


if __name__ == "__main__":
    main()
