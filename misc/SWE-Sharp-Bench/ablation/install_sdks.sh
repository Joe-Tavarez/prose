#!/usr/bin/env bash
# One isolated .NET root per SDK version the SWE-Sharp-Bench harness installs for a sample task
# (harness_sdk.json), mirroring the harness image: exact SDK + .NET and ASP.NET Core runtimes 6.0 and 7.0.
set -euo pipefail
INSTALLER=~/ablation/tools/dotnet-install.sh
ROOTS=~/.dotnet-sdks
VERSIONS=$(python3 -c 'import json; print("\n".join(sorted({v["sdk"] for v in json.load(open("'"$(dirname "$0")"'/harness_sdk.json")).values() if v["sdk"]})))')
for v in $VERSIONS; do
  root=$ROOTS/$v
  if [ -x "$root/dotnet" ] && "$root/dotnet" --list-sdks | grep -q "^$v "; then echo "ok   $v"; continue; fi
  echo "inst $v"
  bash $INSTALLER --version "$v" --install-dir "$root" --no-path >/dev/null
  for rt in dotnet aspnetcore; do for ch in 6.0 7.0; do
    bash $INSTALLER --runtime $rt --channel $ch --install-dir "$root" --no-path >/dev/null
  done; done
  "$root/dotnet" --list-sdks | grep -q "^$v " || { echo "FAILED $v"; exit 1; }
done
du -sh $ROOTS
