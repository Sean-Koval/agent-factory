---
hide:
  - toc
---

<span class="af-eyebrow">Airframe</span>

# Components

Each card is one component: its Night preview, its group and what the preview shows. Open one for when to use it, do and don't, what you provide and the markup; the [gallery](gallery/) renders every preview live in both themes. Each component is a set of `af-` classes in `theme/airframe-components.css`, kept in [`airframe/components/<Name>/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/components) with its README and `preview.html`.

[Open the gallery](gallery/){ .md-button .md-button--primary } [Brand book](guide/brand.md){ .md-button }

--8<-- "airframe-components.md"

## Conventions

- **Names are BEM under `af-`.** `af-card__foot`, `af-btn--primary`, `af-status--approval`. State classes are `is-active`, `is-selected`, `is-attention`.
- **Markup is yours.** Airframe ships CSS and one optional helper module, no framework. Render the markup the README shows from whatever your app uses, or build it with `airframe.js` (`status()`, `btn()`, `meta()`, `avatar()`, `obj()`), which returns the same markup with every value escaped; `toast()`, `confirm()` and `drawer` carry the three behaviours that are the pattern.
- **Patterns are components.** The page-level recipes (page header, empty state, toast, dialog, drawer) live in `airframe/components/` under the `Patterns` group with the same README and preview contract.
- **New parts start as tokens.** If a screen needs something the components don't cover, build it from `var(--af-*)` tokens in the tool's own CSS, then propose it here once a second tool needs it.
