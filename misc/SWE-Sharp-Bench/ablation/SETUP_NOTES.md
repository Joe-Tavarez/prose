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
- Agents are run by the per-task runner's oh_driver.py (below), not `openhands --headless`, which has no step
  limit option. Settings come from the persistence dir's files; nothing uses --override-with-envs.
- Ollama context (65536) is set server-side; the OpenAI endpoint ignores num_ctx. Verify with `curl localhost:11434/api/ps`.

## Per-task runner (prose: misc/SWE-Sharp-Bench/ablation/; ~/ablation/runner links there)
- `run_tasks.py` (run with ~/ablation/loadcheck-venv/bin/python) + `oh_driver.py` (runs with the OpenHands tool python).
- Dry run: `python run_tasks.py --run-id dry-36b --dry-run` -> ~/ablation/runs/<run-id>/summary.md
  (dry-36b, 2026-11-15: 72/72 set up, agent shell SDK == harness SDK 72/72, Roslyn MCP 7 tools + ready, no patch
  without an agent; remaining flags = the baseline errors and Roslyn /health warnings listed in Methods notes)
- Real run (NOT yet done): `python run_tasks.py --run-id <id> --conditions text roslyn`
  (baseline + final `dotnet build` always run; --no-build-check skips both)
- Same in both conditions: fresh checkout with history only up to base_commit (see "Git history"), REPO_SETUP prepare steps,
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
- **Resume (2026-11-15):** rerun the same command with the same --run-id (e.g. after a PC restart). A run is done
  when its run.json exists (written last, atomically) and is skipped; a run dir without run.json was interrupted:
  it is moved to <run>/_interrupted/ and redone from a fresh workspace. predictions.jsonl/.json are rebuilt from
  finished runs. Settings that change results must match config.json, else it refuses. Tested by terminating the
  distro mid-run. After a restart: Ollama and (for grading) Docker Desktop must be running on Windows.
- predictions.json (JSON array) is what swe_sharp_bench.cli --predictions_path reads; predictions.jsonl is kept.
- **Step limit counts iterations, not actions** (found in the pilot): the SDK's max_iteration_per_run counts model
  turns, including turns where the model sent no tool call and got "use a tool" feedback. So a run can stop at 100
  with 70 actions. driver.json `hitStepLimit` (actions >= 100) is wrong for that; use the MaxIterationsReached event
  (pilot_report.py `hitIterationLimit`) and report actions and no-tool-call turns separately.
- Steps = ActionEvents in the conversation (driver.json `actions`, per-tool counts in `toolCalls`).
  Compile errors (decided 2026-11-15) = only errors the agent ADDS: finalBuild errors minus the same run's
  baselineBuild errors (run.json), matched on id + file + message, not line. A run "has compile errors" if that set
  is non-empty. Needed because efcore-27428 and csvhelper-2132 don't compile before the agent starts.

## Pre-run design decisions (2026-11-15, after the 4-model pilot; before any real run)
- **Model: gpt-oss:20b** (fits fully in the 16 GB GPU: 12.8/12.8 GB, context 65536; reasoning_effort high
  in both conditions, verified in the request OpenHands sends).
- **Temperature is NOT applied.** When reasoning_effort is set, OpenHands/litellm leave `temperature` out of
  the request (captured with a fake endpoint: keys sent = model, max_completion_tokens, reasoning_effort).
  agent_settings.json says 0.0, but every pilot run so far used Ollama's model default. Same in both conditions.
- **Stronger Roslyn treatment (agent/AGENTS.md, RoslynAnalyzerApi; sha256 recorded per run as
  run.json agentsMdSha256 / config.json).** New "Mandatory workflow" at the top: (1) roslyn_health first;
  (2) before editing, Roslyn definition (roslyn_analyze_file / roslyn_analyze_method) and references
  (roslyn_analyze_method callers; roslyn_analyze_deep references/implementations) of everything changed;
  (3) after editing, roslyn_reload then roslyn_diagnostics on every changed file, fix every error YOU
  INTRODUCED (vs the file's errors before the edit), repeat (project files only: roslyn_diagnostics with
  projects); (4) Roslyn is the source of truth. Rules 4/5 use roslyn_diagnostics on the changed files.
  Motivation: in the pilot, Roslyn-condition agents made 0-5 analysis calls per run.
  (Pilot gptoss-2 briefly used "fix every error"; reverted to the baseline wording because efcore-27428
  and csvhelper-2132 don't compile before the agent starts, and fixing those isn't the task.)
