#!/bin/sh
# Build the suite site into site/: theme tokens, diagrams, deck, then the docs.
#   sh scripts/build_site.sh            (needs: pip install zensical==0.0.71 playwright)
set -eu
cd "$(dirname "$0")/.."
python3 scripts/diagrams.py
python3 scripts/build_deck.py
rm -rf docs/theme docs/deck && cp -R theme docs/theme && mkdir -p docs/deck
cp deck/index.html docs/deck/index.html
[ -f deck/agent-factory.pdf ] && cp deck/agent-factory.pdf docs/deck/
${ZENSICAL:-zensical} build
