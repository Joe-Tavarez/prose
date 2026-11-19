"""Step-limit analysis, step 1 of 3 (read-only). Run in the sandbox as runner:

    python3 limit_extract.py [ROUND] > limit_runs.jsonl        # ROUND = 1 (default), 2 or 3

For every run of fix-r<ROUND>-{text,roslyn,enforced} that hit the step limit (the SDK's
MaxIterationsReached event, see step_limit.py; NOT run.json's hitStepLimit), summarizes the whole run's
successful edits and the last 20 steps (tool calls, including malformed ones): edits (ok / failed),
terminal writes, builds/tests and their results, exact repeats of an earlier call, re-reads of a file
already read, rejected/malformed calls. Also prints the final patch. Then limit_combine.py, limit_cat.py.
Written 2026-11-18 for round 1 (results in SETUP_NOTES.md, "Step limit").
"""
import json, glob, os, re, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from step_limit import hit_step_limit
ROUND = sys.argv[1] if len(sys.argv) > 1 else "1"
W = 20
WRITE_RE = re.compile(r"sed\s+-i|perl\s+-pi|>\s*[\w./-]+\.(cs|csproj|props|targets|xml|json)\b|\btee\s|git\s+apply|patch\s+-p|"
                      r"open\([^)]*['\"][wa]['\"]|write_text|cat\s*<<|python3?\s+-\s*<<")
BUILD_RE = re.compile(r"\bdotnet\s+(build|test|msbuild|run)\b")
READ_RE = re.compile(r"^\s*(cat|head|tail|less|nl|sed\s+-n|awk)\b.*?([\w./-]+\.\w+)")

def text_of(obs):
    o = (obs or {}).get("observation") or {}
    c = o.get("content") or []
    return "".join(x.get("text", "") for x in c if isinstance(x, dict)), o

def build_summary(t, o):
    s = {"exit": o.get("exit_code"), "timeout": o.get("timeout")}
    m = re.findall(r"(\d+)\s+Error\(s\)", t)
    if m: s["errors"] = int(m[-1])
    cs = set(re.findall(r"error (CS\d+)", t))
    if cs: s["csCodes"] = sorted(cs)[:6]; s["csErrLines"] = len(set(re.findall(r"[^\s]+\.cs\(\d+,\d+\): error CS\d+", t)))
    m = re.findall(r"Failed:\s*(\d+),\s*Passed:\s*(\d+)", t)
    if m: s["failed"], s["passed"] = map(int, m[-1])
    if "Build succeeded" in t: s["ok"] = True
    return s

