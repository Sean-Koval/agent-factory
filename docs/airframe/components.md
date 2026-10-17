<span class="af-eyebrow">Airframe</span>

# Components

Each component is a set of `af-` classes in `theme/airframe-components.css`. Its folder in [`airframe/components/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/components) holds a README (what you provide, the markup, when to use it, do and don't) and the `preview.html` the gallery renders.

[Open the gallery](../gallery/){ .md-button .md-button--primary }

--8<-- "airframe-components.md"

## Conventions

- **Names are BEM under `af-`.** `af-card__foot`, `af-btn--primary`, `af-status--approval`. State classes are `is-active`, `is-selected`, `is-attention`.
- **Markup is yours.** Airframe ships CSS only, no framework and no runtime. Render the markup the README shows from whatever your app uses.
- **New parts start as tokens.** If a screen needs something the components don't cover, build it from `var(--af-*)` tokens in the tool's own CSS, then propose it here once a second tool needs it.
