# SessionLanes

Session lanes: one row per agent session over the last 60 minutes, showing stages, open PRs, human waits and outcomes up to a brand "now" line.

## What you provide

- A time window (60 min by default) and its axis ticks; the last tick is `now`.
- Per session: tail number, `harness/model`, segments `[kind, start, end]` with kind = `plan | edit | test | pr | wait | queue`, and point markers `[kind, at]` with kind = `fail | deny | merge`.
- Keyed totals for the header (merged, waiting, failed, denied, queued).
- Positions as percentages of the window: `left = (t − t0) / (t1 − t0) × 100%`, `width = (end − start) / (t1 − t0) × 100%`.

## Markup

```html
<div class="af-lanes" role="figure" aria-label="Session lanes, last 60 minutes: 9 sessions, 4 merged, 1 waiting on a human">
  <div class="af-lanes__in">
    <div class="af-lanes__head">
      <span class="af-lanes__title"><svg class="af-ic">…session…</svg><span class="af-lbl">Sessions<span class="af-lbl__sub">last 60 min</span></span></span>
      <span class="af-meta">…merged 4, waiting 1 (--approval), failed 2 (--failed)…</span>
    </div>
    <div class="af-lanes__axis"><span></span><div class="af-viz-axis">
      <span class="af-viz-axis__t" style="left:0%">-60 min</span> … <span class="af-viz-axis__t af-viz-axis__t--now" style="left:100%">now</span>
    </div></div>
    <div class="af-lanes__rows">
      <div class="af-lanes__row">
        <div class="af-lanes__label"><span class="af-lanes__tail">HGR-2D9C</span><span class="af-lanes__who">codex/gpt-5.1</span></div>
        <div class="af-lanes__track">
          <span class="af-lane-seg af-lane-seg--edit" style="left:31.67%;width:26.67%" title="edit, 16 min"></span>
          <span class="af-lane-seg af-lane-seg--pr" style="left:70%;width:5%" title="PR open, 3 min"></span>
          <span class="af-lane-mark af-lane-mark--merge" style="left:75%" role="img" aria-label="merged, 15 min ago"><svg class="af-ic">…check…</svg></span>
        </div>
      </div>
      <i class="af-lanes__now" aria-hidden="true"></i>
    </div>
    <div class="af-lanes__foot af-viz-key">…key items built from the same classes plus --key…</div>
  </div>
</div>
```

## Encoding

| Thing | Class | Drawn as |
|---|---|---|
| Plan, edit, test | `af-lane-seg--plan`, `--edit`, `--test` | `stage-*` greys; later stages carry more ink in both themes |
| PR open | `af-lane-seg--pr` | 1px `fg-muted` outline, no fill |
| Waiting on a human | `af-lane-seg--wait` | orange hatching with an orange outline |
| Queued | `af-lane-seg--queue` | dashed `status-queued` outline |
| Failed | `af-lane-mark--fail` | red triangle |
| Denied | `af-lane-mark--deny` | small red placard |
| Merged | `af-lane-mark--merge` | ring with a check |
| Now | `af-lanes__now` | 1px `brand-text` line with a 5px cap; the axis `now` tick is brand too |

Variants: `af-lanes--compact` (28 px rows, used inside FleetView), `af-lanes--bare` (no panel; for embedding), `af-lanes__row--selected` (brand wash with a 2px `brand-text` marker on the label). Make the label a `<button class="af-lanes__label" aria-pressed>` when rows select something. Segments are split by a 1px gap painted in `--af-lanes-gap` (the panel color); set it when lanes sit on another surface. Add `af-lane-seg--key` / `af-lane-mark--key` to draw a static legend swatch from the same class.

## When to use

History of many sessions at once: the fleet's Lanes view, a pool page, a harness experiment's runs. For one session's turn in detail use TraceSpans.

## Do

- Keep the window fixed while people read it; shift by whole ticks.
- Always draw the legend; stage greys are told apart by order and the key, never alone.
- Put the number of hidden rows in a "Show N more" button rather than shrinking rows.

## Don't

- Don't color stages; only human waits and outcomes take status color.
- Don't draw a "now" line anywhere but the right edge of a live window.
- Don't label segments inside the bar; use `title` and the trace view.
