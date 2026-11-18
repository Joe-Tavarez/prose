#!/bin/bash
# Redo of fix-r1-roslyn / sixlabors__imagesharp-2298 (user decision 2026-11-18). Its first attempt (2026-11-18
# 03:26) was refused before the agent started because mirror.json was briefly missing (see SETUP_NOTES.md,
# "Mirror check retry"). Waits for the whole re-run (~/ablation/fixbatch/all.done), moves the refused record
# to runs/fix-r1-roslyn/_sandbox_refused/, then resumes fix-r1-roslyn with the identical command: the other
# 35 runs are skipped, and run_tasks.py exits if any setting differs from the pass's config.json.
# Writes ~/ablation/fixbatch/fix-r1-roslyn-redo.done (the Windows grader waits for it) or REDO_FAILED.
# Safe to re-run after a restart.
F=~/ablation/fixbatch
RUN=fix-r1-roslyn; COND=roslyn; IID=sixlabors__imagesharp-2298
D=~/ablation/runs/$RUN/$COND/$IID
L=~/ablation/$RUN.log
cd ~/ablation/runner || exit 1
[ -f $F/$RUN-redo.done ] && { echo "already done"; exit 0; }
until [ -f $F/all.done ]; do
  [ -f $F/PAUSED ] && { echo "batch paused; redo waits"; }
  sleep 120
done
if [ -f $D/run.json ] && python3 -c "import json,sys; r=json.load(open(sys.argv[1])); sys.exit(0 if 'mirror not running' in (r.get('error') or '') else 1)" $D/run.json; then
  mkdir -p ~/ablation/runs/$RUN/_sandbox_refused
  mv $D ~/ablation/runs/$RUN/_sandbox_refused/$IID-$(date +%Y%m%d-%H%M%S)
fi
echo "=== redo $IID (refused 2026-11-18 03:26: mirror.json missing) start $(date -Is) ===" >> $L
python3 run_tasks.py --run-id $RUN --conditions $COND --openhands ~/ablation/openhands-gpt-oss-20b-ctx48k >> $L 2>&1
rc=$?
echo "=== redo exit $rc $(date -Is) ===" >> $L
res=$(python3 - "$D/run.json" <<'EOF'
import json, sys, glob, os
try: r = json.load(open(sys.argv[1]))
except Exception as ex: print(f"no run.json ({ex})"); sys.exit()
n = len(glob.glob(os.path.dirname(os.path.dirname(sys.argv[1])) + "/*/run.json"))
bad = r.get("invalid") or ("refused: " + r["error"][:150] if "sandbox check failed" in (r.get("error") or "") or "Ollama" in (r.get("error") or "") else "")
print(f"{n} runs; {r['instance_id']}: {'BAD ' + str(bad) if bad else 'valid'}, timedOut {r.get('timedOut')}, error {(r.get('error') or '')[:80]!r}")
EOF
)
if [ $rc -eq 0 ] && [[ "$res" == "36 runs;"*valid* ]] && [[ "$res" != *BAD* ]]; then
  echo "$(date -Is) $RUN redo of $IID done: $res" >> $F/status.log
  date -Is > $F/$RUN-redo.done
else
  echo "$(date -Is) $RUN redo of $IID FAILED (exit $rc): $res" | tee -a $F/status.log > $F/REDO_FAILED
  exit 1
fi
