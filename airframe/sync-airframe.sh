#!/bin/sh
# Refresh this repo's vendored Airframe files from Sean-Koval/agent-factory, which owns them.
# Take the files unmodified and never edit them here; change Airframe in agent-factory instead.
#
#   sh scripts/sync-airframe.sh theme-v2     # a release tag (what the sync PRs use)
#   sh scripts/sync-airframe.sh              # main
#
# Template: agent-factory airframe/sync-airframe.sh. Each tool repo keeps a copy as
# scripts/sync-airframe.sh and lists what it vendors in FILES, one "<theme file> <destination>"
# pair per line. Published theme files: airframe.css (tokens), airframe-components.css (the af-
# classes), airframe-docs.css (docs-site mapping), airframe-suite.html (the suite strip partial for the
# docs header; see below), airframe-icons.svg (sprite), airframe.js (the optional helpers: markup
# builders, toast, confirm, drawer), airframe-tokens.json, airframe-tailwind.css (Tailwind v4 theme),
# airframe.tokens.json and airframe-day.tokens.json (DTCG).
#
# The suite strip needs three lines of config in mkdocs.yml and a two-line template of your own:
#   theme: {custom_dir: overrides}
#   extra: {airframe: {product: hangar}}      # agent-factory, hangar, flightdeck, tower, ai-dlc
#   overrides/main.html:
#     {% extends "base.html" %}
#     {% block announce %}{% include "partials/airframe-suite.html" %}{% endblock %}
# Projects without a fixed layout can use the registry instead: npx shadcn@latest add
# Sean-Koval/agent-factory/airframe#<tag> (see docs/airframe/registry.md).
set -eu

FILES="
airframe.css            docs/stylesheets/airframe.css
airframe-docs.css       docs/stylesheets/airframe-docs.css
airframe-suite.html     overrides/partials/airframe-suite.html
"

ref="${1:-main}"
base="https://raw.githubusercontent.com/Sean-Koval/agent-factory/${ref}/theme"
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# fetch each distinct file once, and fail before touching anything if one is missing
for f in $(printf '%s\n' "$FILES" | awk 'NF {print $1}' | sort -u); do
  code="$(curl -sS -L -o "$tmp/$f" -w '%{http_code}' "$base/$f")" || {
    echo "sync-airframe: could not fetch $base/$f" >&2; exit 1; }
  if [ "$code" != "200" ]; then
    echo "sync-airframe: $base/$f returned HTTP $code (is '$ref' a published ref that has theme/$f?)" >&2; exit 1
  fi
  [ -s "$tmp/$f" ] || { echo "sync-airframe: $base/$f is empty" >&2; exit 1; }
done

printf '%s\n' "$FILES" | awk 'NF {print $1, $2}' | while read -r f dest; do
  mkdir -p "$(dirname "$root/$dest")"
  if cmp -s "$tmp/$f" "$root/$dest"; then
    echo "unchanged  $dest"
  else
    cp "$tmp/$f" "$root/$dest"
    echo "updated    $dest"
  fi
done
