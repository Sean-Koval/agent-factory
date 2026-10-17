# FleetView

The fleet at a glance: every sandbox as a quiet stand tile grouped by pool, switchable to session lanes, with an inspector row for the selected agent.

## What you provide

- **Header**: region (label sub), keyed totals (running, waiting, failed, denied, queued, off) and the pool schedule ("pools up 10:00 · down 01:00").
- **Pools**: name, icon (`environment`, or `gpu` for GPU pools), keyed counts, used and total slots (the cap bar width is `used / total`).
- **Agents**: tail number, state (running, queued, approval, failed, denied, off), stage (plan, edit, test, PR), harness, model, CPU, age, cost. For the Lanes view, each agent's last 60 minutes as SessionLanes segments and markers.
- **Selection**: one selected agent; the inspector shows its details as keyed inline data plus its actions.

## Markup

```html
<div class="af-fleet">                                   <!-- add af-fleet--lanes for the Lanes view -->
  <div class="af-fleet__head">
    <span class="af-fleet__title"><svg class="af-ic">…fleet…</svg><span class="af-lbl">Fleet<span class="af-lbl__sub">us-east4</span></span></span>
    <span class="af-meta">…running 31, waiting 1 (af-meta__item--approval), failed 1 (--failed)…</span>
    <span class="af-fleet__sched"><svg class="af-ic">…spindown…</svg>pools up <b>10:00</b> · down <b>01:00</b></span>
    <span class="af-seg" role="group" aria-label="View">
      <button type="button" class="af-seg__btn" aria-pressed="true">Board</button>
      <button type="button" class="af-seg__btn" aria-pressed="false">Lanes</button>
    </span>
  </div>
  <div class="af-fleet__body">
    <div class="af-fleet__axis af-lanes af-lanes--bare"><!-- SessionLanes axis; shown in Lanes view only --></div>
    <section class="af-fleet__pool" aria-label="base-codex pool">
      <div class="af-fleet__pool-head">
        <svg class="af-ic">…environment…</svg><span class="af-fleet__pool-name">base-codex</span>
        <span class="af-meta">…running 16, waiting 1…</span>
        <span class="af-fleet__cap"><span class="af-fleet__capbar" aria-hidden="true"><i style="width:91.7%"></i></span>22 of 24 slots</span>
      </div>
      <div class="af-fleet__board">
        <button type="button" class="af-stand af-stand--approval" aria-pressed="true" aria-label="HGR-3MX9, Needs approval, PR stage">
          <span class="af-stand__tail">3MX9</span><i class="af-stand__mark"></i>
          <span class="af-stand__pips"><i class="af-stand__pip af-stand__pip--done"></i><i class="af-stand__pip af-stand__pip--done"></i><i class="af-stand__pip af-stand__pip--done"></i><i class="af-stand__pip af-stand__pip--now"></i></span>
        </button>
        <span class="af-stand af-stand--free" aria-hidden="true"></span>
      </div>
      <div class="af-fleet__lanes af-lanes af-lanes--bare af-lanes--compact">
        <div class="af-lanes__rows"><!-- SessionLanes rows, label as <button class="af-lanes__label"> --><i class="af-lanes__now" aria-hidden="true"></i></div>
        <div class="af-lanes__more"><button type="button" class="af-btn af-btn--ghost af-btn--sm" aria-expanded="false">Show 17 more</button></div>
      </div>
    </section>
  </div>
  <div class="af-fleet__inspect" aria-live="polite">
    <span class="af-fleet__who"><svg class="af-ic af-ic--20">…agent…</svg><span class="af-fleet__sel">HGR-3MX9</span><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></span>
    <span class="af-fleet__actions"><button class="af-btn af-btn--primary af-btn--sm">Review</button><button class="af-btn af-btn--secondary af-btn--sm">Open session</button></span>
    <span class="af-meta">…harness, model, stage, held, policy, cpu, age, cost, pool…</span>
  </div>
  <div class="af-viz-key af-fleet__key--board">…status marks, stage pips…</div>
  <div class="af-viz-key af-fleet__key--lanes">…SessionLanes key…</div>
</div>
```

## Tile states

| State | Modifier | Tile | Mark |
|---|---|---|---|
| Running | `af-stand--running` | tonal fill, no border | grey dot |
| Queued | `af-stand--queued` | tonal fill | ring |
| Needs approval | `af-stand--approval` | 1px orange inset ring, faint orange tint | diamond; current pip orange |
| Failed | `af-stand--failed` | 1px red inset ring, faint tint | triangle; current pip red |
| Denied | `af-stand--denied` | 1px red inset ring, faint tint | small placard; current pip red |
| Spun down | `af-stand--off` | hollow, hairline, dim tail | small dot |
| Free slot | `af-stand--free` (a `span`, `aria-hidden`) | dashed outline, empty | none |
| Selected | `aria-pressed="true"` | 1px brand ring outside the tile | unchanged |

Stage pips are four 2 px bars (plan, edit, test, PR): `--done` for finished stages, `--now` for the current one, none for queued and spun-down agents.

## Board and Lanes

Toggle `af-fleet--lanes` on the root and `aria-pressed` on the two `af-seg__btn`s. Both views stay in the DOM so the selection carries across: selecting a lane label selects the same tile and the inspector follows. In Lanes, each pool lists attention first (approval, failed, denied), then running, then queued; show four and put the rest behind "Show N more" (rows with `hidden`). Spun-down agents have no lane.

## When to use

The hangar fleet page, or any overview of up to a few hundred sandboxes where the question is "what needs me, and where is everything". Use FleetTable for a sortable list with columns, SessionLanes alone for history without the board, and TraceSpans for a single turn.

## Do

- Keep the board dark: only approval, failed and denied carry color.
- Show the short tail (last four characters) on the tile and the full tail in `aria-label` and the inspector.
- Keep CPU, cost and age in the inspector, not on tiles.
- Keep the pool order stable; never re-sort tiles while someone is looking.

## Don't

- Don't add borders, meters or sparklines to running tiles.
- Don't use brand yellow for anything except the selection ring, the inspector glyph, the primary action and the "now" line.
- Don't color pools by product hue or by environment.
