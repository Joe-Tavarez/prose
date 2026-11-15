# Roslyn ablation — machine setup (2026-11-14)

## Repos
Repos live on the Windows drive at C:\Repos (= /mnt/c/Repos in WSL); moved there from ~/repos on 2026-11-14.
`git config core.filemode false` is set in prose (NTFS exec bits).
- /mnt/c/Repos/prose @ harness-fixes (4880d14a)
- /mnt/c/Repos/RoslynAnalyzerApi @ main. Cloned by the user with a Windows git (CRLF working tree);
  `git config core.autocrlf true` set so WSL git doesn't report every file modified.
  - 9a821cd (pushed): loadcheck --bench-csv/--results-dir/--api-dll + results-win/ + results-wsl/
  - bf8f6de (pushed 2026-11-15): API ignores 0-document projects (see Methods notes)
- /mnt/c/Repos/prose @ harness-fixes also holds this file and the runner: misc/SWE-Sharp-Bench/ablation/.
  ~/ablation/runner, ~/ablation/SETUP_NOTES.md and ~/ablation/gen_settings.py are symlinks into that folder.
  Commit prose with the WSL git (the Windows git's autocrlf=true shows 3 data JSON files as modified; they aren't),
  push with the Windows git (credentials).
  - Commit with the Windows git (C:\Program Files\Git\cmd\git.exe); it holds the GitHub credentials.

## Methods notes
- **Roslyn servers run in WSL** (decided 2026-11-14), same paths as the agent, no PathMap. Linux also matches the
  harness's grading environment. Consequence: .NET Framework (net4xx) target frameworks don't load (e.g. Polly
  38 vs 44 projects); only modern TFMs are analyzable, which are also the only ones the Linux harness builds.
