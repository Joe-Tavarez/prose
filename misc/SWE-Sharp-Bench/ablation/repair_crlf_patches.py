"""Repair patch.diff files captured before the CRLF fix (run_tasks.collect_patch used text mode, which
turned every CRLF in the diff into LF, so hunks touching CRLF files no longer applied).

For each run whose patch touches a file that is CRLF at base_commit:
  1. check out base_commit in a temp clone of ~/swe-repos/_base/<instance>.git
  2. convert those files to LF (the form the stripped patch was made against) and `git apply` the patch
  3. convert them back to CRLF and take `git diff --binary` as bytes
The result has the agent's content changes against the real CRLF files. What can't be recovered is the
line-ending of lines the agent wrote (all become CRLF in CRLF files), which doesn't affect build or tests.
Original kept as patch.lf-stripped.diff; run.json gets patchRepairedCRLF. Then predictions are rebuilt.

    python3 repair_crlf_patches.py RUN_DIR
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_tasks  # noqa: E402

TASKS = {t["instance_id"]: t for t in json.loads((HERE.parent / "harness/data/tasks/sample.json").read_text())}


def g(args, cwd, inp=None):
    p = subprocess.run(["git", "-c", "core.longpaths=true", "-c", "core.autocrlf=false", *args], cwd=cwd,
                       input=inp, capture_output=True)
    if p.returncode:
        raise RuntimeError(f"git {args[:3]} failed: {p.stderr.decode(errors='replace')[-800:]}")
    return p.stdout


def repair(run_json):
    rec = json.loads(run_json.read_text())
    inst, pf = rec["instance_id"], run_json.parent / "patch.diff"
    patch = pf.read_bytes()
    if not patch or b"\r" in patch or rec.get("patchRepairedCRLF"):
        return None
    files = re.findall(rb"^diff --git a/(\S+) b/", patch, re.M)
    base, bare = TASKS[inst]["base_commit"], Path.home() / f"swe-repos/_base/{inst}.git"
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        g(["clone", "-q", "--no-checkout", str(bare), str(ws)], tmp)
        g(["checkout", "-q", "--detach", base], ws)
        crlf = [f.decode() for f in files if (ws / f.decode()).is_file() and b"\r\n" in (ws / f.decode()).read_bytes()]
        if not crlf:
            return None
        for f in crlf:
            (ws / f).write_bytes((ws / f).read_bytes().replace(b"\r\n", b"\n"))
        g(["apply", "--binary", "-"], ws, inp=patch)
        for f in crlf:
            p = ws / f
            if p.exists():
                p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        g(["add", "-A"], ws)
        fixed = g(["diff", "--cached", "--binary", base], ws)
    (run_json.parent / "patch.lf-stripped.diff").write_bytes(patch)
    pf.write_bytes(fixed)
    rec["patchRepairedCRLF"] = {"crlfFiles": crlf, "linesBefore": patch.count(b"\n"), "linesAfter": fixed.count(b"\n")}
    rec["patchLines"] = fixed.count(b"\n")
    run_tasks.write_json(run_json, rec)
    return rec["patchRepairedCRLF"]


def main():
    run_dir = Path(sys.argv[1]).expanduser()
    for cond in ("text", "roslyn"):
        for rj in sorted((run_dir / cond).glob("*/run.json")):
            r = repair(rj)
            if r:
                print(cond, rj.parent.name, r)
        # same model_name_or_path as the original predictions ("<MODEL_NAME>__<condition>")
        first = json.loads((run_dir / cond / "predictions.jsonl").read_text().splitlines()[0])
        run_tasks.MODEL_NAME = first["model_name_or_path"].removesuffix(f"__{cond}")
        run_tasks.write_predictions(run_dir, cond)


if __name__ == "__main__":
    main()
