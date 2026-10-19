# Icons

The Airframe icon set: 57 stroke glyphs on a 20 px grid, drawn with a 1.5 stroke, square caps and miter joins in `currentColor`.

## What you provide

The glyph's inner markup (from `assets/Icons/icons.json`) or a reference to a sprite symbol, a size class, and an accessible name when the icon is the only label. Color comes from the surrounding text through `currentColor`; never set a fill or a stroke color on the icon itself.

## Markup

```html
<!-- inline: paste the inner markup from icons.json -->
<svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2.5L3.5 6.25V13.75L10 17.5L16.5 13.75V6.25"/><path d="M9.25 9.25h1.5v1.5h-1.5z"/></svg>

<!-- sprite: reference a symbol from assets/Icons/airframe-icons.svg -->
<svg class="af-ic af-ic--20" aria-hidden="true"><use href="/assets/Icons/airframe-icons.svg#af-agent"/></svg>

<!-- an icon that is the only label gets a name -->
<button class="af-btn af-btn--ghost af-btn--sm" aria-label="Copy tail number"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…copy…</svg></button>
```

Sizes: `af-ic` is 16 px (UI default; buttons shrink it to 14 or 13 px), `af-ic--20` for nav and headers, `af-ic--14` for dense rows, `af-ic--24` for empty states. The stroke scales with the size, so 1.5 on the grid is 1.2 px at 16 px.

## The set

| Group | Glyphs |
|---|---|
| Fleet | agent, fleet, sandbox, session, job, environment, harness, model, gpu, pool, region |
| Governance | policy, approval, receipt, denied, caution, secret, egress, lock, user |
| Traces and code | trace, span, tool, terminal, log, duration, cost, database, fork, snapshot, branch, pr, diff, experiment, eval |
| Actions | play, pause, stop, spindown, retry, search, filter, copy, settings, plus, check, close, more, info, chevron-right, chevron-down, arrow-right, sun, moon |
| Agent candidates | agent-alt-1 (orbit), agent-alt-2 (actor), agent-alt-3 (beacon) |

## The agent glyph

The aircraft is retired. `agent` is a hexagonal unit drawn as an open loop around a solid core: a worker in the middle of a task. It holds up at 16 px, it isn't a spinner, a robot face or a sparkle, and hex units tile, so `fleet` is three of them. The other three candidates stay in the set as `agent-alt-1` (a core inside a running orbit), `agent-alt-2` (a pointer with a target) and `agent-alt-3` (a core broadcasting), so the choice can be revisited without redrawing.

Changes from the Lab set: `session` is a speech bubble (a session is a conversation you come back to), `job` is a briefcase (it was a play button in a box), `cost` is two coins (the old cylinder is now `database`). New: lock, user, database, experiment, eval, retry, filter, copy, settings, plus, more, info, the two chevrons and arrow-right. `sun` and `moon` are the theme toggle's two states (Day and Night); a docs site or console shows the one the reader can switch to.

## When to use

- Lead tabs, buttons, section labels and list rows with an icon when it speeds scanning; 16 px beside 13–14 px text, 20 px in the app header.
- Use the status atom (`af-status`), not an icon, to show state. `caution` and `denied` are for rules and docs, not for live status.

## Do

- Let icons inherit color: `fg-subtle` beside labels, `fg` when active, `brand-text` only for a selected item (the selected trace span, the fleet inspector).
- Draw new glyphs on the 20 px grid inside the 2.5–17.5 live area: 1.5 stroke, square caps, miter joins, no fills. The only solid mark is a 1.5 px closed square stroked at 1.5 (cores and dots).
- Give the icon a name (`aria-label` on its button) when there is no visible text.

## Don't

- Don't use `agent-alt-1..3` for the agent in product UI; they are kept for comparison.
- Don't mix in other icon sets, rounded caps, two-tone fills or product hues.
- Don't rotate or mirror glyphs to make new meanings.
