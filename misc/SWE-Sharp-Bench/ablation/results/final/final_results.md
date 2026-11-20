# Final results: gpt-oss:20b, 3 rounds x 3 conditions (35 tasks; spectreconsole__spectre-console-1303 excluded)

## Resolved

| condition | round 1 | round 2 | round 3 | pooled | mean per pass |
|---|---|---|---|---|---|
| text | 4/35 (11.4%) | 5/35 (14.3%) | 6/35 (17.1%) | 15/105 (14.3%) | 5.00 |
| roslyn | 5/35 (14.3%) | 6/35 (17.1%) | 3/35 (8.6%) | 14/105 (13.3%) | 4.67 |
| roslyn-enforced | 5/35 (14.3%) | 4/35 (11.4%) | 5/35 (14.3%) | 14/105 (13.3%) | 4.67 |

## Per-task solve counts (0-3 of 3 rounds)

| solved in | text | roslyn | roslyn-enforced |
|---|---|---|---|
| 0/3 | 27 | 26 | 29 |
| 1/3 | 4 | 5 | 0 |
| 2/3 | 1 | 3 | 4 |
| 3/3 | 3 | 1 | 2 |

| task | text | roslyn | roslyn-enforced |
|---|---|---|---|
| ardalis__cleanarchitecture-546 | 3 | 1 | 2 |
| avaloniaui__avalonia-15498 | 0 | 1 | 0 |
| avaloniaui__avalonia-16564 | 1 | 0 | 0 |
| devlooped__moq-1081 | 1 | 1 | 0 |
| dotnet__benchmarkdotnet-2304 | 2 | 1 | 2 |
| dotnet__benchmarkdotnet-2368 | 0 | 1 | 2 |
| dotnet__efcore-27428 | 1 | 2 | 3 |
| polly-2164 | 1 | 2 | 0 |
| restsharp__restsharp-1676 | 3 | 3 | 2 |
| serilog__serilog-2083 | 3 | 2 | 3 |

Tasks never solved in any of the 9 passes: 25/35.

## Paired comparisons per task (two-sided exact tests)

| comparison | tasks better / worse / tied | Wilcoxon signed-rank W+ / W-, n | Wilcoxon p | sign test p |
|---|---|---|---|---|
| roslyn vs text | 4 / 4 / 27 | 16 / 20, n=8 | 1.000 | 1.000 |
| roslyn-enforced vs text | 2 / 5 / 28 | 13 / 15, n=7 | 1.000 | 0.453 |

McNemar per round (exact binomial on discordant tasks; b = only the Roslyn condition solved, c = only text solved):

| comparison | round | both | b | c | neither | p |
|---|---|---|---|---|---|---|
| roslyn vs text | 1 | 2 | 3 | 2 | 28 | 1.000 |
| roslyn vs text | 2 | 3 | 3 | 2 | 27 | 1.000 |
| roslyn vs text | 3 | 2 | 1 | 4 | 28 | 0.375 |
| roslyn-enforced vs text | 1 | 3 | 2 | 1 | 29 | 1.000 |
| roslyn-enforced vs text | 2 | 3 | 1 | 2 | 29 | 1.000 |
| roslyn-enforced vs text | 3 | 4 | 1 | 2 | 28 | 1.000 |

## Proposal metrics (pooled over 3 rounds)

| condition | % resolved | steps to resolution: model turns, median (mean; n resolved) | actions, median | non-empty patches | with compile errors added | rate | rate without NU1900 |
|---|---|---|---|---|---|---|---|
| text | 14.3% | 36 (43.4; n=15) | 35 | 70 | 23 | 32.9% | 25.7% |
| roslyn | 13.3% | 52 (55.5; n=14) | 49.5 | 74 | 18 | 24.3% | 20.3% |
| roslyn-enforced | 13.3% | 33 (36.5; n=14) | 30.5 | 76 | 10 | 13.2% | 7.9% |

Compile-error rate vs text, exact two-sided Fisher test on pooled non-empty patches (indicative only: the runs are not independent, each task appears up to 3 times per condition):

- roslyn vs text (all added errors): 18/74 vs 23/70, p = 0.274
- roslyn vs text (without NU1900): 15/74 vs 18/70, p = 0.552
- roslyn-enforced vs text (all added errors): 10/76 vs 23/70, p = 0.005
- roslyn-enforced vs text (without NU1900): 6/76 vs 18/70, p = 0.006

## Clustered test: within-task permutation (exact)

Runs on the same task are correlated, so here the condition labels are shuffled only within each task, keeping each task's number of runs per condition (exact null distribution by convolving one hypergeometric per task; equivalent to an exact stratified test with tasks as strata). Two-sided p = P(|T - E[T]| >= observed). Tasks where relabeling can't change anything (no events, all events, or no runs in one condition) don't contribute.

