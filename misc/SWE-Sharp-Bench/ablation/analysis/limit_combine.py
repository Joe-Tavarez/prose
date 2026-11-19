"""Step-limit analysis, step 2 of 3 (read-only except DIR/limit_rows.json). Run in Ubuntu (needs the harness):

    python3 limit_combine.py DIR [ROUND]      # DIR holds limit_runs.jsonl from limit_extract.py

Joins each limit run with its gold patch (same files, overlapping hunks, share of the gold's added lines
present) and its harness grading (patch applied, FAIL_TO_PASS passed, PASS_TO_PASS broken). Writes
DIR/limit_rows.json and prints one line per run.
"""
import json, re, glob, sys, ast
S = sys.argv[1]
ROUND = sys.argv[2] if len(sys.argv) > 2 else "1"
H = "/mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness"
gold = {t["instance_id"]: t for t in json.load(open(f"{H}/data/tasks/sample.json"))}
RID = {"text": f"fix-r{ROUND}-text", "roslyn": f"fix-r{ROUND}-roslyn", "roslyn-enforced": f"fix-r{ROUND}-enforced"}

def parse(patch):
    files, cur = {}, None
    for l in patch.splitlines():
        m = re.match(r"diff --git a/(\S+) b/", l)
        if m: cur = m.group(1); files[cur] = {"hunks": [], "add": [], "rem": []}; continue
        m = re.match(r"@@ -(\d+)(?:,(\d+))? ", l)
        if m and cur: a = int(m.group(1)); files[cur]["hunks"].append((a, a + int(m.group(2) or 1))); continue
        if cur and l.startswith("+") and not l.startswith("+++"): files[cur]["add"].append(l[1:].strip())
        if cur and l.startswith("-") and not l.startswith("---"): files[cur]["rem"].append(l[1:].strip())
    return files

def norm(lines): return {re.sub(r"\s+", "", x) for x in lines if len(x.strip()) > 3 and x.strip() not in ("{", "}", "};")}

rows = []
for line in open(f"{S}/limit_runs.jsonl"):
    r = json.loads(line)
    g = parse(gold[r["iid"]]["patch"]); a = parse(r["patch"])
    gsrc = {f for f in g}
    edited = {re.sub(r"^/srv/ablation/work/[^/]+/", "", p) for p in r["editedFiles"]}
    sameFiles = sorted(gsrc & set(a))
    touchedGoldEver = sorted(gsrc & edited)
    hunkOverlap = any(abs(ga - aa) < 25 or (aa <= gb and ga <= ab) for f in sameFiles for ga, gb in g[f]["hunks"] for aa, ab in a[f]["hunks"])
    gadd = set().union(*[norm(g[f]["add"]) for f in g]) if g else set()
    aadd = set().union(*[norm(a[f]["add"]) for f in a]) if a else set()
    addCover = len(gadd & aadd) / len(gadd) if gadd else None
    lit = lambda v: v if isinstance(v, list) else ast.literal_eval(v); f2p = lit(gold[r["iid"]]["FAIL_TO_PASS"]); p2p = lit(gold[r["iid"]]["PASS_TO_PASS"])
    rep = glob.glob(f"{H}/logs/run_evaluation/{RID[r['cond']]}/*/{r['iid']}/report.json")
    ts = None
    if rep:
        x = json.load(open(rep[0]))[r["iid"]]
        t = x.get("tests_status") or {}
        ts = {"applied": x.get("patch_successfully_applied"), "resolved": x.get("resolved"),
              "f2pOk": len((t.get("FAIL_TO_PASS") or {}).get("success", [])), "f2p": len(f2p),
              "p2pFail": len((t.get("PASS_TO_PASS") or {}).get("failure", [])), "p2pOk": len((t.get("PASS_TO_PASS") or {}).get("success", [])), "p2p": len(p2p)}
    rows.append({**{k: r[k] for k in ("cond", "iid", "nsteps", "patchLines", "lastOkEditStepsFromEnd", "firstOkEdit")},
                 "w": {k: v for k, v in r["win"].items() if k != "trace"}, "trace": r["win"]["trace"],
                 "goldFiles": sorted(gsrc), "patchFiles": sorted(a), "sameFiles": sameFiles, "touchedGoldEver": touchedGoldEver,
                 "hunkOverlap": hunkOverlap, "goldAddCover": addCover, "goldAddN": len(gadd), "tests": ts})
json.dump(rows, open(f"{S}/limit_rows.json", "w"), indent=1)
for x in rows:
    w = x["w"]; t = x["tests"] or {}
    print(f"{x['cond'][:8]:8s} {x['iid'][:40]:40s} pl={x['patchLines']!s:>4} okE={w['okEdits']} distE={w['distinctOkEdits']} failE={w['failEdits']} tw={w['termWrites']} "
          f"newF={len(w['newFilesEdited'])} rep={w['repeated']:2d} rer={w['rereads']:2d} aerr={w['agentErrors']} err={w['errors']:2d} "
          f"lastE={x['lastOkEditStepsFromEnd']!s:>4} builds={len(w['builds'])} | gold={len(x['goldFiles'])} same={len(x['sameFiles'])} ever={len(x['touchedGoldEver'])} "
          f"hunk={'Y' if x['hunkOverlap'] else '-'} cover={'' if x['goldAddCover'] is None else round(x['goldAddCover'],2)} "
          f"f2p={t.get('f2pOk','')}/{t.get('f2p','')} p2pFail={t.get('p2pFail','')}")
