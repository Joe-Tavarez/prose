"""Step-limit analysis, step 3 of 3: counts each limit run's last 20 steps by category (edit, failed edit,
terminal write, build/test, Roslyn tool, read, search, exact repeat, rejected/malformed call, finish) and
adds them to DIR/limit_rows.json as "cats".

    python3 limit_cat.py DIR

The progress/looping verdicts in SETUP_NOTES.md ("Step limit") came from these counts plus reading each
run's "trace" in limit_rows.json. limit_rows.json here is the round-1 output (2026-11-18).
"""
import json,sys,re,collections
rows=json.load(open(sys.argv[1]+"/limit_rows.json"))
def cat(t):
    rep=t[0]=="R"; err=t[2]=="x"; s=t[4:]
    if s.startswith(("AGENTERROR","MALFORMED","PARSEFAIL")): return "badcall"
    if re.match(r"(str_replace|insert|create|undo_edit) ",s): return "editFail" if err else "edit"
    if s.startswith("T ") and re.search(r"sed\s+-i|perl -pi|>\s*\S+\.cs|cat\s*<<|python3? -\s*<<|apply",s): return "writeFail" if err else "write"
    if s.startswith("T ") and re.search(r"dotnet (build|test|msbuild|run)",s): return "build"
    if s.startswith("M "): return "roslynTool"
    if rep: return "repeat"
    if s.startswith("view ") or re.match(r"T\s*(cat|head|tail|sed -n|nl|awk)",s): return "read"
    if re.match(r"T\s*(grep|find|rg|ls|git (grep|log|show|diff))",s) or s.startswith("search"): return "search"
    if s=="FINISH": return "finish"
    return "other"
for x in rows:
    c=collections.Counter(cat(t) for t in x["trace"])
    x["cats"]=dict(c)
    print(f"{x['cond'][:8]:8s} {x['iid'][:38]:38s} pl={x['patchLines']!s:>4} "+" ".join(f"{k}={c[k]}" for k in ["edit","editFail","write","writeFail","build","roslynTool","read","search","repeat","badcall","finish","other"] if c[k]))
json.dump(rows,open(sys.argv[1]+"/limit_rows.json","w"),indent=1)
