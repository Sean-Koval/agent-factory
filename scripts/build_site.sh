#!/bin/sh
# Build the suite site into site/: Airframe, diagrams, deck, roadmap data, then the docs.
#   sh scripts/build_site.sh            (needs: pip install zensical==0.0.71 playwright)
#   ROADMAP_ARGS=--offline sh scripts/build_site.sh   (skip the GitHub fetch; placeholder roadmap)
set -eu
cd "$(dirname "$0")/.."
python3 scripts/airframe.py check
python3 scripts/airframe.py pages generated
python3 scripts/airframe.py gallery docs/airframe/gallery
python3 scripts/airframe.py registry docs/r
python3 scripts/diagrams.py
python3 scripts/build_deck.py
python3 scripts/roadmap.py ${ROADMAP_ARGS:-}
# The slides go to deck/slides/: docs/deck.md already renders to site/deck/index.html.
rm -rf docs/theme docs/deck && mkdir -p docs/theme docs/deck/slides && cp theme/*.css theme/*.json docs/theme/
cp deck/index.html docs/deck/slides/index.html
mkdir -p docs/deck/slides/captures && cp deck/captures/*.png docs/deck/slides/captures/
# The suite strip partial that overrides/main.html includes is the published theme file.
mkdir -p overrides/partials && cp theme/airframe-suite.html overrides/partials/airframe-suite.html
[ -f deck/agent-factory.pdf ] && cp deck/agent-factory.pdf docs/deck/
${ZENSICAL:-zensical} build
grep -q 'class="slide' site/deck/slides/index.html || {
  echo "build_site: site/deck/slides/index.html is not the slides" >&2; exit 1; }
