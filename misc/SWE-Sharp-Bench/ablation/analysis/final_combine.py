"""Final analysis, step 2 of 2 (runs in Ubuntu with the harness venv, next to the grading logs):

    harness/.venv/bin/python final_combine.py final_runs.jsonl HARNESS_DIR OUT_DIR

Joins final_extract.py's per-run lines with the harness grading of the nine gpt-oss passes and writes
OUT_DIR/final_runs.csv (one row per run), OUT_DIR/final_results.md (tables) and OUT_DIR/final_stats.json.

- Tasks: spectreconsole__spectre-console-1303 is left out everywhere (its harness image fails even for the gold
  patch; SETUP_NOTES), so each pass has 35 graded tasks.
- Why an unresolved run failed (one primary reason per run, first that applies):
    empty patch; grading error (harness error_ids); patch did not apply;
    no tests ran: none of the task's FAIL_TO_PASS/PASS_TO_PASS tests appear in the test results, and the test log
      has compiler/MSBuild errors ("build failure"). Split by the runner's final build of the patch without the
      task's tests: agent's code does not compile (compile errors added, NU1900 left out) / tests do not compile
      against the patch. Without compiler errors in the log: "no test results: other";
    regression: a PASS_TO_PASS test failed or did not run (while other tests did);
    target tests failing: every PASS_TO_PASS test passed but a FAIL_TO_PASS test did not.
  The harness counts a test that never ran as failed; here the test log is re-parsed with the harness's own
  parser (swe_sharp_bench.log_parsers) to tell "ran and failed" from "did not run". The re-parse reproduces the
  harness's resolved verdict (checked; mismatches are reported in final_stats.json).
- Paired tests per task (35 tasks; per-task solve count 0-3 per condition): exact Wilcoxon signed-rank (zero
  differences dropped, average ranks for ties, exact null distribution by enumeration) and exact sign test;
  McNemar per round = exact binomial test on the discordant tasks. All two-sided.
"""
import contextlib
import csv
import io
import json
import math
import re
import statistics as S
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

EXCL = "spectreconsole__spectre-console-1303"
CONDS = ["text", "roslyn", "roslyn-enforced"]
MODEL = "openhands-1.16.0__gpt-oss-20b"
PASS = {"PASSED", "XFAIL"}


# ---------- exact tests ----------
def binom_two_sided(k, n):
    """Exact two-sided binomial test, p = 0.5 (sum of outcomes no more likely than k)."""
    if n == 0:
        return 1.0
    pk = [math.comb(n, i) for i in range(n + 1)]
    return min(1.0, sum(p for p in pk if p <= pk[k]) / 2 ** n)


def fisher_two_sided(a, b, c, d):
    """Exact two-sided Fisher test for [[a, b], [c, d]] (sum of tables no more likely than the observed)."""
    r1, c1, n = a + b, a + c, a + b + c + d
    p = lambda x: math.comb(c1, x) * math.comb(n - c1, r1 - x)
    obs = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, r1 + c1 - n), min(r1, c1) + 1) if p(x) <= obs * (1 + 1e-9)) / math.comb(n, r1))


def within_task_permutation(strata):
    """Exact within-task (stratified) permutation test.

    strata: one (k_b, n_b, k_a, n_a) per task: events k and runs n in condition B and in condition A. Under the null,
    condition labels are exchangeable within a task: the n_b + n_a runs of a task are relabeled with n_b B labels,
    keeping each task's run counts. The statistic T = total B events is then a sum of independent hypergeometrics,
    whose exact distribution is their convolution. Two-sided p = P(|T - E[T]| >= |t_obs - E[T]|).
    Returns (rate_b, rate_a, t_obs, expected, p, n_informative_tasks).
    """
    dist = {0: Fraction(1)}
    t_obs, kb_tot, nb_tot, ka_tot, na_tot, informative = 0, 0, 0, 0, 0, 0
    for kb, nb, ka, na in strata:
        K, N = kb + ka, nb + na
        t_obs += kb
        kb_tot, nb_tot, ka_tot, na_tot = kb_tot + kb, nb_tot + nb, ka_tot + ka, na_tot + na
        if nb == 0 or na == 0 or K == 0 or K == N:  # relabeling can't change this task's B count: a fixed shift
            dist = {s + kb: p for s, p in dist.items()}
            continue
        informative += 1
        tot = math.comb(N, nb)
        h = {x: Fraction(math.comb(K, x) * math.comb(N - K, nb - x), tot) for x in range(max(0, nb - (N - K)), min(K, nb) + 1)}
        nd = defaultdict(Fraction)
        for s, p in dist.items():
            for x, q in h.items():
                nd[s + x] += p * q
        dist = nd
    exp = sum(s * p for s, p in dist.items())
    d_obs = abs(t_obs - exp)
    p = float(sum(q for s, q in dist.items() if abs(s - exp) >= d_obs - Fraction(1, 10 ** 9)))
    return (kb_tot / nb_tot if nb_tot else None, ka_tot / na_tot if na_tot else None, t_obs, float(exp), min(1.0, p), informative)


