<span class="af-eyebrow">Design system</span>

# Airframe

Airframe is the one design system for every tool in the suite: the hangar console, Tower, the five docs sites, the deck and the diagrams. It works like a dark cockpit. The screen stays black, white and grey while agents work. One signal yellow marks what is yours to act on, and color appears only when something needs a person.

This repository is its single source of truth. Every color, size and font is a token in [`airframe/tokens.json`](https://github.com/Sean-Koval/agent-factory/blob/main/airframe/tokens.json); every component is a class in [`airframe/styles/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/styles). A tool never invents its own palette. It loads Airframe at a tagged version and builds with its classes.

[Open the component gallery](gallery/){ .md-button .md-button--primary } [Tokens](tokens.md){ .md-button } [Components](components.md){ .md-button } [Icons](icons.md){ .md-button }

## The rules

<div class="af-rules">
  <div class="af-rule"><b>Quiet until a human is needed</b><span>Running is a grey dot. Only needs approval (orange diamond), failed (red triangle) and denied (red placard) carry color. A screen with no color on it means nobody is needed.</span></div>
  <div class="af-rule"><b>Yellow is your action, never a status</b><span>The brand fill marks the primary action, focus, the selected item and the trace's critical path. Caution is orange so it can never be mistaken for it.</span></div>
  <div class="af-rule"><b>Tonal, not boxed</b><span>Cards are a raised tone on the canvas with no border and no shadow. Dividers inside them are faint. No gloss, glow, blur or gradients.</span></div>
  <div class="af-rule"><b>Color, shape and a word</b><span>Every status has all three, so it reads in grayscale, for color-blind readers and on a projector.</span></div>
  <div class="af-rule"><b>Three faces</b><span>Archivo Expanded for headlines, Red Hat Text for reading, DM Mono for IDs, data, labels and buttons. Numbers use tabular figures.</span></div>
  <div class="af-rule"><b>Keyed data</b><span>Metadata reads <code>POLICY require-approval-main-push  MODEL gpt-5.1</code>: a small mono key, then the value. Never "a · b · c".</span></div>
</div>

Two themes share every component: **Night** (`dark`, the default, true black) and **Day** (`light`, paper grey, white cards). The [brand book](guide/brand.md) (voice, layout, accessibility) is here, with [Status](guide/status.md), [Data](guide/data.md) and [Products](guide/products.md); the source is [`airframe/guide/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/guide).

## What a tool loads

Everything a tool loads is in `theme/`:

| File | What it is | Who loads it |
| --- | --- | --- |
| `airframe.css` | Every token as `--af-<name>`, Night and Day. Generated. | Everything |
| `airframe-components.css` | The `af-` classes for every component on the [Components](components.md) page, plus the fonts. Generated. | Consoles and web apps |
| `airframe-docs.css` | Maps the docs theme (Zensical / Material) onto the tokens, from the header to the home hero and the suite strip. Generated from `airframe/docs-site/`. | Docs sites |
| `airframe-suite.html` | The suite strip above the docs header: the family's docs sites, with the product marker under the current one. A template partial, rendered by the docs theme. Generated from `airframe/docs-site/`. | Docs sites |
| `airframe-icons.svg` | The icon sprite: `<svg class="af-ic"><use href="airframe-icons.svg#af-agent"/></svg>`. Generated. | Consoles and web apps |
| `airframe.js` | Optional. One ES module, no dependencies: markup helpers that match the contracts, and the toast, confirm and drawer behaviours. Copied from `airframe/js/`. | Consoles and web apps |
| `airframe-tokens.json` | Tokens resolved per theme, for scripts that draw (diagrams, decks, charts). Generated. | Build scripts |

A page is themed by `data-theme="dark"` or `data-theme="light"` on `<html>` (or any element, for a nested scope). With neither, Day follows the reader's OS setting and Night is the fallback.

```html
<html data-theme="dark">
<link rel="stylesheet" href="airframe/airframe.css">
<link rel="stylesheet" href="airframe/airframe-components.css">

<article class="af-card">
  <div class="af-card__top">
    <span class="af-lbl">Sandbox<span class="af-lbl__sub">us-east4</span></span>
    <span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span>
  </div>
  <span class="af-id">HGR-3MX9</span>
  <div class="af-card__foot"><span>Held <b>41 min</b></span><button class="af-btn af-btn--primary af-btn--sm">Review</button></div>
</article>
```

## The docs sites

Every product's docs site is Material for MkDocs or Zensical with three vendored files and a few lines of config. The five sites read as one family. The same header with the product's mark and hue, the same home hero and page anatomy, and the suite strip that links them.

1. Vendor `airframe.css`, `airframe-docs.css` and `airframe-suite.html` with `scripts/sync-airframe.sh theme-vN` (the template lists the destinations: `docs/stylesheets/` and `overrides/partials/`).
2. In `mkdocs.yml`: `theme.logo` and `theme.favicon` are the product's `mark.svg` and `favicon.svg` from [`brand/`](https://github.com/Sean-Koval/agent-factory/tree/main/brand). `extra_css` loads `airframe.css`, `airframe-docs.css`, then the site's own one-line `product.css` (`:root, [data-md-color-scheme] { --af-product: var(--af-product-hangar); }`). `theme.custom_dir: overrides`, and `extra.airframe.product: hangar` names the current item in the strip.
3. `overrides/main.html`, the one template a site owns, is two lines:

    ```jinja
    {% extends "base.html" %}
    {% block announce %}{% include "partials/airframe-suite.html" %}{% endblock %}
    ```

The home page is an `af-hero`: an `af-eyebrow`, one display headline, one `af-lede` and two `md-button`s (one primary). With `af-hero--visual`, a `figure.af-hero__visual` holds a real capture of the product. Every other page is a title, one sentence styled as the lede, sections, and a "See also" list.

## How the tools stay in sync

Each tool repo **vendors** the files it needs, unmodified, with its own `scripts/sync-airframe.sh <tag>`, and never edits them. Its own CSS uses `var(--af-*)` tokens and `af-` classes only; a test in each repo fails on a hard-coded color.

Each repo's `AGENTS.md` points coding agents here, so an agent asked to build a screen reads Airframe first.

1. Change a value in `airframe/tokens.json` or a component in `airframe/styles/`.
2. Run `python3 scripts/airframe.py build`; it regenerates `theme/`. `python3 scripts/airframe.py check` (run in CI) fails if `theme/` is stale, a source uses a color literal, or a `var(--af-*)` is not a token.
3. Add a `## theme-vN` entry to [`theme/CHANGELOG.md`](https://github.com/Sean-Koval/agent-factory/blob/main/theme/CHANGELOG.md) listing each changed token. The `theme` workflow refuses a theme change without one.
4. Merging tags `theme-vN` and opens a sync pull request in hangar, flightdeck, ai-dlc and Tower (or prints the one-command `sh scripts/theme_sync.sh theme-vN`).

Token names are a contract: rename only with an alias. The theme-v1 names (`--af-st-appr`, `--af-p-hangar`, `--af-f-mono` and the rest) still resolve, and new code uses the full names.

## Where else Airframe shows up

- **The deck** reads `theme/airframe.css`; `python3 scripts/build_deck.py --pdf` rebuilds it.
- **Diagrams** use `var(--af-*)` with the Night value as fallback, from `theme/airframe-tokens.json`, so an inlined diagram follows the page theme.
- **The Design System page on claude.ai** shows the same components for design reviews. It is a viewer; when it and this repository disagree, this repository wins.
