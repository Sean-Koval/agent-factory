#!/bin/sh
# Build the suite site into site/: theme tokens, diagrams, deck, roadmap data, then the docs.
#   sh scripts/build_site.sh            (needs: pip install zensical==0.0.71 playwright)
#   ROADMAP_ARGS=--offline sh scripts/build_site.sh   (skip the GitHub fetch; placeholder roadmap)
set -eu
cd "$(dirname "$0")/.."
python3 scripts/diagrams.py
python3 scripts/build_deck.py
python3 scripts/roadmap.py ${ROADMAP_ARGS:-}
rm -rf docs/theme docs/deck && mkdir -p docs/theme docs/deck && cp theme/*.css docs/theme/
cp deck/index.html docs/deck/index.html
[ -f deck/agent-factory.pdf ] && cp deck/agent-factory.pdf docs/deck/
${ZENSICAL:-zensical} build