def wilcoxon_exact(diffs):
    """Exact two-sided Wilcoxon signed-rank test. Returns (W+, W-, n_nonzero, p)."""
    d = [x for x in diffs if x != 0]
    n = len(d)
    if n == 0:
        return 0, 0, 0, 1.0
    order = sorted(range(n), key=lambda i: abs(d[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(d[order[j + 1]]) == abs(d[order[i]]):
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    r2 = [int(round(2 * r)) for r in ranks]  # doubled ranks are integers
    wplus2 = sum(r for r, x in zip(r2, d) if x > 0)
    dist = Counter({0: 1})
    for r in r2:
        nd = Counter()
        for s, c in dist.items():
            nd[s] += c
            nd[s + r] += c
        dist = nd
    total = 2 ** n
    lo = sum(c for s, c in dist.items() if s <= wplus2)
    hi = sum(c for s, c in dist.items() if s >= wplus2)
    p = min(1.0, 2 * min(lo, hi) / total)
    return wplus2 / 2, sum(r2) / 2 - wplus2 / 2, n, p


# ---------- grading ----------
def load_tasks(harness):
    return {t["instance_id"]: t for t in json.loads((harness / "data/tasks/sample.json").read_text())}


def as_list(v):
    return json.loads(v) if isinstance(v, str) else (v or [])


def classify(harness, rid, cond, iid, task, rep_ids, parser_for):
    """Returns (resolved, reason, detail dict)."""
    if iid in rep_ids["empty"]:
        return False, "empty patch", {}
    if iid in rep_ids["error"]:
        return False, "grading error", {}
    d = harness / "logs/run_evaluation" / rid / f"{MODEL}__{cond}" / iid
    rep = json.loads((d / "report.json").read_text())[iid]
    harness_resolved = bool(rep.get("resolved"))
    if not rep.get("patch_successfully_applied"):
        return harness_resolved, "patch did not apply", {"harnessResolved": harness_resolved}
    log = (d / "test_output.txt").read_text(errors="replace")
    with contextlib.redirect_stdout(io.StringIO()):  # some parsers print a summary
        status = parser_for(task["repo"])(log, None)
    f2p, p2p = as_list(task["FAIL_TO_PASS"]), as_list(task["PASS_TO_PASS"])
    ran = lambda t: t in status
    ok = lambda t: status.get(t) in PASS
    det = {
        "f2pTotal": len(f2p), "f2pPassed": sum(map(ok, f2p)), "f2pNotRun": sum(not ran(t) for t in f2p),
        "p2pTotal": len(p2p), "p2pFailedRan": sum(ran(t) and not ok(t) for t in p2p),
        "p2pNotRun": sum(not ran(t) for t in p2p),
        "testLogBuildErrors": bool(re.search(r"error CS\d+|error MSB\d+|Build FAILED", log)),
        "harnessResolved": harness_resolved,
    }
    my_resolved = all(map(ok, f2p)) and all(map(ok, p2p))
    det["reparseAgrees"] = my_resolved == harness_resolved
    if harness_resolved:
        return True, "resolved", det
    if not any(map(ran, f2p + p2p)):
        return False, ("no tests ran: build failure" if det["testLogBuildErrors"] else "no test results: other"), det
    if det["p2pFailedRan"] or det["p2pNotRun"]:
        return False, "regression (previously passing test fails)", det
    return False, "target tests failing", det


def fmt_p(p):
    return f"{p:.3f}" if p >= 0.001 else "<0.001"


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "n/a"


def main():
    runs_path, harness, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(harness))
    from swe_sharp_bench.log_parsers import MAP_REPO_TO_PARSER, parse_log_dotnet_test
    parser_for = lambda repo: MAP_REPO_TO_PARSER.get(repo, parse_log_dotnet_test)
    tasks = load_tasks(harness)

    reps = {}
    rows = []
    for line in runs_path.read_text().splitlines():
        r = json.loads(line)
        rid, cond, iid = r["runId"], r["condition"], r["instance"]
        if rid not in reps:
            rj = json.loads((harness / f"{MODEL}__{cond}.{rid}.json").read_text())
            reps[rid] = {"resolved": set(rj["resolved_ids"]), "empty": set(rj["empty_patch_ids"]),
                         "error": set(rj["error_ids"]), "unresolved": set(rj["unresolved_ids"])}
        res, reason, det = classify(harness, rid, cond, iid, tasks[iid], reps[rid], parser_for)
        assert res == (iid in reps[rid]["resolved"]), (rid, iid)
        if reason == "no tests ran: build failure":  # whose code fails to compile: the agent's, or only the tests'
            reason += (", agent's code does not compile" if r["compileErrorsAddedExclNU1900"] > 0
                       else ", tests do not compile against the patch")
        r.update(resolved=res, outcome=reason, excluded=iid == EXCL, **{k: det.get(k) for k in (
            "f2pTotal", "f2pPassed", "f2pNotRun", "p2pTotal", "p2pFailedRan", "p2pNotRun", "testLogBuildErrors",
            "reparseAgrees")})
        r["addedErrorIds"] = " ".join(r["addedErrorIds"])
        r["invalidRun"] = "; ".join(r["invalidRun"])
        rows.append(r)

    cols = ["round", "condition", "runId", "instance", "excluded", "resolved", "outcome", "modelTurns", "modelTurnsSource", "actions",
            "hitStepLimit", "timedOut", "agentMinutes", "patchLines", "patchFiles", "successfulEdits", "fileEditorEdits",
            "terminalWrites", "malformedToolCalls", "invalidToolCalls", "agentRoslynAnalysisCalls", "agentRoslynCallsAll",
            "autoRoslynCalls", "autoRoslynAnalysisCalls", "finishGateTriggered", "enforcedGateChecks",
            "enforcedGateRefusals", "enforcedGateAllowedWithIntroducedErrors", "baselineBuildErrors", "finalBuildExit",
            "compileErrorsAdded", "compileErrorsAddedExclNU1900", "addedErrorIds", "f2pTotal", "f2pPassed", "f2pNotRun",
            "p2pTotal", "p2pFailedRan", "p2pNotRun", "testLogBuildErrors", "reparseAgrees", "condensations",
            "maxPromptPlusReply", "driverStatus", "invalidRun", "runError"]
    with open(out / "final_runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["round"], CONDS.index(r["condition"]), r["instance"])):
            w.writerow(r)

    R = [r for r in rows if not r["excluded"]]
    insts = sorted({r["instance"] for r in R})
    by = defaultdict(list)
    for r in R:
        by[r["condition"]].append(r)
        by[(r["condition"], r["round"])].append(r)
    solved = {c: {i: sum(r["resolved"] for r in by[c] if r["instance"] == i) for i in insts} for c in CONDS}
    st = {"tasks": len(insts), "runs": len(R), "excludedTask": EXCL,
          "reparseDisagreements": [(r["runId"], r["instance"]) for r in R if r["reparseAgrees"] is False]}
    md = [f"# Final results: gpt-oss:20b, 3 rounds x 3 conditions ({len(insts)} tasks; {EXCL} excluded)", ""]

    # 1 resolved per pass and pooled
    md += ["## Resolved", "", "| condition | round 1 | round 2 | round 3 | pooled | mean per pass |", "|---|---|---|---|---|---|"]
    st["resolved"] = {}
    for c in CONDS:
        per = [sum(r["resolved"] for r in by[(c, k)]) for k in (1, 2, 3)]
        n = [len(by[(c, k)]) for k in (1, 2, 3)]
        st["resolved"][c] = {"perRound": per, "n": n, "pooled": sum(per), "pooledN": sum(n)}
        md.append(f"| {c} | " + " | ".join(f"{a}/{b} ({pct(a, b)})" for a, b in zip(per, n)) +
                  f" | {sum(per)}/{sum(n)} ({pct(sum(per), sum(n))}) | {S.mean(per):.2f} |")

    # 2 per-task solve counts
    md += ["", "## Per-task solve counts (0-3 of 3 rounds)", "",
           "| solved in | " + " | ".join(CONDS) + " |", "|---|---|---|---|"]
    st["solveCountHistogram"] = {c: Counter(solved[c].values()) for c in CONDS}
    for k in (0, 1, 2, 3):
        md.append(f"| {k}/3 | " + " | ".join(str(st["solveCountHistogram"][c][k]) for c in CONDS) + " |")
    md += ["", "| task | " + " | ".join(CONDS) + " |", "|---|---|---|---|"]
    for i in insts:
        if any(solved[c][i] for c in CONDS):
            md.append(f"| {i} | " + " | ".join(str(solved[c][i]) for c in CONDS) + " |")
    md.append(f"\nTasks never solved in any of the 9 passes: {sum(not any(solved[c][i] for c in CONDS) for i in insts)}/{len(insts)}.")
    st["perTaskSolved"] = solved

    # 3 paired comparisons
    md += ["", "## Paired comparisons per task (two-sided exact tests)", "",
           "| comparison | tasks better / worse / tied | Wilcoxon signed-rank W+ / W-, n | Wilcoxon p | sign test p |",
           "|---|---|---|---|---|"]
    st["paired"] = {}
    for c in ("roslyn", "roslyn-enforced"):
        diffs = [solved[c][i] - solved["text"][i] for i in insts]
        wp, wm, n, p = wilcoxon_exact(diffs)
        pos, neg = sum(x > 0 for x in diffs), sum(x < 0 for x in diffs)
        sp = binom_two_sided(min(pos, neg), pos + neg)
        st["paired"][c] = {"better": pos, "worse": neg, "tied": len(diffs) - pos - neg, "wilcoxonWplus": wp,
                           "wilcoxonWminus": wm, "n": n, "wilcoxonP": p, "signP": sp,
                           "meanDiff": S.mean(diffs)}
        md.append(f"| {c} vs text | {pos} / {neg} / {len(diffs) - pos - neg} | {wp:g} / {wm:g}, n={n} | {fmt_p(p)} | {fmt_p(sp)} |")
    md += ["", "McNemar per round (exact binomial on discordant tasks; b = only the Roslyn condition solved, c = only text solved):", "",
           "| comparison | round | both | b | c | neither | p |", "|---|---|---|---|---|---|---|"]
    st["mcnemar"] = {}
    for c in ("roslyn", "roslyn-enforced"):
        for k in (1, 2, 3):
            t = {r["instance"]: r["resolved"] for r in by[("text", k)]}
            o = {r["instance"]: r["resolved"] for r in by[(c, k)]}
            both = sum(t[i] and o[i] for i in insts)
            b = sum(o[i] and not t[i] for i in insts)
            cc = sum(t[i] and not o[i] for i in insts)
            p = binom_two_sided(min(b, cc), b + cc)
            st["mcnemar"][f"{c} r{k}"] = {"both": both, "b": b, "c": cc, "neither": len(insts) - both - b - cc, "p": p}
            md.append(f"| {c} vs text | {k} | {both} | {b} | {cc} | {len(insts) - both - b - cc} | {fmt_p(p)} |")

    # 4 proposal metrics
    md += ["", "## Proposal metrics (pooled over 3 rounds)", "",
           "| condition | % resolved | steps to resolution: model turns, median (mean; n resolved) | actions, median | "
           "non-empty patches | with compile errors added | rate | rate without NU1900 |", "|---|---|---|---|---|---|---|---|"]
    st["proposal"] = {}
    for c in CONDS:
        g = by[c]
        res = [r for r in g if r["resolved"]]
        ne = [r for r in g if r["patchLines"] > 0]
        ce = sum(r["compileErrorsAdded"] > 0 for r in ne)
        ce2 = sum(r["compileErrorsAddedExclNU1900"] > 0 for r in ne)
        turns = [r["modelTurns"] for r in res]
        st["proposal"][c] = {"resolvedPct": 100 * len(res) / len(g), "turnsResolvedMedian": S.median(turns) if turns else None,
                             "turnsResolvedMean": S.mean(turns) if turns else None, "nResolved": len(res),
                             "nonEmpty": len(ne), "withCompileErrors": ce, "withCompileErrorsExclNU1900": ce2}
        md.append(f"| {c} | {pct(len(res), len(g))} | {S.median(turns):g} ({S.mean(turns):.1f}; n={len(res)}) | "
                  f"{S.median(r['actions'] for r in res):g} | {len(ne)} | {ce} | {pct(ce, len(ne))} | {pct(ce2, len(ne))} |")
    st["compileErrorFisher"] = {}
    md += ["", "Compile-error rate vs text, exact two-sided Fisher test on pooled non-empty patches (indicative only: "
           "the runs are not independent, each task appears up to 3 times per condition):", ""]
    t = st["proposal"]["text"]
    for c in ("roslyn", "roslyn-enforced"):
        o = st["proposal"][c]
        for key, label in (("withCompileErrors", "all added errors"), ("withCompileErrorsExclNU1900", "without NU1900")):
            p = fisher_two_sided(o[key], o["nonEmpty"] - o[key], t[key], t["nonEmpty"] - t[key])
            st["compileErrorFisher"][f"{c} {label}"] = p
            md.append(f"- {c} vs text ({label}): {o[key]}/{o['nonEmpty']} vs {t[key]}/{t['nonEmpty']}, p = {fmt_p(p)}")
    # clustered test: runs of the same task are not independent, so condition labels are permuted within task
    md += ["", "## Clustered test: within-task permutation (exact)", "",
           "Runs on the same task are correlated, so here the condition labels are shuffled only within each task, keeping "
           "each task's number of runs per condition (exact null distribution by convolving one hypergeometric per task; "
           "equivalent to an exact stratified test with tasks as strata). Two-sided p = P(|T - E[T]| >= observed). Tasks "
           "where relabeling can't change anything (no events, all events, or no runs in one condition) don't contribute.", "",
           "| comparison | metric | rate (comparison) | rate (text) | observed / expected events | informative tasks | p |",
           "|---|---|---|---|---|---|---|"]
    st["clustered"] = {}
    metrics = [("resolve rate (all runs)", lambda r: True, lambda r: r["resolved"]),
               ("compile-error rate, all added errors (non-empty patches)", lambda r: r["patchLines"] > 0,
                lambda r: r["compileErrorsAdded"] > 0),
               ("compile-error rate, without NU1900 (non-empty patches)", lambda r: r["patchLines"] > 0,
                lambda r: r["compileErrorsAddedExclNU1900"] > 0)]
    for c in ("roslyn", "roslyn-enforced"):
        for name, keep, event in metrics:
            strata = []
            for i in insts:
                b = [r for r in by[c] if r["instance"] == i and keep(r)]
                a = [r for r in by["text"] if r["instance"] == i and keep(r)]
                strata.append((sum(map(event, b)), len(b), sum(map(event, a)), len(a)))
            rb, ra, t, e, p, inf = within_task_permutation(strata)
            st["clustered"][f"{c} | {name}"] = {"rateComparison": rb, "rateText": ra, "observed": t, "expected": e,
                                                "p": p, "informativeTasks": inf}
            md.append(f"| {c} vs text | {name} | {pct(rb, 1)} | {pct(ra, 1)} | {t} / {e:.1f} | {inf} | {fmt_p(p)} |")
    md += ["", "Rates here are pooled over every run that enters the test, as in the tables above. The p-values replace "
           "the indicative Fisher tests above, which treat runs as independent."]

    md += ["", "Compile-error rate per round (non-empty patches with errors added / non-empty patches):", "",
           "| condition | round 1 | round 2 | round 3 |", "|---|---|---|---|"]
    for c in CONDS:
        cells = []
        for k in (1, 2, 3):
            ne = [r for r in by[(c, k)] if r["patchLines"] > 0]
            ce = sum(r["compileErrorsAdded"] > 0 for r in ne)
            cells.append(f"{ce}/{len(ne)} ({pct(ce, len(ne))})")
        md.append(f"| {c} | " + " | ".join(cells) + " |")

    # 5 process metrics
    md += ["", "## Process metrics (pooled over 3 rounds; 105 runs per condition)", "",
           "| metric | " + " | ".join(CONDS) + " |", "|---|---|---|---|"]
    st["process"] = {}

    def line(name, f):
        vals = {c: f(by[c]) for c in CONDS}
        st["process"][name] = vals
        md.append(f"| {name} | " + " | ".join(str(vals[c]) for c in CONDS) + " |")

    cnt = lambda pred: (lambda g: sum(1 for r in g if pred(r)))
    tot = lambda key: (lambda g: sum((r[key] or 0) for r in g))
    line("empty patches", cnt(lambda r: r["patchLines"] == 0))
    line("never made a successful edit", cnt(lambda r: r["successfulEdits"] == 0))
    line("hit the 100-step limit (MaxIterationsReached)", cnt(lambda r: r["hitStepLimit"]))
    line("2-hour timeouts", cnt(lambda r: r["timedOut"]))
    line("invalid runs (context budget check)", cnt(lambda r: bool(r["invalidRun"])))
    line("malformed tool calls (total)", tot("malformedToolCalls"))
    line("runs with >= 1 malformed tool call", cnt(lambda r: r["malformedToolCalls"] > 0))
    line("invalid tool calls (total)", tot("invalidToolCalls"))
    line("runs with >= 1 invalid tool call", cnt(lambda r: r["invalidToolCalls"] > 0))
    line("agent Roslyn analysis calls (total)", tot("agentRoslynAnalysisCalls"))
    line("agent Roslyn analysis calls per run (median)", lambda g: S.median(r["agentRoslynAnalysisCalls"] for r in g))
    line("runs with 0 agent Roslyn analysis calls", cnt(lambda r: r["agentRoslynAnalysisCalls"] == 0))
    line("agent Roslyn calls, all roslyn_* tools (total)", tot("agentRoslynCallsAll"))
    line("enforced automatic Roslyn calls (total)", lambda g: sum(r["autoRoslynCalls"] or 0 for r in g) if g[0]["autoRoslynCalls"] is not None else "-")
    line("enforced automatic analysis calls (analyze/diagnostics)", lambda g: sum(r["autoRoslynAnalysisCalls"] or 0 for r in g) if g[0]["autoRoslynCalls"] is not None else "-")
    line("Roslyn finish gate fired (runs)", lambda g: sum(bool(r["finishGateTriggered"]) for r in g) if g[0]["condition"] != "text" else "-")
    line("enforced gate refusals (total)", lambda g: sum(r["enforcedGateRefusals"] or 0 for r in g) if g[0]["autoRoslynCalls"] is not None else "-")
    line("runs with >= 1 enforced gate refusal", lambda g: sum((r["enforcedGateRefusals"] or 0) > 0 for r in g) if g[0]["autoRoslynCalls"] is not None else "-")
    line("enforced gate: stop allowed with introduced errors", lambda g: sum(bool(r["enforcedGateAllowedWithIntroducedErrors"]) for r in g) if g[0]["autoRoslynCalls"] is not None else "-")
    line("agent minutes per run (median)", lambda g: S.median(r["agentMinutes"] for r in g))
    line("model turns per run (median)", lambda g: S.median(r["modelTurns"] for r in g))

    # 6 failure reasons
    reasons = ["resolved", "empty patch", "grading error", "patch did not apply",
               "no tests ran: build failure, agent's code does not compile",
               "no tests ran: build failure, tests do not compile against the patch",
               "no test results: other", "regression (previously passing test fails)", "target tests failing"]
    md += ["", "## Outcome of every run (pooled; one primary reason per unresolved run)", "",
           "| outcome | " + " | ".join(CONDS) + " |", "|---|---|---|---|"]
    st["outcomes"] = {c: Counter(r["outcome"] for r in by[c]) for c in CONDS}
    for o in reasons:
        md.append(f"| {o} | " + " | ".join(str(st["outcomes"][c][o]) for c in CONDS) + " |")
    md += ["", "Among unresolved runs with a non-empty patch that was graded: target tests failing = all previously passing "
           "tests still pass but a target test does not; regression = at least one previously passing test fails or no "
           "longer runs; no tests ran = none of the task's tests produced a result. Build failure is split by the runner's "
           "own final build of the agent's patch (without the task's tests): if it added compile errors (NU1900 left out), "
           "the agent's code does not compile; if not, only the task's tests fail to compile against the patch (typically "
           "an API the tests call was not added). No test results, other = the test log has no compiler errors but no "
           "results either (terminal-gui-3195: the target test filter matched no test; benchmarkdotnet-2304/2368: the "
           "repo's test script wrote no results file)."]
    tf = [r for r in R if r["outcome"] == "target tests failing"]
    md.append(f"Of the {len(tf)} 'target tests failing' runs, {sum((r['f2pPassed'] or 0) > 0 for r in tf)} pass some but "
              f"not all target tests.")

    (out / "final_results.md").write_text("\n".join(md) + "\n")
    (out / "final_stats.json").write_text(json.dumps(st, indent=1, default=lambda o: dict(o) if isinstance(o, Counter) else str(o)))
    print("\n".join(md))


if __name__ == "__main__":
    main()
