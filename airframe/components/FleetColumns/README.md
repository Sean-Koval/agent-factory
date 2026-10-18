# FleetColumns

The fleet sorted by state: one column each for Needs you, Failed or denied, Running (two wide), Starting and Paused, so the work that needs a person is always the first thing on the left.

## What you provide

- **Columns**: name, the status role its head shows (`approval`, `failed`, `running`, `queued`, `off`), count, and the empty text ("Nothing is waiting on you.").
- **Per card**: tail number, environment, the work, stage (plan, edit, test, PR or none), owner and harness, age; for attention cards the reason and one action.

## Markup

```html
<div class="af-statecols">
  <section class="af-statecol" aria-label="Needs you">
    <div class="af-statecol__head"><span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>Needs you</span><span class="af-statecol__count">2</span></div>
    <div class="af-statecol__list">
      <article class="af-mini af-mini--approval" aria-label="HGR-3MX9, Needs approval">
        <div class="af-mini__top"><b>HGR-3MX9</b><span>base-codex</span></div>
        <p class="af-mini__title">Push the refunds migration to main</p>
        <span class="af-stand__pips" aria-hidden="true"><i class="af-stand__pip af-stand__pip--done"></i>…<i class="af-stand__pip af-stand__pip--now"></i></span>
        <div class="af-mini__top"><span>sean · codex</span><span>41 min</span></div>
        <p class="af-bay__note">Push to main held by require-approval-main-push.</p>
        <div><button type="button" class="af-btn af-btn--primary af-btn--sm">Review the push</button></div>
      </article>
    </div>
  </section>
  <section class="af-statecol af-statecol--wide" aria-label="Running">…</section>
</div>
```

Card states mirror FleetBays: `af-mini--queued`, `--approval` (orange ring), `--failed` and `--denied` (red ring), `--off` (hollow), `is-selected` (brand ring). Column heads stay sticky while the page scrolls. Below 1100 px the columns fold to two, and to one on a phone.

## When to use

Triage: when the question is "what needs me, what broke" rather than "where is everything". It is the best view to leave open on a second screen. Use FleetView (Board) for the whole fleet at a glance, FleetBays to read every task, FleetOwners for capacity by person.

## Do

- Keep the column order fixed and attention first; show empty columns with their empty text rather than hiding them.
- Give each attention card its reason and exactly one action.
- Sort Running by environment, then age, so cards do not jump while someone reads.

## Don't

- Don't color the Running, Starting or Paused heads; their marks are grey.
- Don't add a column per environment here; that is the Board's job.
- Don't use a primary button outside the Needs you column.