- **0-document projects are ignored** (RoslynAnalyzerApi bf8f6de). After loading, every C# project with 0 documents
  is removed from the solution snapshot, together with its MSBuild "does not contain 'Compile' target" failures.
  Cause: serilog's `<TargetFrameworks>$(TargetFrameworks);net8.0;...` starts with ';' on Linux (the Windows-only
  prefix is empty), which MSBuildWorkspace loads as an extra TFM-less project with no documents. Without the fix,
  roslyn_health reports "Project 'Serilog' loaded with 0 documents — project evaluation likely failed" in all 3
  serilog sample tasks, and AGENTS.md tells the agent to distrust answers there, although every real serilog project
  loaded (net8.0 compiles with 0 errors). Only the Roslyn condition is affected (the text condition never sees
  /health). Trade-off: a project that genuinely failed to evaluate and has 0 documents is now hidden from
  /health too; it is logged by the API ("Ignoring project ..."), and its other workspace diagnostics are kept.
  Response shapes are unchanged, so agent/AGENTS.md (the treatment text) is unchanged.
  Regression test: WorkspaceSetupTests.Empty_target_framework_entry_does_not_leave_an_empty_project.
  Residual: serilog still reports 4 workspace diagnostics ("Found project reference without a matching metadata
  reference" to Serilog.csproj / TestDummies.csproj); 2 phantom Serilog.Tests x 2 references = 4, and Windows has
  none, so they very likely come from the same phantom evaluations, but the message doesn't name the referencing
  project, so they are left in. /health `warnings` is empty.
- **Agent environment uses the harness's exact SDK per task.** The harness image installs one exact SDK
  (MAP_REPO_VERSION_TO_SPECS default or per-PR override; harness_sdk.py -> runner/harness_sdk.json; 15 versions
  for the sample, 6.0.100 ... 9.0.100-rc.2). Each lives in an isolated root ~/.dotnet-sdks/<version> with the same
  extra .NET/ASP.NET Core 6.0 + 7.0 runtimes as the image (install_sdks.sh). The runner's restore/build and the
  agent's process (so its terminal) get only that root on PATH; ~/.bashrc only adds ~/.dotnet when DOTNET_ROOT is
  unset. With roll-forward to the newest installed SDK instead, 5 of 36 baselines failed to compile (newer
  analyzers/compiler: CA2022, CS8170, CS8629...); with the harness SDKs, 2 do. The Roslyn API itself still runs on
  ~/.dotnet with MSBuild from SDK 8 (by design: MSBuildSetup loads the MSBuild matching its runtime).
- **Baseline compile errors (environment, not the agent):** efcore-27428 (RS2003 in EFCore.Analyzers) and
  csvhelper-2132 (CS0104 ambiguous ConfigurationException), both on the harness SDK. The compile-error metric must
  count NEW errors: final-build errors minus the same task's baseline errors (compare id + file + message, not line).
- **Files changed by setup are excluded from patches.** restore/build rewrite 3 tracked template.json files in
  BenchmarkDotNet-2368 (version stamping). The runner records files dirty after setup (restore + baseline build)
  and leaves them out of the predicted patch, in both conditions. The baseline build is part of setup in both
  conditions, so both start from the same built state.
- **Avalonia-14013:** Avalonia.Desktop.slnf lists src/Windows/Avalonia.Win32.Interop, which is not in Avalonia.sln
  at that commit (MSB5028). The runner writes Avalonia.Desktop.ablation.slnf without it (repo root, git-excluded)
  and uses it for the prepare build and the Roslyn API, in both conditions.
- **Roslyn-condition-only /health warnings that remain** (pre-existing load-check PARTIALs, not fixed): efcore x2
  ("EFCore.Sqlite"/"EFCore.Tools" have no metadata references), csvhelper ("_build" unrestored), MessagePack x3
  ("MessagePack(netstandard2.0/2.1)" unrestored). 6 of 36 tasks.
- API test suite: 42/42 on Windows; 41/42 on Linux. The one Linux failure (LoadTimeoutTests) is the test, not the
  API: it blocks the build with `ping -n 120 ... > nul`, which exits at once on Linux. With `sleep 120` the timeout,
  build-host kill and recovery all pass on Linux. Fails the same way before bf8f6de.

## Roslyn condition
- .NET SDKs 6.0.428, 7.0.410, 8.0.428, 9.0.321, 10.0.404 installed in BOTH:
  WSL ~/.dotnet (exports in ~/.bashrc; needs libicu78), Windows %LOCALAPPDATA%\Microsoft\dotnet (user PATH + DOTNET_ROOT).
- API builds: Windows in C:\Repos\RoslynAnalyzerApi\bin; WSL from its own clone ~/build/RoslynAnalyzerApi (separate bin/obj).
- Load check results (committed in 9a821cd): loadcheck/results-win, loadcheck/results-wsl (WSL run predates bf8f6de).
  Windows == original results exactly (17/17). WSL: same except .NET Framework TFMs (net4xx) are absent on Linux
  (Polly 38 vs 44 projects, BenchmarkDotNet, MessagePack) and serilog shows PARTIAL only because its csproj
  TargetFrameworks starts with ';' on Linux -> two empty phantom projects 'Serilog'/'Serilog.Tests' (0 docs);
  all real serilog TFM projects load and net8.0 compiles with 0 errors.
- Clones: Windows C:\swe-repos, WSL ~/swe-repos.
- Flow per task: API on :5050 loads the task solution (`--solution ... --Roslyn:RestoreOnLoad true --Roslyn:RunId <id>`),
  MCP wrapper on :5051 (`/mcp`, Streamable HTTP), roslyn/mcp.json -> {"mcpServers":{"roslyn":{"url":"http://localhost:5051/mcp"}}}.
  PathMap only needed if API and agent see the repo under different paths (Windows API + WSL agent).
- agent/AGENTS.md (frozen copy) goes in the task repo root: OpenHands SDK 1.21 loads root AGENTS.md / CLAUDE.md /
  .cursorrules as always-on skills (openhands/sdk/skills/skill.py load_project_skills). Add it to .git/info/exclude
  so it never ends up in the predicted patch. Check if a target repo already ships AGENTS.md at base_commit.

## Harness
- venv: /mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness/.venv (uv, CPython 3.12.16; swebench==3.0.0)
- dataset: harness/data/tasks/swe-sharp-bench.json (150 instances, 17 repos)
- sample: harness/data/tasks/sample.{json,txt} — 36 instances, 17 repos, seed 755, no exclusions
- images are built locally: pass `--namespace ""` to swe_sharp_bench.cli (default `swebcs` is not a published registry)

- gold validation (run_id validate-gold): ardalis__cleanarchitecture-546 and serilog__serilog-1906 both resolved

## OpenHands
- `uv tool install --python 3.12 openhands==1.16.0` (CLI; pins openhands-sdk/tools 1.21.0, litellm 1.109.1)
- One persistence dir per condition, selected with OPENHANDS_PERSISTENCE_DIR:
  - ~/ablation/openhands/text    — mcp.json = {"mcpServers": {}}
  - ~/ablation/openhands/roslyn  — mcp.json = Roslyn MCP server (TODO once repo is cloned)
- agent_settings.json is byte-identical in both (regenerate with gen_settings.py):
  model openai/qwen3.5:9b, base_url http://localhost:11434/v1, api_key "ollama",
  temperature 0.0, max_input_tokens 65536, max_output_tokens 8192, native tool calling,
  LLMSummarizingCondenser (max_size 240, same LLM). Critic disabled (and inactive off the All-Hands proxy).
- Run: `OPENHANDS_PERSISTENCE_DIR=~/ablation/openhands/<cond> openhands --headless --json -f task.md`
  from inside the task's repo checkout (do NOT pass --override-with-envs; settings come from the file).
- Ollama context (65536) is set server-side; the OpenAI endpoint ignores num_ctx. Verify with `curl localhost:11434/api/ps`.

## Per-task runner (prose: misc/SWE-Sharp-Bench/ablation/; ~/ablation/runner links there)
- `run_tasks.py` (run with ~/ablation/loadcheck-venv/bin/python) + `oh_driver.py` (runs with the OpenHands tool python).
- Dry run: `python run_tasks.py --run-id dry-36b --dry-run` -> ~/ablation/runs/<run-id>/summary.md
  (dry-36b, 2026-11-15: 72/72 set up, agent shell SDK == harness SDK 72/72, Roslyn MCP 7 tools + ready, no patch
  without an agent; remaining flags = the baseline errors and Roslyn /health warnings listed in Methods notes)
- Real run (NOT yet done): `python run_tasks.py --run-id <id> --conditions text roslyn`
  (baseline + final `dotnet build` always run; --no-build-check skips both)
- Same in both conditions: fresh checkout from ~/swe-repos cache (origin reset to GitHub), REPO_SETUP prepare steps,
  `dotnet restore -p:NuGetAudit=false`, prompt (OpenHands SWE-bench style, no hints_text), agent settings, limits.
  Roslyn only: AGENTS.md at repo root (git-excluded), API :5050 + MCP :5051 started and checked; servers killed after.
- Agent: oh_driver.py builds the agent with the CLI's load_agent_specs and runs an SDK Conversation (LLM security
  analyzer, NeverConfirm, hooks, builtin subagents, like `--headless`) with an explicit step limit, because the CLI
  has no option for it and always uses the SDK default of 500.
