"""roslyn-context scoping: does the overview mention the files the gold patch edits? (evaluation only)

    python3 gold_check.py SAMPLE_JSON COLLECT_DIR RENDER_DIR

The gold patch is read here and only here, after the context blocks were generated; render_context.py and
collect_overview.py never see it. Per task and gold-edited file:
- full: the endpoint response names the file (a listed type's file, or a project's .csproj path);
- block: the 3,000-token roslyn-context markdown shows the file (same rule), and the control block (file tree +
  README) shows the file itself, its project file or its directory.
Writes RENDER_DIR/gold_check.json.
"""
import json
import re
import sys
from pathlib import Path

EXCL = "spectreconsole__spectre-console-1303"


def gold_files(patch):
    return sorted({m for m in re.findall(r"^diff --git a/(\S+) b/", patch, re.M)})


def main():
    sample = {t["instance_id"]: t for t in json.loads(Path(sys.argv[1]).read_text())}
    src, rend = Path(sys.argv[2]), Path(sys.argv[3])
    rows = []
    for f in sorted(src.glob("*.json")):
        rec = json.loads(f.read_text())
        iid = rec["instance"]
        if iid == EXCL or "error" in rec:
            continue
        files = gold_files(sample[iid]["patch"])
        projects = rec["overview"]["projects"]
        type_files = {t["file"] for p in projects for t in p["types"] if t.get("file")}
        proj_files = {p["path"] for p in projects if p.get("path")}
        md = (rend / "roslyn" / f"{iid}.md").read_text()
        ctl = (rend / "control" / f"{iid}.md").read_text()
        per = []
        for g in files:
            d = g.rsplit("/", 1)[0] if "/" in g else ""
            md_dirs = {x.rsplit("/", 1)[0] for x in re.findall(r"\(([^()\s]+\.cs)\)", md) if "/" in x}
            per.append({"file": g, "cs": g.endswith(".cs"),
                        "inFullOverview": g in type_files or g in proj_files,
                        "inRoslynBlock": f"({g})" in md or f"`{g}`" in md,
                        "dirInRoslynBlock": f"({g})" in md or f"`{g}`" in md or (bool(d) and d in md_dirs),
                        "inControlBlock": f"`{g}`" in ctl or (bool(d) and f"`{d}/`" in ctl)})
        rows.append({"instance": iid, "goldFiles": per,
                     "anyInFullOverview": any(x["inFullOverview"] for x in per),
                     "allInFullOverview": all(x["inFullOverview"] for x in per),
                     "anyInRoslynBlock": any(x["inRoslynBlock"] for x in per),
                     "allInRoslynBlock": all(x["inRoslynBlock"] for x in per),
                     "anyDirInRoslynBlock": any(x["dirInRoslynBlock"] for x in per),
                     "anyInControlBlock": any(x["inControlBlock"] for x in per)})
    (rend / "gold_check.json").write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(r["instance"], "| files", len(r["goldFiles"]), "| full any/all", r["anyInFullOverview"], r["allInFullOverview"],
              "| block any/all", r["anyInRoslynBlock"], r["allInRoslynBlock"], "| control any", r["anyInControlBlock"],
              "|", ", ".join(x["file"] for x in r["goldFiles"])[:160])
    n = len(rows)
    print(f"tasks {n}: full any {sum(r['anyInFullOverview'] for r in rows)}, full all {sum(r['allInFullOverview'] for r in rows)}, "
          f"block any {sum(r['anyInRoslynBlock'] for r in rows)}, block all {sum(r['allInRoslynBlock'] for r in rows)}, "
          f"block dir-level any {sum(r['anyDirInRoslynBlock'] for r in rows)}, "
          f"control (file or its directory) any {sum(r['anyInControlBlock'] for r in rows)}")


if __name__ == "__main__":
    main()
