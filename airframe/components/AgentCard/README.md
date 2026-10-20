# AgentCard

The board card: the same `af-agent` as AgentRow, laid out as a tile for a grid. The harness as a hexagonal avatar, the tail, a stage ring in the corner, the work (two lines at most), the now-line, a capsule, and a foot with the owner and either the status word (when a person is needed or the agent stopped) or the heartbeat.

## What you provide

The same per-agent data as AgentRow; the card shows less of it (no model, no stage times, no sparkline, no cost) and the console shows the rest when it opens.

## Markup

```html
<div class="af-board" role="group">
  <article class="af-agent af-agent--card af-agent--lit" data-id="HGR-3MX9">
    <button type="button" class="af-agent__face" aria-expanded="false" aria-label="HGR-3MX9, Needs approval, Push the refunds migration to main">
      <span class="af-agent__hd"><span class="af-avatar af-avatar--agent af-avatar--22">cx</span><span class="af-agent__tail">3MX9</span><svg class="af-ring af-ring--approval">…</svg></span>
      <span class="af-agent__work">Push the refunds migration to main</span>
      <span class="af-agent__now">waiting on you: push to main</span>
      <span class="af-capsule af-capsule--approval">…</span>
      <span class="af-agent__ft"><span class="af-avatar af-avatar--person af-avatar--22">SK</span><span>Sean</span><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></span>
    </button>
    <div class="af-agent__body"><div><!-- af-console when open --></div></div>
  </article>
</div>
```

| Part | Class | Notes |
|---|---|---|
| Grid | `af-board` | `auto-fill, minmax(228px, 1fr)`, 10 px gap; two columns below 760. |
| Card | `af-agent af-agent--card` | Everything the row has (edge, hover, lifted open state); hover also lifts it 1 px. `is-open` spans the whole grid row. |
| Face | `af-agent__face` | A `button`, 138 px min; `__hd` (avatar, tail, ring pushed right), `__work` (clamped to two lines), `__now`, `af-capsule`, `__ft`. When open the face becomes one line (avatar, tail, work, capsule, foot) above the console. |
| Foot | `af-agent__ft` | The owner, then the status word in its color for a lit or stopped card, else the heartbeat. The denied placard keeps its own colors. |

## When to use

hangar's Fleet in its Board view, and a dashboard that shows a few agents as tiles. The Owners view (FleetOwners) and Columns (FleetColumns) keep their smaller tiles; this card is for a grid where the work's title should be readable.

## Do

- Keep every card the same height in a row; the foot pins to the bottom.
- Let the ring carry the stage and the capsule the progress; the two agree.

## Don't

- Don't put more than the title, the now-line and the owner on the face; the console holds the rest.
- Don't use a status color on the face except the ring's current arc, the capsule's current segment, the edge and the status word.
