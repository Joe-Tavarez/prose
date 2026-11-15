#!/bin/bash
# Runner-side setup of the ablation-sandbox distro (as user runner, after provision_root.sh, while
# /mnt/c and the network are still available). The SDK roots, ~/.dotnet, the NuGet packages and the
# repo cache were copied from the tested Ubuntu distro (see SETUP_NOTES.md "Sandbox").
#   setup_runner.sh OH_FREEZE_TXT     (pip freeze of the tested OpenHands tool env, used as constraints)
set -euo pipefail
FREEZE="$1"
ROSLYN_SRC=/mnt/c/Repos/RoslynAnalyzerApi
PROSE_SRC=/mnt/c/Repos/prose
export DOTNET_ROOT=/opt/dotnet PATH=/opt/dotnet:$PATH DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
export NUGET_PACKAGES=/srv/nuget

mkdir -p ~/src ~/ablation/runs
# Roslyn API + MCP wrapper: clone at the tested commit, build, publish the binaries to /opt/roslyn.
[ -d ~/src/RoslynAnalyzerApi ] || git clone -q "$ROSLYN_SRC" ~/src/RoslynAnalyzerApi
git -C ~/src/RoslynAnalyzerApi checkout -q main
git -C ~/src/RoslynAnalyzerApi log -1 --oneline
(cd ~/src/RoslynAnalyzerApi && dotnet build -v:q -nologo RoslynAnalyzerApi.csproj \
  && dotnet build -v:q -nologo mcp/RoslynAnalyzerMcp/RoslynAnalyzerMcp.csproj)
rm -rf /opt/roslyn/api /opt/roslyn/mcp
cp -a ~/src/RoslynAnalyzerApi/bin/Debug/net8.0 /opt/roslyn/api
cp -a ~/src/RoslynAnalyzerApi/mcp/RoslynAnalyzerMcp/bin/Debug/net8.0 /opt/roslyn/mcp
git -C ~/src/RoslynAnalyzerApi rev-parse HEAD > /opt/roslyn/COMMIT

# prose (harness-fixes): the runner + harness; harness/data (sample with gold patches) is gitignored.
[ -d ~/src/prose ] || git clone -q --branch harness-fixes "$PROSE_SRC" ~/src/prose
mkdir -p ~/src/prose/misc/SWE-Sharp-Bench/harness/data/tasks
cp "$PROSE_SRC"/misc/SWE-Sharp-Bench/harness/data/tasks/*.json ~/src/prose/misc/SWE-Sharp-Bench/harness/data/tasks/
ln -sfn ~/src/prose/misc/SWE-Sharp-Bench/ablation ~/ablation/runner

# OpenHands CLI, pinned exactly like the tested env (same Python, same resolved versions).
export UV_TOOL_DIR=/opt/openhands/tools UV_TOOL_BIN_DIR=/opt/openhands/bin UV_PYTHON_INSTALL_DIR=/opt/openhands/python
grep -v '^openhands==' "$FREEZE" > /tmp/oh-constraints.txt
uv tool install -q --python 3.12.16 --constraints /tmp/oh-constraints.txt openhands==1.16.0
uv pip freeze --python /opt/openhands/tools/openhands/bin/python > ~/ablation/oh-freeze-sandbox.txt
diff <(sort "$FREEZE") <(sort ~/ablation/oh-freeze-sandbox.txt) && echo "OpenHands env identical to the tested one"
chmod -R a+rX /opt/openhands /opt/roslyn
