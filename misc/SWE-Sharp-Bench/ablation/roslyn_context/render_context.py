"""roslyn-context scoping, step 2 of 2: turn each collected overview into the markdown block the agent would get,
capped at CAP tokens (gpt-oss's tokenizer, o200k), and the same for the non-Roslyn control (file tree + README).

    ~/.local/share/uv/tools/openhands/bin/python render_context.py COLLECT_DIR OUT_DIR [CAP]

Inputs per task (collect_overview.py): the overview JSON, `git ls-files`, the root README and the issue text,
all at base_commit. Nothing else is read: no gold patch, no test patch, no later history.

Prioritization (both blocks use the same task terms, so the control is not handicapped):
  terms = code-shaped identifiers from the issue text (CamelCase, dotted, backticked, underscored) and plain words
  of 4+ letters. A symbol scores 10 for an exact code-term name, 4 for a name containing a code term, 1 per plain
  word among its CamelCase parts; member names count half. Projects are ordered by the sum over their types
  (test projects x0.3), then by public type count. Within a project, matching types first, then the endpoint's
  score (public surface + how many types derive from it).
Packing: fixed header, then items in priority order until the cap; the result is counted exactly and trimmed from
the end if the line-by-line estimate overshot.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")  # gpt-oss's o200k_harmony = o200k_base + chat special tokens
EXCL = "spectreconsole__spectre-console-1303"


def ntok(s):
    return len(ENC.encode(s))


def camel_parts(name):
    return [p.lower() for p in re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", name)]


def member_name(sig):
    m = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:<[^()]*>)?\s*\(", sig) or re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:\{|$)", sig)
    return m.group(1) if m else sig


class Scorer:
    def __init__(self, code, words):
        self.code = {c.lower() for c in code}
        self.words = {w.lower() for w in words}

    def name(self, n):
        base = re.sub(r"<.*", "", n.split(".")[-1]).lower()
        s = 10 if base in self.code else (4 if any(c in base for c in self.code if len(c) >= 4) else 0)
        return s + sum(1 for p in camel_parts(n.split(".")[-1]) if p in self.words)

    def type(self, t):
        return self.name(t["name"]) + 0.5 * sum(self.name(member_name(m)) for m in t["members"])


class Packer:
    """Adds lines in order while the running count stays under the cap; then trims exactly."""
    def __init__(self, cap):
        self.cap, self.lines, self.used = cap, [], 0

    def add(self, line, force=False):
        n = ntok(line + "\n")
        if not force and self.used + n > self.cap:
            return False
        self.lines.append(line)
        self.used += n
        return True

    def text(self):
        while self.lines and ntok("\n".join(self.lines) + "\n") > self.cap:
            self.lines.pop()
        return "\n".join(self.lines) + "\n"


def render_roslyn(rec, cap):
    o, sc = rec["overview"], Scorer(rec["codeTerms"], rec["wordTerms"])
    projects = o["projects"]
    for p in projects:
        p["_types"] = sorted(p["types"], key=lambda t: (-sc.type(t), -(min(t["memberCount"], 50) + 3 * t["derivedCount"]), t["name"]))
        p["_score"] = sum(sc.type(t) for t in p["types"]) * (0.3 if p["isTestProject"] else 1)
    order = sorted(projects, key=lambda p: (-p["_score"], p["isTestProject"], -p["publicTypeCount"], p["name"]))
    k = Packer(cap)
    k.add("## Repository map (from Roslyn, at the starting commit; declarations only)", True)
    k.add(f"Solution `{rec['solution']}`, .NET SDK {rec['sdk']}, {len(projects)} C# projects "
          f"({sum(p['isTestProject'] for p in projects)} test). Projects are listed most relevant to the issue first.", True)
    k.add("", True)
    k.add("### Projects", True)
    listed = 0
    for i, p in enumerate(order):
        tf = ", ".join(p["targetFrameworks"]) or "?"
        if p["isTestProject"]:
            line = f"- {p['name']} (`{p['path']}`; {tf}) — tests {', '.join(p['testedProjects']) or '—'}"
        else:
            refs = ", ".join(p["projectReferences"]) or "no project refs"
            ns = ", ".join(n["name"] for n in p["namespaces"][:3])
            line = f"- **{p['name']}** (`{p['path']}`; {tf}) → {refs}; {p['publicTypeCount']} public types; ns {ns}"
        # the project list may take at most 40% of the cap; the rest is named compactly
        if k.used + ntok(line + "\n") > 0.4 * cap or not k.add(line):
            rest = [q["name"] for q in order[i:]]
            k.add(f"- … {len(rest)} more: " + ", ".join(rest), True) if ntok(", ".join(rest)) < 0.1 * cap else \
                k.add(f"- … {len(rest)} more projects (not listed)", True)
            break
        listed += 1
    # types: round-robin over the projects in priority order, so the top project can't take the whole budget
    k.add("", True)
    k.add("### Key public types (members abbreviated)", True)
    queues = [(p, list(p["_types"])) for p in order if not p["isTestProject"] and p["_types"]]
    shown = Counter()
    full = False
    while queues and not full:
        for p, q in list(queues):
            if not q:
                queues.remove((p, q))
                continue
            t = q.pop(0)
            base = f" : {', '.join(t['baseTypes'][:3])}" if t["baseTypes"] else ""
            n_members = 8 if sc.type(t) > 0 else 4
            mem = "; ".join(t["members"][:n_members]) + (f"; … +{t['memberCount'] - n_members}" if t["memberCount"] > n_members else "")
            head = f"- {p['name']}: `{t['kind']} {t['name']}{base}` ({t['file']})"
            if not k.add(head + (f"\n  {mem}" if mem else "")):
                full = True
                break
            shown[p["name"]] += 1
    return k.text(), {"projects": len(projects), "projectsListed": listed, "typesShown": sum(shown.values()),
                      "typesAvailable": sum(len(p["types"]) for p in projects if not p["isTestProject"]),
                      "topProjects": [p["name"] for p in order[:3]]}


def render_control(rec, cap):
    """Non-Roslyn control: directory tree (file counts) + README, same cap and term priority."""
    sc = Scorer(rec["codeTerms"], rec["wordTerms"])
    files = [f for f in rec["files"] if not re.search(r"(^|/)(\.git|bin|obj|node_modules)/", f)]
    dirs = Counter()
    for f in files:
        parts = f.split("/")[:-1]
        for d in range(1, min(len(parts), 3) + 1):
            dirs["/".join(parts[:d])] += 1
    cs = Counter("/".join(f.split("/")[:-1][:3]) for f in files if f.endswith(".cs"))
    projs = sorted(f for f in files if f.endswith(".csproj"))
    k = Packer(cap)
    k.add("## Repository overview (file tree and README, at the starting commit)", True)
    k.add(f"{len(files)} tracked files, {sum(1 for f in files if f.endswith('.cs'))} .cs files, {len(projs)} .csproj files.", True)
    k.add("", True)
    k.add("### Project files", True)
    proj_lines = [f"- `{p}`" for p in sorted(projs, key=lambda p: (-sc.name(Path(p).stem.replace('.', '')), p))]
    for i, line in enumerate(proj_lines):
        if k.used + ntok(line + "\n") > 0.3 * cap or not k.add(line):
            k.add(f"- … {len(proj_lines) - i} more", True)
            break
    k.add("", True)
    k.add("### Directories (files; .cs files), most relevant first", True)
    score = lambda d: sum(sc.name(seg) for seg in re.split(r"[/._-]", d) if seg)
    tree = sorted(dirs, key=lambda d: (-score(d), d.count("/"), -dirs[d], d))
    budget_tree = 0.65 * cap
    for d in tree:
        if k.used > budget_tree or not k.add(f"- `{d}/` ({dirs[d]}; {cs.get(d, 0)} .cs)"):
            break
    if rec.get("readme"):
        k.add("", True)
        k.add(f"### {rec['readmeName']} (start)", True)
        readme = re.sub(r"<[^>]+>|!\[[^\]]*\]\([^)]*\)|\[!\[.*?\]\(.*?\)\]\(.*?\)", "", rec["readme"])  # badges/images/HTML
        for line in [l.rstrip() for l in readme.splitlines()]:
            if line and not k.add(line):
                break
    return k.text(), {"files": len(files), "csproj": len(projs)}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    (out / "roslyn").mkdir(parents=True, exist_ok=True)
    (out / "control").mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(src.glob("*.json")):
        if f.name.endswith(".calls.jsonl"):
            continue
        rec = json.loads(f.read_text())
        iid = rec["instance"]
        if iid == EXCL:
            continue
        row = {"instance": iid}
        if "error" in rec:
            row["error"] = rec["error"][:300]
            rows.append(row)
            continue
        rmd, rinfo = render_roslyn(rec, cap)
        cmd, cinfo = render_control(rec, cap)
        (out / "roslyn" / f"{iid}.md").write_text(rmd)
        (out / "control" / f"{iid}.md").write_text(cmd)
        o = rec["overview"]
        row.update(roslynTokens=ntok(rmd), controlTokens=ntok(cmd), **rinfo,
                   uncappedOverviewChars=len(json.dumps(o)), loadSeconds=rec.get("loadSeconds"),
                   overviewSeconds=rec.get("overviewSeconds"), codeTerms=len(rec["codeTerms"]), wordTerms=len(rec["wordTerms"]),
                   healthWarnings=len((rec.get("health") or {}).get("warnings") or []), **{f"control_{k}": v for k, v in cinfo.items()})
        rows.append(row)
    (out / "tokens.json").write_text(json.dumps(rows, indent=1))
    ok = [r for r in rows if "error" not in r]
    print(f"{len(ok)} rendered, {len(rows) - len(ok)} errors")
    for r in rows:
        print(r["instance"], r.get("roslynTokens"), r.get("controlTokens"), r.get("typesShown"), r.get("typesAvailable"), r.get("error", "")[:120])


if __name__ == "__main__":
    main()
