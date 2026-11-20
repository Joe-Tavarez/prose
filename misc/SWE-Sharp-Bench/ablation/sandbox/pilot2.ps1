# Second-model pilot (user request 2026-11-18): devstral-small-2:24b and qwen3-coder:30b, each on the 3 pilot
# tasks (serilog-2083, spectre-console-1503, autofac-1424) in text, roslyn and roslyn-enforced. Settings are
# identical to the gpt-oss re-run except the model (new settings dir per model, 48K budget, 100 steps,
# Ollama truncation checks on). Starts only after the whole re-run is graded: all nine fix-r* passes AND the
# fix-r1-roslyn imagesharp-2298 redo. Then:
#   1 verify per model: Ollama context is 65,536 (ollama ps), GPU/CPU split, and real tokens vs gpt-oss on the
#     same text, so that the largest prompt+reply seen with gpt-oss, scaled, still fits in 65,536. Stops if not.
#   2 settings dirs (gen_settings.py --model), checked identical to the gpt-oss dir except the model
#   3 pilot runs (run ids pilot2-<model>), 4 grading, 5 summary (analysis/pilot2_summary.py)
# Then stops. Everything goes to C:\Users\jtava\ablation-batch\pilot2\ (log.txt, verify.json, summary, DONE or
# STOPPED). Safe to re-run after a restart: finished runs are skipped, graded conditions are not re-graded.
$ErrorActionPreference = "Stop"
$dir = "C:\Users\jtava\ablation-batch"
$P = "$dir\pilot2"
$sbx = "\\wsl.localhost\ablation-sandbox\home\runner"
$fb = "$sbx\ablation\fixbatch"
$harness = "C:\Repos\prose\misc\SWE-Sharp-Bench\harness"
$tasks = "serilog__serilog-2083 spectreconsole__spectre-console-1503 autofac__autofac-1424"
$models = @("devstral-small-2:24b", "qwen3-coder:30b")
$conds = @("text", "roslyn", "roslyn-enforced")
New-Item -ItemType Directory -Force $P | Out-Null
function Log($m) { "$(Get-Date -Format s) $m" | Out-File -Append -Encoding utf8 "$P\log.txt" }
function Stop-Pilot($m) { Log "STOPPED: $m"; "$(Get-Date -Format s) $m" | Out-File -Encoding utf8 "$P\STOPPED"; exit 1 }
function Slug($m) { ($m -replace '[^A-Za-z0-9.]+', '-') }
function Sandbox($script) {  # run a bash script in the sandbox as runner; returns its output
    # stderr is merged into the output; in PowerShell 5.1 that turns each stderr line into an error record,
    # which "Stop" would make fatal (the BOM line's "command not found" killed the first launch), so not here
    $ErrorActionPreference = "Continue"
    ("`n" + $script + "`ntrue`n") -replace "`r", "" | wsl.exe -d ablation-sandbox -u runner -- bash -s 2>&1 |
        ForEach-Object { "$_" } | Where-Object { $_ -notmatch 'command not found' }
}
trap { Stop-Pilot "unexpected error: $($_.Exception.Message) (line $($_.InvocationInfo.ScriptLineNumber))" }
if (Test-Path "$P\DONE") { exit 0 }
Remove-Item "$P\STOPPED" -ErrorAction SilentlyContinue
Log "pilot2: waiting for the re-run to be fully graded"

# --- 0 wait: nine passes graded + redo graded ---
$need = @()
foreach ($r in 1..3) { foreach ($c in "text", "roslyn", "enforced") { $need += "$dir\fix-r$r-$c.graded" } }
$need += "$dir\fix-r1-roslyn-redo.graded"
while (@($need | Where-Object { -not (Test-Path $_) }).Count -gt 0) {
    if (Test-Path "$fb\PAUSED") { Stop-Pilot "the re-run is PAUSED ($(Get-Content "$fb\PAUSED")); pilot not started" }
    if (Test-Path "$fb\REDO_FAILED") { Stop-Pilot "the imagesharp-2298 redo failed ($(Get-Content "$fb\REDO_FAILED")); pilot not started" }
    Start-Sleep -Seconds 600
}
Log "pilot2: re-run fully graded; starting"
if (Get-CimInstance Win32_Process -Filter "Name='wsl.exe'" | Where-Object { $_.CommandLine -match 'start_fix\.sh|redo_r1_roslyn\.sh' }) {
    Stop-Pilot "a re-run script is still running although everything is graded; not starting"
}

