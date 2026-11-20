# roslyn-context scoping (2026-11-19): design and token counts only, no agent runs

Exploratory condition idea: give the agent, up front, a compact Roslyn project map of the repo at base_commit.
Nothing in the runner uses this yet.

## Pieces
- **Endpoint:** `POST /api/Analyze/overview` (RoslynAnalyzerApi branch `overview-endpoint`, 5439c84; main and the
  deployed /opt/roslyn/api are unchanged). It returns, per C# project:
  - target frameworks and project references;
  - whether it is a test project (test-framework assemblies or a *Tests name) and, for a test project, the source
    projects it tests;
  - namespaces with type counts;
  - the public types, scored by public surface plus the number of derived types. Each type has its file, base
    types, member signatures (no bodies) and member count. Types matching a priority term are always kept.

  It only declares, never binds method bodies. The two caps are maxTypesPerProject (300 here) and maxMembersPerType
  (40 here).
- **Collector:** `roslyn_context/collect_overview.py` runs in the sandbox as the runner user, with no agent. It
  uses the runner's own functions:
  - prepare_workspace (history trimmed to base_commit) and history_check;
  - the no-gold solution pick;
  - restore with the task's harness SDK.

  It then starts the branch's API on port 5060. The only task fields it gets are instance_id, repo and base_commit.
  The task text is the `<issue_description>` from the task.md the agents received.
- **Generator:** `roslyn_context/render_context.py` writes markdown capped at 3,000 tokens, counted with o200k,
  which matches gpt-oss exactly (checked against Ollama: 2,523 = 2,523 and 2,669 = 2,669).
  - **Order:** projects by how well their type and member names match the issue's terms (test projects ×0.3), then
    types round-robin over projects.
  - **Control:** `render_control` builds the file tree (directories with file counts) plus the README, with the
    same cap and term priority.
- **Evaluation only:** `roslyn_context/gold_check.py` reads the gold patch after generation to check whether its
  edited files appear (gold_check.md).

## Numbers (35 tasks)
- **Roslyn block tokens:** min 2,771 (autofac-1424), median 2,962, max 2,998 (imagesharp-2488). Every task has
  more public types than fit, so the cap binds in all 35. The uncapped endpoint response is 87 K to 7.5 M characters.
- **Control block tokens:** min 996 (stackexchangeredis-2654), median 2,956, max 2,997. 18 tasks are at 2,950 or
  more.
- **Cost:** API load median 5.1 s (max 46 s); overview call at most 11.4 s.
- **Gold files** (per task, any edited file):

  | Where | Tasks |
  |---|---|
  | Full endpoint response | 19/35 (all files: 9) |
  | 3K Roslyn block, file named | 14/35 |
  | 3K Roslyn block, same directory | 27/35 |
  | Control block, file or its directory | 27/35 |
  | Project of a gold file listed (both blocks) | 35/35 |

- **Why 57 of 127 gold .cs files are missing from the full response:**

  | Reason | Files |
  |---|---|
  | Declare no public type (internal-only; outside the "public types" design) | 37 |
  | New files | 6 |
  | Public partial type listed under its first file only | 6 |
  | Cut by the type cap | 8 |

  One of the 8 "cap" files, CoreStrings.Designer.cs, was actually dropped by the generated-file filter.
