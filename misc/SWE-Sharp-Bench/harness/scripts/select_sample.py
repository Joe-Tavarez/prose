"""Pick a repo-stratified sample of SWE-Sharp-Bench instances for the ablation.

Every repo gets at least one instance; the rest of the budget is split in proportion to each
repo's share of the dataset (largest remainder). Instances within a repo are drawn with a fixed
seed, so the sample is reproducible.

    python scripts/select_sample.py --size 36 --exclude-file data/tasks/gold_failures.txt
"""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def allocate(counts: dict[str, int], size: int) -> dict[str, int]:
    if size < len(counts):
        raise ValueError(f"size {size} is smaller than the number of repos ({len(counts)})")
    alloc = {repo: 1 for repo in counts}
    remaining = size - len(counts)
    spare = {repo: n - 1 for repo, n in counts.items()}
    total_spare = sum(spare.values())
    quotas = {repo: remaining * s / total_spare for repo, s in spare.items()}
    for repo, q in quotas.items():
        alloc[repo] += min(int(q), spare[repo])
    leftover = size - sum(alloc.values())
    by_remainder = sorted(counts, key=lambda r: (quotas[r] - int(quotas[r]), counts[r]), reverse=True)
    for repo in by_remainder:
        if leftover == 0:
            break
        if alloc[repo] < counts[repo]:
            alloc[repo] += 1
            leftover -= 1
    return alloc


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", default="data/tasks/swe-sharp-bench.json")
    parser.add_argument("--size", type=int, default=36)
    parser.add_argument("--seed", type=int, default=755)
    parser.add_argument("--exclude-file", help="Instance ids (one per line) to leave out, e.g. gold-patch failures")
    parser.add_argument("--out", default="data/tasks/sample")
    args = parser.parse_args()

    instances = json.loads(Path(args.dataset).read_text())
    excluded = set()
    if args.exclude_file and Path(args.exclude_file).exists():
        excluded = {line.strip() for line in Path(args.exclude_file).read_text().splitlines() if line.strip()}

    by_repo = defaultdict(list)
    for inst in instances:
        if inst["instance_id"] not in excluded:
            by_repo[inst["repo"]].append(inst)

    alloc = allocate({repo: len(v) for repo, v in by_repo.items()}, args.size)
    rng = random.Random(args.seed)
    sample = []
    for repo in sorted(by_repo):
        pool = sorted(by_repo[repo], key=lambda i: i["instance_id"])
        sample.extend(rng.sample(pool, alloc[repo]))
    sample.sort(key=lambda i: i["instance_id"])

    out = Path(args.out)
    out.with_suffix(".json").write_text(json.dumps(sample, indent=2))
    out.with_suffix(".txt").write_text("".join(i["instance_id"] + "\n" for i in sample))

    print(f"{len(sample)} instances from {len(by_repo)} repos (seed {args.seed}, {len(excluded)} excluded)")
    for repo in sorted(alloc, key=lambda r: -alloc[r]):
        print(f"  {alloc[repo]:>2} / {len(by_repo[repo]):>2}  {repo}")


if __name__ == "__main__":
    main()
