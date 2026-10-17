# Repository guidance

agent-factory is the suite-level home for hangar, flightdeck, ai-dlc, Tower and Spaceport: the docs site, the deck, the architecture diagrams, the example team harness, and **Airframe**, the design system every tool uses.

## Airframe is the design source of truth

- Values live in `airframe/tokens.json`; component CSS in `airframe/styles/`; per-component docs and previews in `airframe/components/<Name>/`; icons in `airframe/icons/`; the brand book in `airframe/guide/`. Read `airframe/README.md` and `airframe/guide/brand.md` before any visual work, here or in a tool repo.
- `theme/airframe.css`, `theme/airframe-components.css`, `theme/airframe-icons.svg` and `theme/airframe-tokens.json` are generated. Never edit them; change `airframe/` and run `python3 scripts/airframe.py build`.
- CSS, HTML, the deck and diagrams use `var(--af-<name>)` tokens and `af-` classes, never a color literal. `python3 scripts/airframe.py check` and `tests/test_airframe.py` enforce it, along with the contrast floor.
- Token names are a contract with the tool repos: rename only by adding an alias in `ALIASES` (`scripts/airframe.py`).
- Any change under `theme/` needs a new `## theme-vN` entry in `theme/CHANGELOG.md` listing each changed token. Merging releases it to the tool repos (`.github/workflows/theme.yml`).
- The brand yellow is never a status; color appears only when a person is needed (see `airframe/guide/Status.md`).

## Checks

```sh
python3 scripts/airframe.py check
python3 -m unittest discover -s tests
python3 scripts/diagrams.py && git diff --exit-code -- docs/assets/diagrams/*.svg
python3 scripts/build_deck.py && git diff --exit-code -- deck/index.html
ROADMAP_ARGS=--offline sh scripts/build_site.sh
```

Use conventional commit prefixes (`feat:`, `fix:`, `docs:`, `style:`).
