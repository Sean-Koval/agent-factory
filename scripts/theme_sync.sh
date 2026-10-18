#!/bin/sh
# Open a pull request in each tool repo that vendors Airframe, syncing it to a theme tag.
#
#   sh scripts/theme_sync.sh                       # newest tag in theme/CHANGELOG.md, every tool
#   sh scripts/theme_sync.sh theme-v2 hangar       # one tag, chosen repos
#
# For each repo: clone it, run its own scripts/sync-airframe.sh <tag>, and when the vendored
# files change, push branch airframe/<tag> and open a PR through the REST API. Repos already in
# sync, or with that branch already pushed, are left alone, so reruns are safe.
# Needs git and gh, authenticated as someone who can push to the tool repos (`gh auth login`
# locally; the theme workflow passes a short-lived GitHub App token). No GraphQL.
# Optional: THEME_SYNC_TRAILER (commit trailer lines) and THEME_SYNC_PR_FOOTER (PR body footer).
set -eu

root="$(cd "$(dirname "$0")/.." && pwd)"
owner="${THEME_SYNC_OWNER:-Sean-Koval}"
tag="${1:-$(python3 "$root/scripts/theme_release.py" version)}"
[ $# -gt 0 ] && shift
repos="${*:-hangar flightdeck ai-dlc tower}"
branch="airframe/$tag"

case "$tag" in theme-v[0-9]*) ;; *) echo "theme_sync: '$tag' is not a theme-vN tag" >&2; exit 2 ;; esac
if ! git ls-remote --exit-code --tags "https://github.com/$owner/agent-factory" "refs/tags/$tag" >/dev/null; then
  echo "theme_sync: tag $tag is not published on $owner/agent-factory yet" >&2
  exit 1
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
status=0

for repo in $repos; do
  dir="$work/$repo"
  if ! git clone -q --depth 1 "https://github.com/$owner/$repo.git" "$dir"; then
    echo "$repo: clone failed" >&2; status=1; continue
  fi
  if [ ! -f "$dir/scripts/sync-airframe.sh" ]; then
    echo "$repo: no scripts/sync-airframe.sh; skipped" >&2; status=1; continue
  fi
  if git -C "$dir" ls-remote --exit-code --heads origin "$branch" >/dev/null 2>&1; then
    echo "$repo: branch $branch already exists; skipped"; continue
  fi
  (cd "$dir" && sh scripts/sync-airframe.sh "$tag" >/dev/null) || {
    echo "$repo: sync-airframe.sh $tag failed" >&2; status=1; continue
  }
  if [ -z "$(git -C "$dir" status --porcelain)" ]; then
    echo "$repo: already at $tag"; continue
  fi
  base="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"
  git -C "$dir" checkout -q -b "$branch"
  git -C "$dir" add -A
  name="$(git config user.name || echo airframe-sync)"
  email="$(git config user.email || echo airframe-sync@users.noreply.github.com)"
  git -C "$dir" -c user.name="$name" -c user.email="$email" \
    commit -q -m "style: sync Airframe theme to $tag" \
    -m "Vendored with scripts/sync-airframe.sh $tag from $owner/agent-factory; see theme/CHANGELOG.md there." \
    ${THEME_SYNC_TRAILER:+-m "$THEME_SYNC_TRAILER"}
  git -C "$dir" push -q origin "$branch"
  body="Syncs the vendored Airframe theme to [\`$tag\`](https://github.com/$owner/agent-factory/releases/tag/$tag) with \`sh scripts/sync-airframe.sh $tag\`. Changes: [theme/CHANGELOG.md](https://github.com/$owner/agent-factory/blob/$tag/theme/CHANGELOG.md). Files are taken unmodified; the product hue stays in this repo.${THEME_SYNC_PR_FOOTER:+

$THEME_SYNC_PR_FOOTER}"
  url="$(gh api "repos/$owner/$repo/pulls" -f title="style: sync Airframe theme to $tag" \
    -f head="$branch" -f base="$base" -f body="$body" --jq .html_url)" || {
    echo "$repo: pushed $branch but could not open the PR" >&2; status=1; continue
  }
  echo "$repo: $url"
done
exit $status
