# Second-model pilot (abandoned, not analyzed)

Started 2026-11-19 20:30, stopped by the user at 21:19 the same evening. Planned: devstral-small-2:24b and
qwen3-coder:30b on 3 pilot tasks (serilog-2083, spectre-console-1503, autofac-1424) x text / roslyn /
roslyn-enforced, with settings identical to the gpt-oss runs except the model. Nothing here was graded or analyzed.
Don't use it for results.

Why it was abandoned: scope. Also, devstral-small-2:24b rejects the shared settings: all 9 of its runs ended at the
first model call with Ollama's HTTP 400 "devstral-small-2:24b does not support thinking", because the settings send
reasoning_effort high. qwen3-coder:30b finished 4 runs and was killed during its 5th (roslyn-enforced
serilog-2083, which has no run.json).

| path | what |
|---|---|
| pilot2-runs.tar.gz | ~/ablation/runs/pilot2-{devstral-small-2-24b,qwen3-coder-30b} and both runner logs, moved from the sandbox (a tarball because the OpenHands event paths exceed Windows' 260-character limit) |
| settings/ | the two settings dirs (~/ablation/openhands-<model>-ctx48k) |
| windows/ | the chain script's folder (log.txt, verify.json = context / GPU split / token-ratio check, STOPPED, model pull logs) |

The chain script is sandbox/pilot2.ps1. verify.json: both models' context was 65,536 and passed the scaled budget check
(devstral ~53% on GPU, x1.121 tokens vs gpt-oss; qwen3-coder ~57% on GPU, x1.064).
