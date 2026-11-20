# Final results: gpt-oss:20b, nine passes (fix-r{1,2,3}-{text,roslyn,enforced})

All runs after the context budget fix (SETUP_NOTES.md "Context budget fix"); every earlier run is invalid.
36 tasks x 3 conditions x 3 rounds = 324 runs; spectreconsole__spectre-console-1303 is excluded from all results
(its harness image fails even for the gold patch), leaving 35 tasks and 315 runs. fix-r1-roslyn includes the
redo of imagesharp-2298 (SETUP_NOTES "Redo of fix-r1-roslyn imagesharp-2298").

| file | what |
|---|---|
| final_runs.csv | one row per run (all 324; filter `excluded == False`) |
| final_results.md | the results tables |
| final_stats.json | the same numbers, machine-readable, plus p-values |
| final_runs.jsonl | per-run extract from the sandbox run records (input to final_combine.py) |
| grades/*.json | harness summary report per pass (`.before-redo` = fix-r1-roslyn before the redo) |
| grades/<pass>/<task>.report.json | harness per-instance report (graded non-empty patches only) |

Reproduce: `analysis/final_extract.py` in the sandbox (reads ~/ablation/runs), then
`harness/.venv/bin/python analysis/final_combine.py results/final/final_runs.jsonl harness results/final` in Ubuntu
(reads harness/logs/run_evaluation, which is git-ignored).

## final_runs.csv columns

| column | meaning |
|---|---|
| round, condition, runId, instance | 1-3; text / roslyn / roslyn-enforced; pass id; task |
| excluded | True for spectre-console-1303 |
| resolved | harness verdict (all FAIL_TO_PASS and PASS_TO_PASS tests pass) |
| outcome | resolved, or the primary reason it failed (see final_results.md, last section) |
| modelTurns | model turns (what the 100-step limit counts); modelTurnsSource "events (lower bound)" for the 7 runs killed by the 2-hour wall clock, which have no driver summary |
| actions | tool calls executed (ActionEvents) |
| hitStepLimit | the SDK's MaxIterationsReached event (not run.json's hitStepLimit, which is wrong; SETUP_NOTES "Step limit") |
| timedOut | killed by the 2-hour wall clock |
| agentMinutes | agent wall clock |
| patchLines, patchFiles | size of the predicted patch (0 = empty patch) |
| successfulEdits | fileEditorEdits (file_editor create/str_replace/insert/undo_edit that did not error) + terminalWrites (shell commands that write files and exited 0) |
| malformedToolCalls | tool calls Ollama could not parse (recovered by the driver) |
| invalidToolCalls | tool calls the SDK rejected: unknown tool or bad arguments (AgentErrorEvents) |
| agentRoslynAnalysisCalls | the agent's own roslyn_analyze_* and roslyn_diagnostics calls; agentRoslynCallsAll = every roslyn_* tool |
| autoRoslynCalls, autoRoslynAnalysisCalls | roslyn-enforced only: the runner's automatic Roslyn calls (all / analysis) |
| finishGateTriggered | roslyn conditions: the finish gate refused a stop without roslyn_diagnostics |
| enforcedGateChecks, enforcedGateRefusals, enforcedGateAllowedWithIntroducedErrors | roslyn-enforced: whole-solution gate checks, refusals (max 3), stop allowed after 3 refusals with errors left |
| baselineBuildErrors, finalBuildExit | runner's build before the agent / after (without the task's tests) |
| compileErrorsAdded | final build errors not in the baseline (id + file + message); compileErrorsAddedExclNU1900 leaves out NU1900 (NuGet audit, fails without network); addedErrorIds lists the ids |
| f2pTotal, f2pPassed, f2pNotRun | target (FAIL_TO_PASS) tests: total, passed, produced no result |
| p2pTotal, p2pFailedRan, p2pNotRun | previously passing tests: total, ran and failed, produced no result |
| testLogBuildErrors | the harness test log contains compiler/MSBuild errors |
| reparseAgrees | the re-parsed test results give the harness's verdict (true for every run) |
| condensations, maxPromptPlusReply | context condenser runs; largest prompt + reply (Ollama log; limit 65,536) |
| driverStatus, invalidRun, runError | driver end state; context-budget invalidation (none); runner error |
