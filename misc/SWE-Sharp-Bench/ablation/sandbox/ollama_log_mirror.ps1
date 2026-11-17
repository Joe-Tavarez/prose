# Mirror Ollama's Windows server.log into the sandbox distro, so the runner (which has no /mnt/c) can
# check every agent run for prompt truncation and cut replies (run_tasks.py OllamaLogWatch).
#
#   Start-Process -WindowStyle Hidden powershell.exe -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass',
#       '-File','C:\Repos\prose\misc\SWE-Sharp-Bench\ablation\sandbox\ollama_log_mirror.ps1'
#
# Appends every new byte of server.log to ~runner/ablation/ollama/server.log and, once a second, writes
# ~runner/ablation/ollama/mirror.json: {"utc", "srcBytes", "offset", "generation", "ollamaDebug", "error"}.
# The runner refuses to start an agent unless mirror.json is fresh and Ollama runs with OLLAMA_DEBUG
# (only then does Ollama log "truncating input messages which exceed context length").
param(
    [string]$Src = "$env:LOCALAPPDATA\Ollama\server.log",
    [string]$Dst = '\\wsl.localhost\ablation-sandbox\home\runner\ablation\ollama'
)
$ErrorActionPreference = 'Stop'
$out = Join-Path $Dst 'server.log'
$hb = Join-Path $Dst 'mirror.json'
$enc = New-Object System.Text.UTF8Encoding($false)

function Append([byte[]]$bytes, [int]$n) {
    $o = [IO.File]::Open($out, 'Append', 'Write', 'Read')
    try { $o.Write($bytes, 0, $n) } finally { $o.Close() }
}
function Note([string]$text) { $b = $enc.GetBytes("#### ollama-log-mirror: $text`n"); Append $b $b.Length }

function DebugLevel([string]$text) {
    $m = [regex]::Matches($text, 'msg="server config".*?OLLAMA_DEBUG:(\S+)')
    if ($m.Count) { return $m[$m.Count - 1].Groups[1].Value }
    return $null
}

# The server config line (with OLLAMA_DEBUG) is written once when Ollama starts: read the current one.
$debug = $null
$fs0 = [IO.File]::Open($Src, 'Open', 'Read', 'ReadWrite, Delete')   # Ollama keeps the log open for writing
$rd = New-Object IO.StreamReader($fs0, $enc)
try {
    while ($null -ne ($line = $rd.ReadLine())) {    # streams; the file may be large
        if ($line.Contains('msg="server config"')) { $d = DebugLevel $line; if ($d) { $debug = $d } }
    }
} finally { $rd.Close() }
$offset = (Get-Item $Src).Length    # mirror only what happens from now on
$gen = 0
Note "started $(Get-Date -Format o) at source offset $offset (OLLAMA_DEBUG=$debug)"
$chunk = 8MB
while ($true) {
    $err = $null
    try {
        $fs = [IO.File]::Open($Src, 'Open', 'Read', 'ReadWrite, Delete')
        try {
            $len = $fs.Length
            if ($len -lt $offset) {   # Ollama restarted: server.log was rotated to server-1.log
                $gen++; $offset = 0; $debug = $null
                Note "server.log restarted (generation $gen) $(Get-Date -Format o)"
            }
            while ($len -gt $offset) {
                $n = [int][Math]::Min($chunk, $len - $offset)
                $buf = New-Object byte[] $n
                [void]$fs.Seek($offset, 'Begin')
                $read = 0
                while ($read -lt $n) { $r = $fs.Read($buf, $read, $n - $read); if ($r -le 0) { break }; $read += $r }
                if ($read -le 0) { break }
                Append $buf $read
                $d = DebugLevel ($enc.GetString($buf, 0, $read))
                if ($d) { $debug = $d }
                $offset += $read
            }
        } finally { $fs.Close() }
    } catch { $err = $_.Exception.Message }
    $state = [ordered]@{ utc = (Get-Date).ToUniversalTime().ToString('o'); srcBytes = $len; offset = $offset;
                         generation = $gen; ollamaDebug = $debug; error = $err }
    try {
        [IO.File]::WriteAllText("$hb.tmp", ($state | ConvertTo-Json -Compress), $enc)
        Move-Item -Force "$hb.tmp" $hb
    } catch { }
    Start-Sleep -Milliseconds 1000
}