| comparison | metric | rate (comparison) | rate (text) | observed / expected events | informative tasks | p |
|---|---|---|---|---|---|---|
| roslyn vs text | resolve rate (all runs) | 13.3% | 14.3% | 14 / 14.5 | 9 | 1.000 |
| roslyn vs text | compile-error rate, all added errors (non-empty patches) | 24.3% | 32.9% | 18 / 21.1 | 16 | 0.170 |
| roslyn vs text | compile-error rate, without NU1900 (non-empty patches) | 20.3% | 25.7% | 15 / 16.8 | 14 | 0.465 |
| roslyn-enforced vs text | resolve rate (all runs) | 13.3% | 14.3% | 14 / 14.5 | 8 | 1.000 |
| roslyn-enforced vs text | compile-error rate, all added errors (non-empty patches) | 13.2% | 32.9% | 10 / 18.0 | 14 | <0.001 |
| roslyn-enforced vs text | compile-error rate, without NU1900 (non-empty patches) | 7.9% | 25.7% | 6 / 13.1 | 11 | <0.001 |

Rates here are pooled over every run that enters the test, as in the tables above. The p-values replace the indicative Fisher tests above, which treat runs as independent.

Compile-error rate per round (non-empty patches with errors added / non-empty patches):

| condition | round 1 | round 2 | round 3 |
|---|---|---|---|
| text | 6/19 (31.6%) | 8/24 (33.3%) | 9/27 (33.3%) |
| roslyn | 4/24 (16.7%) | 7/26 (26.9%) | 7/24 (29.2%) |
| roslyn-enforced | 2/23 (8.7%) | 4/24 (16.7%) | 4/29 (13.8%) |

## Process metrics (pooled over 3 rounds; 105 runs per condition)

| metric | text | roslyn | roslyn-enforced |
|---|---|---|---|
| empty patches | 35 | 31 | 29 |
| never made a successful edit | 37 | 32 | 30 |
| hit the 100-step limit (MaxIterationsReached) | 33 | 39 | 30 |
| 2-hour timeouts | 6 | 0 | 1 |
| invalid runs (context budget check) | 0 | 0 | 0 |
| malformed tool calls (total) | 45 | 26 | 37 |
| runs with >= 1 malformed tool call | 27 | 18 | 21 |
| invalid tool calls (total) | 361 | 510 | 534 |
| runs with >= 1 invalid tool call | 90 | 101 | 101 |
| agent Roslyn analysis calls (total) | 0 | 210 | 145 |
| agent Roslyn analysis calls per run (median) | 0 | 1 | 1 |
| runs with 0 agent Roslyn analysis calls | 105 | 36 | 35 |
| agent Roslyn calls, all roslyn_* tools (total) | 0 | 385 | 252 |
| enforced automatic Roslyn calls (total) | - | - | 1438 |
| enforced automatic analysis calls (analyze/diagnostics) | - | - | 1080 |
| Roslyn finish gate fired (runs) | - | 20 | 45 |
| enforced gate refusals (total) | - | - | 10 |
| runs with >= 1 enforced gate refusal | - | - | 5 |
| enforced gate: stop allowed with introduced errors | - | - | 2 |
| agent minutes per run (median) | 5.3 | 3.5 | 4.1 |
| model turns per run (median) | 67 | 71 | 59 |

## Outcome of every run (pooled; one primary reason per unresolved run)

| outcome | text | roslyn | roslyn-enforced |
|---|---|---|---|
| resolved | 15 | 14 | 14 |
| empty patch | 35 | 31 | 29 |
| grading error | 2 | 0 | 0 |
| patch did not apply | 0 | 0 | 0 |
| no tests ran: build failure, agent's code does not compile | 17 | 15 | 5 |
| no tests ran: build failure, tests do not compile against the patch | 12 | 18 | 19 |
| no test results: other | 4 | 2 | 4 |
| regression (previously passing test fails) | 3 | 3 | 3 |
| target tests failing | 17 | 22 | 31 |

Among unresolved runs with a non-empty patch that was graded: target tests failing = all previously passing tests still pass but a target test does not; regression = at least one previously passing test fails or no longer runs; no tests ran = none of the task's tests produced a result. Build failure is split by the runner's own final build of the agent's patch (without the task's tests): if it added compile errors (NU1900 left out), the agent's code does not compile; if not, only the task's tests fail to compile against the patch (typically an API the tests call was not added). No test results, other = the test log has no compiler errors but no results either (terminal-gui-3195: the target test filter matched no test; benchmarkdotnet-2304/2368: the repo's test script wrote no results file).
Of the 70 'target tests failing' runs, 22 pass some but not all target tests.
