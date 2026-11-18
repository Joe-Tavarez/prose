# Re-grades fix-r1-roslyn after the redo of imagesharp-2298 (~/ablation/redo_r1_roslyn.sh writes
# fixbatch/fix-r1-roslyn-redo.done). Keeps the first grading as *.before-redo.json. Same harness run id, so
# the 35 unchanged instances reuse their per-instance reports and only imagesharp-2298 is evaluated.
# Safe to re-run: skipped once fix-r1-roslyn-redo.graded exists. Log: C:\Users\jtava\ablation-batch\grade.log
$dir = "C:\Users\jtava\ablation-batch"
$log = "$dir\grade.log"
$fb = "\\wsl.localhost\ablation-sandbox\home\runner\ablation\fixbatch"
$id = "fix-r1-roslyn"; $cond = "roslyn"
$report = "C:\Repos\prose\misc\SWE-Sharp-Bench\harness\openhands-1.16.0__gpt-oss-20b__$cond.$id.json"
function Log($m) { "$(Get-Date -Format s) $m" | Out-File -Append -Encoding utf8 $log }
if (Test-Path "$dir\$id-redo.graded") { exit 0 }
Log "$id redo: grader waiting"
while (-not (Test-Path "$fb\$id-redo.done")) {
    if (Test-Path "$fb\REDO_FAILED") { Log "$id redo failed ($(Get-Content "$fb\REDO_FAILED")); grader stops"; exit 1 }
    Start-Sleep -Seconds 300
}
# the first grading must have finished before it can be kept
while (-not (Test-Path "$dir\$id.graded")) { Start-Sleep -Seconds 300 }
if (-not (Test-Path "$dir\$id.before-redo.json")) { Copy-Item "$dir\$id.json" "$dir\$id.before-redo.json" }
$kept = $report -replace '\.json$', '.before-redo.json'
if ((Test-Path $report) -and -not (Test-Path $kept)) { Copy-Item $report $kept }
Copy-Item "\\wsl.localhost\ablation-sandbox\home\runner\ablation\runs\$id\$cond\predictions.json" "$dir\$id.json"  # byte-exact
Log "$id redo: predictions copied ($((Get-Item "$dir\$id.json").Length) bytes); re-grading"
$cmd = "cd /mnt/c/Repos/prose/misc/SWE-Sharp-Bench/harness && .venv/bin/python -m swe_sharp_bench.cli " +
       "--dataset_name data/tasks/sample.json --predictions_path /mnt/c/Users/jtava/ablation-batch/$id.json " +
       "--run_id $id --namespace '' --max_workers 3 > /mnt/c/Users/jtava/ablation-batch/$id.redo.grade.log 2>&1; echo exit `$?"
$r = wsl.exe -d Ubuntu -- bash -lc $cmd
Log "$id redo re-graded: $r (report: $report; first grading kept as $kept)"
if ("$r" -match "exit 0") { Get-Date -Format s | Out-File "$dir\$id-redo.graded" }
