---
hide:
  - toc
---

<span class="af-eyebrow">Airframe</span>

# Components

Airframe has 40 components in ten groups. Each card below is one component: its Night preview, its group and what the preview shows.

[Open the gallery](gallery/){ .md-button .md-button--primary } [Brand book](guide/brand.md){ .md-button }

## Find a component

| Group | Use it for | Components |
| --- | --- | --- |
| [Foundations](#foundations) | The atoms every screen uses. | Avatar, Button, Icons, InlineData, Label, ObjectChip, ProductMarks, Readout, Status |
| [Cards](#cards) | The tonal card and what is built on it. | Card, EnvironmentCard, SummaryCards |
| [Controls](#controls) | Inputs and the message box. | Composer, Controls |
| [Navigation](#navigation) | The app header, product switcher and tabs. | Navigation |
| [Patterns](#patterns) | Page-level recipes. | Dialog, Drawer, EmptyState, PageHeader, Toast |
| [Alerts](#alerts) | The master caution and warning lamps. | MasterCaution |
| [Governance](#governance) | What a person decides. | ApprovalCard, DecisionDeck, Question |
| [Data](#data) | Dense data and evidence. | Diff, FleetTable, Terminal, TraceSpans |
| [Fleet](#fleet) | Agents at work, from one row to the whole console. | ActivityTimeline, AgentCard, AgentRow, FleetBays, FleetColumns, FleetConsole, FleetOwners, FleetView, Heartbeat, SessionLanes, StageRail |
| [Marketing](#marketing) | Home and marketing pages. | Hero |

Open a card for when to use the component, do and don't, what you provide and the markup. The [gallery](gallery/) renders every preview live in both themes.

## All components

--8<-- "airframe-components.md"

## Conventions

Each component is a set of `af-` classes in `theme/airframe-components.css`. Its source is a folder in [`airframe/components/<Name>/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/components) with a README and a `preview.html`.

- **Names are BEM under `af-`.** `af-card__foot`, `af-btn--primary`, `af-status--approval`. State classes are `is-active`, `is-selected`, `is-attention`.
- **Markup is yours.** Airframe ships CSS and one optional helper module, no framework. Render the markup the README shows from whatever your app uses.
- **Helpers are optional.** `airframe.js` builds the same markup with every value escaped (`status()`, `btn()`, `meta()`, `avatar()`, `obj()`). `toast()`, `confirm()`, `drawer`, `expand` and `deck` carry the behaviours.
- **Patterns are components.** The page-level recipes live in `airframe/components/` under the `Patterns` group, with the same README and preview contract.
- **New parts start as tokens.** If a screen needs something the components don't cover, build it from `var(--af-*)` tokens in the tool's own CSS. Propose it here once a second tool needs it.
