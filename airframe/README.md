# Airframe

The design system for every tool in the suite, and its single source of truth. Docs: <https://sean-koval.github.io/agent-factory/airframe/>; gallery: <https://sean-koval.github.io/agent-factory/airframe/gallery/>.

| Path | What it is |
| --- | --- |
| `tokens.json` | Every color (Night and Day), font, type style, space, radius, layout and icon value, each with a usage note. Change values here and nowhere else. |
| `styles/` | The component CSS (`base.css` atoms, `core.css` console parts, `viz.css` fleet board, lanes, traces, icons). Tokens only: `var(--af-<name>)`, never a color literal. |
| `components/<Name>/` | One folder per component: `README.md` (what you provide, markup, when to use, do and don't) and `preview.html` (rendered in the gallery and on the claude.ai Design System page). |
| `icons/` | 55 icons on a 20 px grid, one file each, the `airframe-icons.svg` sprite and `icons.json`. |
| `guide/` | The brand book: [principles, voice, layout and accessibility](guide/brand.md), [Status](guide/Status.md), [Data](guide/Data.md), [Products](guide/Products.md). |

`python3 scripts/airframe.py build` turns this folder into `theme/airframe.css`, `theme/airframe-components.css`, `theme/airframe-icons.svg` and `theme/airframe-tokens.json`; `check` (in CI) fails when they are stale, when a source has a color literal, or when a `var(--af-*)` is not a token. Every change to `theme/` needs a `theme/CHANGELOG.md` entry, and merging it releases `theme-vN` to the tool repos.

Previews in the gallery and on the claude.ai Design System page are built from these same files. When anything else disagrees with this folder, this folder wins.