- **Finish gate (first decided for both conditions; text gate removed 2026-11-16, see below) (oh_driver.py
  FinishGate; runner default in Roslyn, --no-finish-gate to disable).**
  If the agent calls finish without its condition's check after its last file edit (or with no check at
  all), the stop is refused once and the agent gets: roslyn "Call roslyn_diagnostics on your changed files
  before finishing. If it reports errors, fix the errors you introduced." / text "Run dotnet build before
  finishing. If dotnet build fails, fix the errors you introduced." (the fix clause was added after pilot
  gptoss-2, where a text run built, failed and finished with 18 new errors; the Roslyn condition already had
  the matching rule in AGENTS.md). Remaining asymmetry, by design: the Roslyn agent always has this rule in
  AGENTS.md (the treatment text), the text agent only sees it if the gate fires. The SDK shows it as a user message
  prefixed "[Stop hook feedback] ". Check = a roslyn_diagnostics call (roslyn) / a terminal command
  containing `dotnet build` or `dotnet test` (text; test builds first). Edit = file_editor
  create/str_replace/insert/undo_edit (edits made with shell commands are not tracked). Only once per run;
  a second finish without the check is allowed. Implemented as the SDK's stop hook, so the agent continues
  in the same run loop and the 100-iteration budget is shared (not reset). Not triggered when a run ends by
  the step limit or the stuck detector. Recorded in driver.json `finishGate` (triggered, reason, action
  number, checkAfterGate, finishedAgainWithoutCheck). Tested with a scripted fake LLM
  (sandbox/test_finish_gate.py).
- **SUPERSEDED 2026-11-16: the text condition has no finish gate (see "Treatment = Roslyn package" below).**
  The text gate above was used only in pilot gptoss-3 and dry run sbx-dry-36c.
- **Treatment = the "Roslyn package" (decided 2026-11-16, before the full run; supersedes the text gate).**
  Text condition = plain OpenHands: no AGENTS.md, no finish gate, no extra instructions beyond task.md.
  Roslyn condition = Roslyn MCP tools + agent/AGENTS.md + the Roslyn finish gate (roslyn_diagnostics
  message above). run_tasks.py passes `--finish-gate roslyn` only in the Roslyn condition and `off` in text
  (visible in run.json driverCommand; driver.json finishGate is null in text). The comparison is
  plain OpenHands vs OpenHands + the whole package. **Limitation:** tools, guidance (AGENTS.md) and the gate
  are confounded. A difference can't be attributed to the tools alone versus the instructions to check
  and fix compile errors (a text agent given the same workflow rules with dotnet build might gain part of
  it). Separating them would need extra arms (text + guidance/gate; tools without AGENTS.md), which are out
  of scope. Malformed-tool-call recovery (next item) stays in both conditions: it is harness error
  handling that keeps a run alive, not task guidance.
- **Malformed tool calls don't end a run (both conditions).** In pilot gptoss-2, 2 of 3 Roslyn runs ended
  early: gpt-oss wrote prose into a tool call, Ollama returned HTTP 500 "error parsing tool call", litellm
  gave up after its retries and the SDK stopped the conversation. Now oh_driver.py catches exactly that
  error (regex: error parsing / failed to parse / invalid tool call), sends the model "Your tool call was
  malformed; try again with valid arguments." and continues the same conversation. Budget: the driver
  counts every model turn (agent.step), including the failed one, and the continued run gets only the turns
  left, so a run never exceeds --max-steps turns in total. Counted in driver.json `malformedToolCalls`
  and included in pilot_report.py `invalidToolCalls` (with the SDK's own rejected calls: unknown tool,
  missing/invalid arguments, which never ended runs). Any other LLM error still ends the run. Tested with
  the fake LLM returning Ollama's 500 persistently until the message appears (sandbox/test_finish_gate.py).
- **Stop tuning (decided 2026-11-15).** No more pilots or rule changes before the full run: Roslyn tool
  uptake (incl. runs that never call Roslyn) is a result to report, and further tuning on 3 tasks would fit
  the setup to those tasks.