- **Limits (decided 2026-11-15):** 100 steps (--max-steps) is what should end a run. Wall clock 120 min
  (--timeout-minutes) is a safety net only: local qwen3.5:9b at 64K context can take 20–40 s per step, and a tight
  clock would cut the Roslyn condition more (server startup, slower tool calls). On timeout the driver's whole
  process group is killed; run.json has timedOut=true (steps then counted from events.jsonl as stepsFromEvents)
  and summary.md lists every timed-out run. Report timeouts per condition.
- **Public skills disabled in both conditions (decided 2026-11-15).** The CLI's AgentStore._build_agent_context
  sets load_public_skills=True (clones github.com/OpenHands/extensions HEAD, ~73 skills in the prompt). oh_driver.py
  replaces that method with a copy that only sets load_public_skills=False. Result: text condition skills = [],
  roslyn condition = ["agents"] (AGENTS.md); the extensions repo is not fetched. Dry-run checks enforce both.
- Solution choice: --solution-policy no-gold (default) ranks by name match + size, so the gold patch can't influence
  setup; run.json records whether loadcheck's gold-aware pick would differ.
- Outputs per task: task.md, run.json, driver(.json|-dry.json), events.jsonl, patch.diff, roslyn-calls.jsonl,
  roslyn-api.log, roslyn-mcp.log; per condition: predictions.jsonl (model_name_or_path
  openhands-1.16.0__qwen3.5-9b__<condition>) for `swe_sharp_bench.cli --predictions_path`.
- Steps = ActionEvents in the conversation (driver.json `actions`, per-tool counts in `toolCalls`).
  Compile errors (decided 2026-11-15) = only errors the agent ADDS: finalBuild errors minus the same run's
  baselineBuild errors (run.json), matched on id + file + message, not line. A run "has compile errors" if that set
  is non-empty. Needed because efcore-27428 and csvhelper-2132 don't compile before the agent starts.

## Open before any agent run
- **Sandbox:** the agent runs on the WSL host as this user and can read/write /mnt/c (the whole Windows drive),
  ~/.ssh, git credentials, etc. Options were laid out on 2026-11-15; decision pending.

## Known caveat
- (Resolved 2026-11-15) The CLI would load ~73 unpinned "public skills" from github.com/OpenHands/extensions HEAD;
  they are now disabled in both conditions (see Per-task runner).
