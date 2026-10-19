#!/bin/sh
# CI for the deploy repo (and the `verify` of its repo policy): every overlay builds, and the policy applies cleanly.
#   sh scripts/check.sh            needs kustomize 5 and hangar (pip install hangar==<the HANGAR_TAG you run>)
set -eu
cd "$(dirname "$0")/.."
for o in overlays/*/; do
  kustomize build "$o" > /dev/null
  echo "ok: $o builds"
done
# What CD runs after a merge, without changing anything: prints what would be created, changed or left alone.
hangar apply -f policy/ --dry-run
