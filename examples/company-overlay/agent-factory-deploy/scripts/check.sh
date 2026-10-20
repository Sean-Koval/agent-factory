#!/bin/sh
# CI for the deploy repo (and the `verify` of its repo policy): every overlay builds, the change-set profiles are
# well formed, and the rest of the policy applies cleanly to the install named by HANGAR_URL / HANGAR_TOKEN (a dry
# run: nothing changes).
#   sh scripts/check.sh            needs kustomize 5 and hangar (pip install hangar==<the HANGAR_TAG you run>)
set -eu
cd "$(dirname "$0")/.."
for o in overlays/*/; do
  kustomize build "$o" > /dev/null
  echo "ok: $o builds"
done
for p in policy/changesets/*.yaml; do
  hangar changeset validate "$p"
done
# Credentials and repo policies: what CD applies after a merge, shown without changing anything. Change-set profiles
# are set with `hangar changeset profile-set` until `hangar apply` takes hangar.changeset-profile/v1 documents too.
hangar apply -f policy/credentials -f policy/repos --dry-run