## Exploratory condition "roslyn-enforced" (added 2026-11-16, AFTER repeat 1; not part of the pre-registered comparison)
- **Why.** Repeat 1 (main-gptoss-r1): text 5/35, roslyn 5/35 resolved, but the Roslyn agent barely used
  Roslyn (median 1 analysis call per run, 8/35 runs none) despite AGENTS.md and the finish gate. So repeat 1
  can't say whether Roslyn analysis helps when it is actually used. This condition takes the choice to
  use it away from the model. It was designed after seeing repeat-1 results, so it is exploratory: report it
  separately from the text vs roslyn comparison, not as a replacement for it.
- **What.** Same settings (the roslyn settings dir, byte-identical), tools, AGENTS.md and finish gate as
  roslyn; text and roslyn unchanged. Plus runner-level enforcement in oh_driver.py (`--enforce`):
  1. file_editor `view` of a .cs file -> roslyn_analyze_file (signatures, calls, diagnostics) appended to
     the view output.
  2. every successful file_editor edit (create/str_replace/insert/undo_edit) of a .cs file -> roslyn_reload
     (that file; full reload for a newly created file) + roslyn_diagnostics on that file, appended to the edit
     output.
  3. finish gate: the roslyn gate first (unchanged, once), then the stop is refused while roslyn_diagnostics
     on the whole solution (after a reload: changed .cs files, or a full reload if files were added/deleted
     /renamed or project files changed) shows errors that weren't in the baseline. Baseline = whole-solution
     roslyn_diagnostics taken by the driver before the agent starts (no agent turns). Match on id + file +
     message (not line), like the compile-error metric. Refused at most 3 times, each time listing the
     introduced errors (max 30), then the stop is allowed. Edits made with shell commands are caught here
     (git status), not by hooks 1-2.
- **Fixed choices (mechanics, not tuned):** appended Roslyn output capped at 6000 chars (JSON compacted;
  truncation says to call the tool for the rest); diagnostics maxResults 500; Roslyn call timeout 900 s.
  If the baseline or a gate compile fails, the gate can't tell and allows the stop (recorded).
- **Counting.** Runner auto-calls are recorded apart from the agent's own roslyn_* calls: driver.json
  `roslynEnforced` {calls per tool, failures, seconds, viewAppends, editChecks, baseline, gate {checks,
  refusals, introducedAtRefusal, allowedWithIntroducedErrors, lastIntroduced}}; `toolCalls` stays
  agent-initiated only. roslyn-calls.jsonl (API log) contains both. pilot_report.py: roslynAutoCalls,
  enforcedGate, enforcedBaseline.
- **Tests.** sandbox/test_enforce.py (fake LLM + fake Roslyn MCP): view/edit appends, baseline error not
  counted as introduced, 3 refusals then allow, refusal after a fix, no compile when no .cs changed,
  auto vs agent call counts. Dry run (`--conditions roslyn-enforced`) also runs every enforced call once
  per task and requires 0 introduced errors without changes (catches non-deterministic diagnostics).
- Run with `--conditions roslyn-enforced` (default conditions stay text + roslyn).

## Patch line endings (bug found grading main-gptoss-r1, fixed 2026-11-16, both conditions)
- run_tasks.collect_patch read `git diff` with text=True and write_predictions used read_text: both apply
  universal newlines, so every CRLF in a patch became LF. Hunks touching files that are CRLF at
  base_commit then failed to apply in the harness ("different line endings" -> grading error). In
  main-gptoss-r1 this hit exactly 3 of 61 non-empty patches (text csvhelper-2132, text + roslyn ocelot-1790);
  no other patch touched a CRLF file. Agent behaviour and the other metrics are unaffected.
- Fix: patch captured and stored as bytes, predictions read with read_bytes. Already-captured patches are
  repaired with repair_crlf_patches.py (apply the stripped patch to an LF copy of base_commit, convert those
  files back to CRLF, re-diff; original kept as patch.lf-stripped.diff, run.json `patchRepairedCRLF`). Only
  the line ending of lines the agent wrote is lost, which doesn't affect build or tests.