out = []
for run, cond in [(f"fix-r{ROUND}-text", "text"), (f"fix-r{ROUND}-roslyn", "roslyn"), (f"fix-r{ROUND}-enforced", "roslyn-enforced")]:
    for f in sorted(glob.glob(os.path.expanduser(f"~/ablation/runs/{run}/{cond}/*/events.jsonl"))):
        ev = [json.loads(l) for l in open(f)]
        if not hit_step_limit(ev):
            continue
        d = os.path.dirname(f)
        rec = json.load(open(d + "/run.json"))
        obs = {e.get("action_id"): e for e in ev if e.get("kind") == "ObservationEvent"}
        steps = []
        for e in ev:
            k = e.get("kind")
            if k == "AgentErrorEvent":
                steps.append({"tool": e.get("tool_name"), "sig": "AGENTERROR " + (e.get("error") or "")[:60], "err": True, "agentError": True})
            elif k == "ConversationErrorEvent" and e.get("code") != "MaxIterationsReached":
                steps.append({"tool": None, "sig": "PARSEFAIL", "err": True, "agentError": True})
            elif k == "ActionEvent":
                a = e.get("action")
                tool = e.get("tool_name")
                st = {"tool": tool}
                if not a:
                    st.update(sig=f"MALFORMED {tool}", err=True, agentError=True); steps.append(st); continue
                t, o = text_of(obs.get(e["id"]))
                st["err"] = bool(o.get("is_error"))
                ak = a.get("kind")
                if ak == "TerminalAction":
                    cmd = (a.get("command") or "").strip()
                    st["sig"] = "T " + cmd
                    st["exit"] = o.get("exit_code")
                    if WRITE_RE.search(cmd): st["write"] = True; st["writeOk"] = o.get("exit_code") == 0
                    if BUILD_RE.search(cmd): st["build"] = build_summary(t, o)
                    m = READ_RE.search(cmd)
                    if m: st["read"] = m.group(2)
                    if o.get("exit_code") not in (0, None): st["err"] = True
                elif ak == "FileEditorAction":
                    c, p = a.get("command"), a.get("path")
                    if c == "view":
                        st["sig"] = f"view {p} {a.get('view_range')}"; st["read"] = p
                    else:
                        h = hashlib.md5(json.dumps([a.get("old_str"), a.get("new_str"), a.get("file_text"), a.get("insert_line")]).encode()).hexdigest()[:8]
                        st["sig"] = f"{c} {p} {h}"; st["edit"] = p
                        failed = st["err"] or t.startswith("ERROR") or "No replacement was performed" in t or "did not appear verbatim" in t
                        st["editOk"] = not failed; st["err"] = failed
                elif ak == "MCPToolAction":
                    st["sig"] = f"M {tool} {json.dumps(a.get('data') or a.get('arguments') or {}, sort_keys=True)[:200]}"
                    m = re.search(r'"errorCount"\s*:\s*(\d+)', t) or re.search(r"(\d+)\s+errors?", t)
                    if m: st["diagErrors"] = int(m.group(1))
                elif ak == "FinishAction":
                    st["sig"] = "FINISH"; st["finishText"] = t[:200]
                else:
                    st["sig"] = f"{ak} {json.dumps(a, sort_keys=True)[:120]}"
                steps.append(st)
        seen, readseen, edited = set(), set(), set()
        for i, s in enumerate(steps):
            s["rep"] = s["sig"] in seen; seen.add(s["sig"])
            if s.get("read"): s["reread"] = s["read"] in readseen; readseen.add(s["read"])
            if s.get("edit") and s.get("editOk"): s["newFile"] = s["edit"] not in edited; edited.add(s["edit"])
        win = steps[-W:]
        okEditIdx = [i for i, s in enumerate(steps) if (s.get("edit") and s.get("editOk")) or s.get("writeOk")]
        patch = open(d + "/patch.diff", encoding="utf8", errors="replace").read() if os.path.exists(d + "/patch.diff") else ""
        out.append({
            "cond": cond, "iid": rec["instance_id"], "nsteps": len(steps),
            "patchLines": rec.get("patchLines"), "patch": patch,
            "editedFiles": sorted(edited), "lastOkEditStepsFromEnd": (len(steps) - 1 - okEditIdx[-1]) if okEditIdx else None,
            "firstOkEdit": okEditIdx[0] if okEditIdx else None,
            "win": {
                "okEdits": sum(1 for s in win if s.get("edit") and s.get("editOk")),
                "failEdits": sum(1 for s in win if s.get("edit") and not s.get("editOk")),
                "distinctOkEdits": len({s["sig"] for s in win if s.get("edit") and s.get("editOk")}),
                "termWrites": sum(1 for s in win if s.get("writeOk")),
                "newFilesEdited": sorted({s["edit"] for s in win if s.get("newFile")}),
                "repeated": sum(1 for s in win if s["rep"]),
                "rereads": sum(1 for s in win if s.get("reread")),
                "agentErrors": sum(1 for s in win if s.get("agentError")),
                "errors": sum(1 for s in win if s.get("err")),
                "builds": [s["build"] for s in win if s.get("build")],
                "diag": [s["diagErrors"] for s in win if "diagErrors" in s],
                "finish": [s.get("finishText") for s in win if s["sig"] == "FINISH"],
                "trace": [("R " if s["rep"] else "  ") + ("x " if s.get("err") else "  ") + s["sig"][:110].replace("\n", " ") for s in win],
            },
        })
for o in out:
    print(json.dumps(o))
