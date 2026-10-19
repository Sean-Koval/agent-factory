# Repository guidance

agent-factory is the suite-level home for hangar, flightdeck, ai-dlc, Tower and Spaceport: the docs site, the deck, the architecture diagrams, a pointer to the example team harness ([Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness)), and **Airframe**, the design system every tool uses.

## Airframe is the design source of truth

- Values live in `airframe/tokens.json`; component CSS in `airframe/styles/`; per-component docs and previews in `airframe/components/<Name>/`; icons in `airframe/icons/`; the brand book in `airframe/guide/`. Read `airframe/README.md` and `airframe/guide/brand.md` before any visual work, here or in a tool repo.
- `theme/airframe.css`, `theme/airframe-components.css`, `theme/airframe-icons.svg`, `theme/airframe.js`, `theme/airframe-tokens.json`, `theme/airframe-tailwind.css`, `theme/airframe.tokens.json`, `theme/airframe-day.tokens.json`, `theme/airframe-docs.css` and `theme/airframe-suite.html` are generated. Never edit them; change `airframe/` (`styles/`, `js/airframe.js`, `icons/`, `docs-site/`, `tokens.json`) and run `python3 scripts/airframe.py build`.
- Components live in `airframe/components/<Name>/` with a README (what you provide, markup, states, do and don't) and a `preview.html` whose first line is the `<!-- @dsCard group=... -->` marker; page-level recipes (page header, empty state, toast, dialog, drawer) are components in the `Patterns` group. Every stylesheet in `airframe/styles/` ends with an `@media (forced-colors: active)` block in system colors. `airframe/js/airframe.js` is the one optional script: framework-free ES module, no dependencies, no build step, no Web Components.
- `registry.json` at the repo root is the shadcn-compatible registry (universal items with `~/` targets, pointing at files in `theme/`, `airframe/components/`, `registry/` and `.claude/skills/`). `scripts/airframe.py registry DIR` builds the served JSON; `check` validates it. The skill in `.claude/skills/airframe/` is what the `skill` item installs, so it must list every component.
- CSS, HTML, the deck and diagrams use `var(--af-<name>)` tokens and `af-` classes, never a color literal. `python3 scripts/airframe.py check` and `tests/test_airframe.py` enforce it, along with the contrast floor.
- Token names are a contract with the tool repos: rename only by adding an alias in `ALIASES` (`scripts/airframe.py`).
- Any change under `theme/` needs a new `## theme-vN` entry in `theme/CHANGELOG.md` listing each changed token. Merging releases it to the tool repos (`.github/workflows/theme.yml`).
- The brand yellow is never a status; color appears only when a person is needed (see `airframe/guide/Status.md`). Diffs are greyscale (`guide/Data.md`); a deny needs a reason; waiting on others stays grey; a question is the approval role with the word "Needs input".

## Checks

```sh
python3 scripts/airframe.py check
python3 -m unittest discover -s tests
python3 scripts/diagrams.py && git diff --exit-code -- docs/assets/diagrams/*.svg
python3 scripts/build_deck.py && git diff --exit-code -- deck/index.html
ROADMAP_ARGS=--offline sh scripts/build_site.sh
```

Use conventional commit prefixes (`feat:`, `fix:`, `docs:`, `style:`).

## Tracking

- Work is tracked in Jira project KAN (<https://seanmkoval.atlassian.net>). GitHub Projects is retired; GitHub Issues are for outside reports only.
- Work tied to a ticket carries its key, so the GitHub for Jira app links it: the branch starts with it (`KAN-35-apply-atomic`), the PR title starts with it (`KAN-35: make hangar apply all or nothing`) and the PR body has a `Jira: KAN-35` line. Commits may mention it. Work without a ticket (typo fixes, outside contributions) needs no key.
- Lanes: only `lane:agent` tickets (job-sized: one repo or one change-set profile, acceptance criteria, a verify command) start a hangar job, when moved to "Ready for agent". `lane:pair` is Sean with Claude Code; `lane:human` is Sean only.
