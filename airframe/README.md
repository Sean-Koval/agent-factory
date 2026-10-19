# Airframe

The design system for every tool in the suite, and its single source of truth. Docs: <https://sean-koval.github.io/agent-factory/airframe/>; gallery: <https://sean-koval.github.io/agent-factory/airframe/gallery/>.

| Path | What it is |
| --- | --- |
| `tokens.json` | Every color (Night and Day), font, type style, space, radius, layout and icon value, each with a usage note. Change values here and nowhere else. |
| `styles/` | The component CSS (`base.css` atoms, `core.css` console parts, `agents.css` the approval decisions, question, composer, diff and object chip, `patterns.css` page header, empty state, toast, dialog and drawer, `viz.css` fleet board, lanes, traces, icons). Tokens only: `var(--af-<name>)`, never a color literal. |
| `js/airframe.js` | The one optional script: an ES module with no dependencies and no build step. Markup helpers that match the contracts (`status`, `icon`, `meta`, `btn`, `avatar`, `obj`, `tag`) and three behaviours (`toast`, `confirm`, `drawer`), with alert inhibition. Published as `theme/airframe.js`. |
| `components/<Name>/` | One folder per component: `README.md` (what you provide, markup, when to use, do and don't) and `preview.html` (rendered in the gallery and on the claude.ai Design System page). |
| `icons/` | 55 icons on a 20 px grid, one file each, the `airframe-icons.svg` sprite and `icons.json`; `marks.json` holds the six product marks. |
| `fonts/` | The three families as small static files, for generating assets whose text must be outlines (banners). Sites load the families from Google Fonts. |
| `docs-site/` | The docs sites' look: `airframe-docs.css` maps Material for MkDocs / Zensical onto the tokens (with its own forced-colors block), and `airframe-suite.html` is the suite strip above every docs header. |
| `guide/` | The brand book: [principles, voice, layout and accessibility](guide/brand.md), [Status](guide/Status.md), [Data](guide/Data.md), [Products](guide/Products.md). |

`python3 scripts/airframe.py build` turns this folder into `theme/airframe.css`, `theme/airframe-components.css`, `theme/airframe-icons.svg`, `theme/airframe.js` and `theme/airframe-tokens.json`, plus three exports for other toolchains: `theme/airframe-tailwind.css` (a Tailwind CSS v4 `@theme` over the tokens) and `theme/airframe.tokens.json` / `theme/airframe-day.tokens.json` (the W3C Design Tokens format, one file per theme); `check` (in CI) fails when they are stale, when a source has a color literal, or when a `var(--af-*)` is not a token. `docs-site/` holds the docs-site mapping (`airframe-docs.css`) and the suite strip partial (`airframe-suite.html`), published as `theme/airframe-docs.css` and `theme/airframe-suite.html` by the same build (see [the docs sites](https://sean-koval.github.io/agent-factory/airframe/#the-docs-sites)). Every change to `theme/` needs a `theme/CHANGELOG.md` entry, and merging it releases `theme-vN` to the tool repos.

`python3 scripts/banners.py` turns the tokens, the marks and the fonts into each product's brand surfaces in [`brand/`](../brand/README.md): README banner, social preview, favicon and header mark.

`registry.json` at the repository root publishes the same files, the component contracts, a React wrapper set and the agent skill as a shadcn-compatible registry (`npx shadcn@latest add Sean-Koval/agent-factory/airframe#theme-vN`, or `<docs site>/r/<item>.json`); see the [Registry](https://sean-koval.github.io/agent-factory/airframe/registry/) page.

Previews in the gallery and on the claude.ai Design System page are built from these same files. When anything else disagrees with this folder, this folder wins.
