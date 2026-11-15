"""For each sample instance, the exact .NET SDK version the SWE-Sharp-Bench harness installs in its image."""
import json, sys
from pathlib import Path
from swe_sharp_bench.constants import MAP_REPO_VERSION_TO_SPECS

sample = json.loads(Path(sys.argv[1]).read_text())
out = {}
for inst in sample:
    repo, version = inst["repo"], inst.get("version", "0.1")
    specs = MAP_REPO_VERSION_TO_SPECS.get(repo, {}).get(version)
    pull = inst.get("pull_number") or inst["instance_id"].split("-")[-1]
    if specs is None:
        out[inst["instance_id"]] = {"repo": repo, "sdk": None, "source": "not in MAP (harness derives it from GitHub)"}
        continue
    d = specs.get("dotnet", {})
    sdk = d.get(str(pull)) or d.get("default")
    out[inst["instance_id"]] = {"repo": repo, "sdk": sdk, "source": "per-PR" if d.get(str(pull)) else "repo default"}
json.dump(out, open(sys.argv[2], "w"), indent=1)
for k, v in out.items():
    print(f"{k:<48} {str(v['sdk']):<12} {v['source']}")
print("distinct:", sorted({str(v["sdk"]) for v in out.values()}))