# --- 1 verify ---
$have = (Invoke-RestMethod http://127.0.0.1:11434/api/tags).models.name
foreach ($m in $models) { if ($have -notcontains $m) { Stop-Pilot "model $m is not installed (see pull-*.log)" } }
$worst = [int]((Sandbox @'
python3 - <<'PY'
import json, glob, os
w = [((json.load(open(f)).get("ollamaLog") or {}).get("maxPromptPlusReply") or 0) for f in glob.glob(os.path.expanduser("~/ablation/runs/fix-r*/*/*/run.json"))]
print(max(w))
PY
'@ | Select-Object -Last 1))
$sample = [IO.File]::ReadAllText("$sbx\ablation\runs\fix-r1-text\text\autofac__autofac-1424\events.jsonl").Substring(0, 150000)
function Count($m) {
    $body = @{ model = $m; stream = $false; keep_alive = "10m"; options = @{ num_predict = 1 }
               messages = @(@{ role = "user"; content = $sample }) } | ConvertTo-Json -Depth 5
    $t = Get-Date
    $r = Invoke-RestMethod http://127.0.0.1:11434/api/chat -Method Post -ContentType "application/json" -Body $body -TimeoutSec 3600
    $ps = (Invoke-RestMethod http://127.0.0.1:11434/api/ps).models | Where-Object { $_.name -eq $m }
    [ordered]@{ model = $m; promptTokens = $r.prompt_eval_count; seconds = [math]::Round(((Get-Date) - $t).TotalSeconds)
                context = $ps.context_length; sizeGB = [math]::Round($ps.size / 1GB, 1); vramGB = [math]::Round($ps.size_vram / 1GB, 1)
                gpuPct = if ($ps.size) { [math]::Round(100 * $ps.size_vram / $ps.size) } else { $null }
                processorLine = ((ollama ps | Select-String ([regex]::Escape($m))) -replace '\s+', ' ').Trim() }
}
$ref = Count "gpt-oss:20b"
$verify = [ordered]@{ at = (Get-Date -Format s); sampleChars = $sample.Length; worstPromptPlusReplyGptOss = $worst; reference = $ref; models = @() }
$ok = $true
foreach ($m in $models) {
    $c = Count $m
    $c.ratioVsGptOss = [math]::Round($c.promptTokens / $ref.promptTokens, 3)
    $c.predictedWorst = [math]::Round($worst * $c.ratioVsGptOss)
    $c.fits = ($c.context -eq 65536) -and ($c.predictedWorst -le 65536) -and ($c.promptTokens -gt 0)
    if (-not $c.fits) { $ok = $false }
    $verify.models += $c
    Log "verify $m : context $($c.context), $($c.gpuPct)% GPU ($($c.vramGB)/$($c.sizeGB) GB), $($c.promptTokens) tokens vs gpt-oss $($ref.promptTokens) (x$($c.ratioVsGptOss)), worst $worst -> $($c.predictedWorst): fits $($c.fits); ps: $($c.processorLine)"
}
$verify | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 "$P\verify.json"
if (-not $ok) { Stop-Pilot "context check failed for at least one model (verify.json); pilot not run" }

# --- 2 settings dirs, identical except the model ---
foreach ($m in $models) {
    $s = Slug $m
    $out = Sandbox @"
set -e
REF=~/ablation/openhands-gpt-oss-20b-ctx48k; D=~/ablation/openhands-$s-ctx48k
if [ ! -d `$D ]; then
  mkdir -p `$D/text `$D/roslyn
  cp `$REF/text/mcp.json `$D/text/; cp `$REF/roslyn/mcp.json `$D/roslyn/
  /opt/openhands/tools/openhands/bin/python ~/ablation/runner/gen_settings.py `$D --model openai/$m > /dev/null
fi
for f in text/agent_settings.json roslyn/agent_settings.json text/mcp.json roslyn/mcp.json text/cli_config.json roslyn/cli_config.json; do
  [ -f `$REF/`$f ] || continue
  if ! diff <(sed 's#gpt-oss:20b#$m#g' `$REF/`$f) `$D/`$f > /dev/null; then echo "DIFF `$f"; diff <(sed 's#gpt-oss:20b#$m#g' `$REF/`$f) `$D/`$f | head -5; fi
done
echo "settings `$D checked"
"@
    Log "settings $m : $($out -join ' / ')"
    if ("$out" -match "DIFF" -or "$out" -notmatch "checked") { Stop-Pilot "settings for $m differ from the gpt-oss settings beyond the model: $out" }
}

# --- 3 pilot runs ---
foreach ($m in $models) {
    $s = Slug $m; $rid = "pilot2-$s"
    Log "$rid : running (9 runs)"
    $out = Sandbox @"
cd ~/ablation/runner
echo "=== start `$(date -Is) ===" >> ~/ablation/$rid.log
python3 run_tasks.py --run-id $rid --conditions $($conds -join ' ') --instances $tasks --openhands ~/ablation/openhands-$s-ctx48k >> ~/ablation/$rid.log 2>&1
echo "exit `$?"
"@
    Log "$rid : $($out -join ' ')"
}

# --- 4 grading ---
foreach ($m in $models) {
    $s = Slug $m; $rid = "pilot2-$s"
    foreach ($c in $conds) {
        $gid = "$rid-$c"
        if (Test-Path "$P\$gid.graded") { continue }
        $src = "$sbx\ablation\runs\$rid\$c\predictions.json"
        if (-not (Test-Path $src)) { Log "$gid : no predictions.json; not graded"; continue }
        Copy-Item $src "$P\$gid.json"
        $cmd = "cd /mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness && .venv/bin/python -m swe_sharp_bench.cli " +
               "--dataset_name data/tasks/sample.json --predictions_path /mnt/c/Users/jtava/ablation-batch/pilot2/$gid.json " +
               "--run_id $gid --namespace '' --max_workers 3 > /mnt/c/Users/jtava/ablation-batch/pilot2/$gid.grade.log 2>&1; echo exit `$?"
        $r = wsl.exe -d Ubuntu -- bash -lc $cmd
        Log "$gid graded: $r"
        if ("$r" -match "exit 0") { Get-Date -Format s | Out-File "$P\$gid.graded" }
    }
}

# --- 5 summary ---
$rep = "$sbx\ablation\grades\pilot2"
New-Item -ItemType Directory -Force $rep | Out-Null
Get-ChildItem $harness -Filter "openhands-1.16.0__*.pilot2-*.json" | Copy-Item -Destination $rep
$specs = ($models | ForEach-Object { "~/ablation/runs/pilot2-$(Slug $_):/home/runner/ablation/grades/pilot2" }) -join ' '
$out = Sandbox "cd ~/ablation/runner && python3 analysis/pilot2_summary.py ~/ablation/grades/pilot2 $specs > /dev/null && echo summary ok"
Log "summary: $($out -join ' ')"
Copy-Item "$rep\pilot2_summary.md", "$rep\pilot2_summary.json" $P -ErrorAction SilentlyContinue
(ollama ps) | Out-File -Encoding utf8 "$P\ollama-ps-end.txt"
Get-Date -Format s | Out-File "$P\DONE"
Log "pilot2: done; stopped (summary: $P\pilot2_summary.md)"
