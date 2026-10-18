# Airframe theme changelog

Every change to a published theme file (the files generated from `airframe/`, or `airframe-docs.css`) gets an entry here, newest first, under a
new `## theme-vN` heading. Merging it to `main` tags `theme-vN` and opens a sync pull request in
each tool repo (hangar, flightdeck, ai-dlc, Tower), or prints the one-command sync when the
workflow has no cross-repo token. Keep token names stable; list each token whose value changed.

## theme-v3 · 2026-10-17

Fleet views: the same sandboxes four ways, chosen by Sean from the fleet layout study. No token
values change.

- `airframe-components.css` gains three components and their shared parts:
  - FleetBays (`af-bays`, `af-bay`): a box per sandbox with its task, owner, harness, a labeled
    stage track, lease left and one action; dashed "Start in …" bay per environment.
  - FleetColumns (`af-statecols`, `af-statecol`, `af-mini`): one column per state, attention
    first, Running two wide, sticky heads.
  - FleetOwners (`af-owners`): people down, environments across, stand tiles in the cells, with
    each person's share of the per-person cap.
  - Shared: `af-cap` (capacity bar), `af-track` (labeled plan / edit / test / PR track),
    `af-person` (initials and name).
- `af-seg__btn` also styles links: `aria-current="page"` reads as pressed, so a segmented switch
  can move between pages or views.
- Brand book: Tower's tail-number prefix is `TWR-` (`TWR-APR-0391`, `TWR-RCPT-88A1`), replacing
  `WS-` from the governed-workspace name.

## theme-v2 · 2026-10-17

Airframe's full system moves here and becomes the source of truth. Values now live in
`airframe/tokens.json` and the component CSS in `airframe/styles/`; `scripts/airframe.py build`
generates `theme/airframe.css` from them (no longer hand-written) and three new published files.
This is the system on the claude.ai Design System page, which is now a viewer of this repo.

New published files (tool repos vendor the ones they need):

- `airframe-components.css`: the `af-` component classes (buttons, statuses, cards, tables,
  navigation, master caution, approval card, terminal, fleet board and table, session lanes,
  trace spans, readouts, product marks, icons) and the `.af-type-<style>` type classes.
- `airframe-icons.svg`: the 55-icon sprite (`#af-<name>`); `agent` is a hex unit, not a plane.
- `airframe-tokens.json`: tokens resolved per theme, for diagrams, decks and charts.

Renamed tokens (the theme-v1 names stay as aliases in every theme scope; new code uses the new names):

- `--af-st-run|queue|appr|fail|deny|off` → `--af-status-running|queued|approval|failed|denied|off`
- `--af-p-hangar|flightdeck|aidlc|spaceport` → `--af-product-…`; `--af-p-workspace` → `--af-product-tower`
- `--af-term-bg|fg` → `--af-terminal-bg|fg`; `--af-code-k|f|s|n|c` → `--af-code-keyword|function|string|number|comment`
- `--af-dot` → `--af-dot-field`; `--af-f-display|sans|mono` → `--af-font-display|sans|mono`
- `--af-r-ctl`, `--af-r-chip` → `--af-radius-control`; `--af-r-card` → `--af-radius-card`; `--af-pad` → `--af-space-16`; `--af-gap` → `--af-space-12`

Changed values, Night (`dark`):

- `--af-line-subtle` `#161616` → `#1F1F1F` and `--af-line` `#1F1F1F` → `#2A2A2A` (dividers were invisible on raised cards)
- `--af-rule` `#3A3A3A` → `#424242`
- `--af-status-approval` (was `--af-st-appr`) `#FFB224` → `#FF8A3D`: caution is orange so it can never read as the brand yellow

Changed values, Day (`light`): paper-grey page with white cards (theme-v1 had a white page with grey cards):

- `--af-canvas` `#FFFFFF` → `#F4F4F2`; `--af-surface` `#F8F8F7` → `#EDEDEB`; `--af-raised` `#F1F1F0` → `#FFFFFF`; `--af-selected` `#E8E8E7` → `#E6E6E3`
- `--af-line-subtle` `#EDEDED` → `#E6E6E3`; `--af-line` `#E0E0E0` → `#DCDCD9`; `--af-line-strong` `#858585` → `#858583`; `--af-rule` `#C9C9C9` → `#BDBDBA`
- `--af-fg` `#000000` → `#0A0A0A`; `--af-fg-muted` `#4D4D4D` → `#474746`; `--af-fg-subtle` `#6B6B6B` → `#666664`; `--af-fg-dim` `#A3A3A3` → `#9C9C99`
- `--af-brand-wash` `.16` → `.18` alpha; `--af-status-queued` `#6B6B6B` → `#666664`; `--af-status-approval` `#9A5B00` → `#B04E00`; `--af-status-off` `#858585` → `#858583`; `--af-dot-field` `#E0E0E0` → `#DCDCD9`

New tokens: `on-status-denied`, `lamp-caution`, `lamp-warning`, `on-lamp`, `terminal-dim|ok|err`,
`span-model|tool|sandbox`, `stage-plan|edit|test`, `readout-cell`, `display-window`, `chart-1…6`,
`shadow-overlay`, the `space-*` scale (2 to 160), `radius-none`, `radius-round`, `container-max`,
`header-h`, `row-h-compact`, `lane-h`, `span-h`, `icon-stroke`, `icon-size`.

Theme scopes: `data-theme` now works on any element (nested scopes), not only `<html>`.

`airframe-docs.css`:

- Token references use the new names.
- Table headers have no fill: mono capitals over a 1px `--af-line` rule.
- The product hue comment now declares `--af-product` on `[data-md-color-scheme]` too, so the Day hue follows a theme switch.

## theme-v1 · 2026-10-17

First tagged release: the "Night Panel" flavor (black canvas, signal-yellow accent, Archivo
Expanded display, Red Hat Text body, DM Mono labels, 2px radius, quiet status colors).
Changes since the copy the tool repos first vendored:

- `airframe.css`, light theme (both the `prefers-color-scheme` block and `[data-theme="light"]`):
  - `--af-surface` `#F7F7F7` → `#F8F8F7`
  - `--af-raised` `#FFFFFF` → `#F1F1F0` (tonal cards instead of white-on-white)
  - `--af-selected` `#EBEBEB` → `#E8E8E7`
- `airframe-docs.css`:
  - Footer sits on the canvas with a top rule (`.md-footer`, `.md-footer-meta`, `.md-copyright`).
  - `figure.af-figure` spans the full column; its SVG or image scales to width; captions upright.
