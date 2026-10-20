# FleetOwners

The fleet by person: people down the side, environments across, each person's sandboxes as stand tiles in the cells, with their share of the per-person cap and what they spent today.

> **Default pair (theme-v12).** hangar's Fleet keeps two views over one data model: **List** (AgentRow) and **Board** (AgentCard), with the DecisionDeck above them and Owners as a filter rather than a view. FleetOwners stays in Airframe for other consoles and inherits the same neutral tile and 3px status edge; reach for List/Board first.

## What you provide

- **Columns**: environments, each with its icon (`environment`, or `gpu`) and sandbox count. Set `--af-owners-cols` on `.af-owners__row` when there are not four.
- **Rows**: person (initials, name), active sandboxes against the per-person cap (`6 of 20`), spend today, and how many of theirs need a person.
- **Tiles**: as FleetView's stand tiles (tail, state, stage pips), attention first within a cell.

## Markup

```html
<div class="af-panel af-owners">
  <div class="af-owners__rows">
    <div class="af-owners__row">
      <div class="af-owners__h">Person<small>cap 20 each</small></div>
      <div class="af-owners__h"><svg class="af-ic">…environment…</svg>base-codex<small>12</small></div>
      …
    </div>
    <div class="af-owners__row">
      <div class="af-owners__who">
        <span class="af-person"><span class="af-person__av" aria-hidden="true">SK</span><span class="af-person__name">Sean</span></span>
        <span class="af-cap af-cap--sm"><span class="af-cap__bar" aria-hidden="true"><i style="width:25%"></i></span>5 of 20</span>
        <span class="af-meta"><span class="af-meta__item"><span class="af-meta__key">today</span><span class="af-meta__val">$2.59</span></span></span>
      </div>
      <div class="af-owners__cell"><div class="af-fleet__board"><button type="button" class="af-stand af-stand--approval" …>…</button></div></div>
      <div class="af-owners__cell"><span class="af-owners__none">—</span></div>
      …
    </div>
  </div>
</div>
```

The panel scrolls sideways below about 1040 px. `af-person` and `af-cap` work on their own elsewhere (an owner field, a quota line).

## When to use

Capacity and fairness: who is using the fleet, where, and how close each person is to their cap; the view a lead opens before raising a limit or chasing idle sessions. Use FleetView (Board) for the whole fleet at a glance, FleetBays to read every task, FleetColumns for triage.

## Do

- Keep people in a stable order (alphabetical, or the team list), never by usage.
- Show an em dash in an empty cell so the grid stays readable.
- Count paused sandboxes against the cap (they hold a slot); spun-down ones do not.

## Don't

- Don't color a person or a cap bar as they near the cap; say it in words ("19 of 20") and let a hard stop surface as an approval elsewhere.
- Don't add avatars with photos or product hues; initials in mono only.