## Git history (fixed 2026-11-15, both conditions)
- Bug found before any agent run: workspaces were cloned from the full-clone cache and kept origin/* refs and tags
  up to today's upstream. serilog-1906: 154 commits after base_commit, 19 touching the gold patch's file, 54 tags;
  `git log --all` showed the real fix offline.
- Now: run_tasks.base_repo() builds ~/swe-repos/_base/<instance>.git once per instance: fetch of base_commit only
  (+ the tags merged into it; Nerdbank.GitVersioning etc. need history and tags) from the full cache. The workspace
  is a --no-hardlinks clone of that, detached at base_commit, local branch deleted, origin removed after submodule
  init. Submodules (Avalonia, ImageSharp) are cloned at their pinned commits, then lose remotes, branches, later
  tags, reflogs and unreachable objects (gc --prune=now).
- Checked on every run (run.json `history`, fatal if not clean; dry-run check): per repo and submodule 0 remotes,
  no refs except tags, 0 commits reachable from any ref/reflog that aren't ancestors of the checked-out commit,
  0 unreachable objects (git fsck --unreachable --no-reflogs).

## Sandbox (decided 2026-11-15: option C, a separate WSL distro)
Agents run only in the WSL distro `ablation-sandbox` (Ubuntu 26.04, C:\WSL\ablation-sandbox), never in `Ubuntu`.
Before this, the agent ran as the Windows user's WSL account: /mnt/c rw (whole Windows drive), Windows interop
(could run powershell.exe as the Windows user), C:\Users\jtava\.ssh readable, open internet, Docker reachable.
- Set up by misc/SWE-Sharp-Bench/ablation/sandbox/: provision_root.sh (packages, users, dirs), setup_runner.sh
  (Roslyn API build at bf8f6de -> /opt/roslyn, prose clone, OpenHands with the tested env's freeze as constraints
  -> identical 172 packages), provision_root.sh --lock (wsl.conf + ablation-harden.service). The SDK roots,
  ~/.dotnet, NuGet packages and repo cache were copied from `Ubuntu` (tar over a pipe), so the same bits as the
  earlier dry runs.
- wsl.conf: automount off (no /mnt/c), interop off, no Windows PATH, static resolv.conf, default user runner.
- ablation-harden.service (harden.sh, at boot, root): WSL's init leaves a world-writable /run/WSL interop
  socket even with interop off; harden.sh (and ablation-interop-guard.service, every second, and the runner before
  each run) keep /run/WSL root-only. /run is per distro. The binfmt handler for Windows .exe files is KERNEL-WIDE,
  shared by all WSL distros and Docker Desktop: never unregister it (an earlier version did, which broke interop
  and Docker's credential helper in `Ubuntu`, 2026-11-15). For the same reason systemd-binfmt.service is masked in
  the sandbox: its stop action unregisters every handler kernel-wide whenever the sandbox shuts down. With the
  handler registered, a real whoami.exe still can't run in the sandbox (interop off + socket locked); the per-run
  probe tests exactly that, as the agent (/opt/ablation-probe/whoami.exe). It unmounts the remaining Windows 9p mount (/usr/lib/wsl/drivers, read-only
  DriverStore), covers WSLg (/mnt/wslg, /tmp/.X11-unix: X11/Wayland/Pulse into the Windows desktop, incl. the
  shared clipboard) and /mnt/wsl (tmpfs shared by all distros) with empty tmpfs, and installs the firewall.
- /mnt/wsl is a shared mount across all WSL distros: harden.sh makes the sandbox's copy private
  (--make-rprivate) before covering it. Without that, the cover propagated into `Ubuntu` and hid Docker Desktop's
  WSL integration ("docker could not be found", 2026-11-15).
- Users: `runner` (uid 1000, passwordless sudo): setup, clone, restore, builds, patch, run records. `agent`
  (uid 1001, no sudo, home 750): the OpenHands driver, its terminal (so every command the model runs) and, in the
  Roslyn condition, the Roslyn API + MCP wrapper (they evaluate repo MSBuild code and answer the agent). Started via
  `sudo -u agent env -i <explicit env>`.
- Firewall (iptables + ip6tables, owner match on uid agent): TCP to 127.0.0.1 ports 11434 (Ollama), 5050, 5051
  only; everything else rejected (internet, DNS, other localhost services incl. Windows ones via mirrored
  networking). The runner keeps normal network access (NuGet restore, submodule clones).
- File access: agent can read /opt/{dotnet-sdks,dotnet,openhands,roslyn} and /srv/nuget (NuGet global packages,
  read-only), and write only /srv/ablation/work/<repo> (chown'ed to agent for the agent phase only) and
  /srv/ablation/agent (per-run scratch: OpenHands persistence dir copied from the runner's pristine templates,
  events.jsonl, driver.json, roslyn-calls.jsonl; copied into the run dir afterwards). It cannot read /home/runner:
  the full-history repo cache, sample.json (gold patches), harness data, the loadcheck results, other runs' records.
- Every agent run starts from the same state: all agent processes killed, scratch emptied, agent home reset from
  /etc/skel, agent files in /tmp, /var/tmp, /dev/shm deleted. After the run everything of uid agent is SIGKILLed
  (also the timeout path) and the workspace returns to runner for patch extraction and the final build.
- Probed as the agent right before every run (run.json `sandbox`, run aborts if any differs): internet by name and
  by IP blocked, DNS blocked, Ollama reachable, /mnt/c absent, no Windows mounts, no interop handler/socket, no
  WSLg sockets, /home/runner unreadable, sudo denied. run_tasks.py refuses non-dry runs without --agent-user.
- Dry runs additionally check that the agent's own `dotnet restore` works offline (it restores implicitly on
  build/test). Needed for that: NuGet's /tmp/NuGetScratch lock dir (and /tmp/.dotnet) belong to whoever creates
  them, so the runner's dotnet uses TMPDIR=/tmp/runner-<uid> (6.0.100 ignores NUGET_SCRATCH); Ocelot's legacy
  DotNetCliToolReference restore writes under /srv/nuget/.tools, the one agent-writable (ACL) part of /srv/nuget.
  NUGET_PACKAGES=/srv/nuget/ with the trailing slash (it becomes a SourceRoot; SourceLink rejects it without).
- Agent environment differences from the earlier (unsandboxed) dry runs, same in both conditions: no Windows PATH
  entries, HOME=/home/agent, workspace under /srv/ablation/work, LITELLM_LOCAL_MODEL_COST_MAP=True (litellm's bundled
  cost map instead of fetching it from GitHub at import).
- Residual: the agent can call any Ollama API on :11434 (e.g. pull/delete models; no internet through it for
  arbitrary URLs); in the text condition nothing listens on 5050/5051 in WSL, so those two ports could reach a
  Windows localhost service on them (none listening, checked 2026-11-15); the agent can edit its own event log /
  scratch files while it runs (it runs as the same uid as the driver); the patch itself comes from git by the runner.
- Grading (docker) is not available in the sandbox: copy predictions.jsonl out (\\wsl.localhost\ablation-sandbox\
  home\runner\ablation\runs\<id>) and grade in `Ubuntu`.
- Updating the runner in the sandbox: it has no /mnt/c. Sync with a tar pipe from Windows, e.g.
  `wsl -d Ubuntu -e tar -C /mnt/c/Repos/prose/misc/SWE-Sharp-Bench -cf - ablation | wsl -d ablation-sandbox -e tar -C /home/runner/src/prose/misc/SWE-Sharp-Bench -xf -`
  (run in cmd.exe; PowerShell 5.1 pipes corrupt binary data).
- Run: `wsl -d ablation-sandbox`, then `cd ~/ablation/runner && python3 run_tasks.py --run-id <id> ...`
- Verified 2026-11-15 in the sandbox: dry run sbx-dry-36b 72/72 set up with 0 errors; history clean 72/72
  (+46 submodule repos); sandbox probe 72/72; agent shell SDK == harness SDK 72/72; agent offline restore 72/72;
  empty patch 72/72; Roslyn MCP 7 tools + ready 36/36; skills text [] / roslyn [agents]. The 8 remaining flags are
  the known ones (baseline errors efcore-27428 + csvhelper-2132 in both conditions; Roslyn /health warnings on 6).
  sandbox/verify_agent.py (adversarial, as agent, real workspace): 19/19 attempts blocked, Ollama works.

## Known caveat
- (Resolved 2026-11-15) The CLI would load ~73 unpinned "public skills" from github.com/OpenHands/extensions HEAD;
  they are now disabled in both conditions (see Per-task runner).
