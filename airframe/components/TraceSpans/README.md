# TraceSpans

One agent turn as a span tree on a timeline: kinds told apart by fill and outline, the critical path as a continuous brand line, and a detail panel for the selected span.

## What you provide

- **Header**: label sub (`turn 7`) and keyed totals: session tail, active time, spans, tokens, cost, status.
- **Spans in tree order**: name, kind (`turn | model | tool | sandbox | wait`), depth (0–3), start and end in seconds (or open), a failed flag, an on-critical-path flag, and an icon (`session`, `model`, `tool` / `search` / `diff`, `terminal`, `approval`).
- **Detail** for each span: attributes as key/value pairs and, when there is one, an output block (terminal text with dim, ok and error runs).

## Markup

```html
<div class="af-trace">
  <div class="af-trace__body">
    <div class="af-trace__main"><div class="af-trace__in">
      <div class="af-trace__head"><span class="af-trace__title"><svg class="af-ic">…trace…</svg><span class="af-lbl">Trace<span class="af-lbl__sub">turn 7</span></span></span><span class="af-meta">…</span></div>
      <div class="af-trace__grid">
        <div class="af-trace__axis"><span></span><div class="af-viz-axis">…0s … 60s…</div><span class="af-trace__dh">Duration</span></div>
        <button type="button" class="af-trace__row af-trace__row--d1 af-trace__row--failed" aria-pressed="true">
          <span class="af-trace__name"><svg class="af-ic">…terminal…</svg><span class="af-trace__label">run_tests</span><span class="af-trace__kind">sandbox</span></span>
          <span class="af-trace__lane"><span class="af-span af-span--failed" style="left:35%;width:23.333%"></span></span>
          <span class="af-trace__dur">14.0 s</span>
        </button>
        <svg class="af-trace__path" viewBox="0 0 100 280" preserveAspectRatio="none" style="height:280px" aria-hidden="true"><path d="M0.667 49H11.5V133H17 …"/></svg>
      </div>
      <div class="af-trace__foot af-viz-key">…key…</div>
    </div></div>
    <aside class="af-trace__side" aria-live="polite" aria-label="Span detail">
      <h3 class="af-trace__side-title"><svg class="af-ic">…</svg><span>run_tests</span></h3>
      <span class="af-meta">…kind, start, duration, status…</span>
      <dl class="af-kv"><dt>command</dt><dd class="af-mono">pnpm test auth</dd>…</dl>
      <div class="af-trace__out-label">Sandbox output</div>
      <pre class="af-trace__out"><span class="af-trace__out-dim">$</span> pnpm test auth
<span class="af-trace__out-err">✗</span> refresh › rotates token after expiry</pre>
    </aside>
  </div>
</div>
```

**Critical path**: an SVG over the timeline column with `viewBox="0 0 100 <rows × 28>"` and `preserveAspectRatio="none"` (the stroke stays 1.5 px through `vector-effect`). For the critical spans in order, draw `M start y H end`, then `V nextY H nextStart H nextEnd`, where x is the percentage of the window and `y = rowIndex × 28 + 21` (2 px under the bar).

## Encoding

| Kind | Class | Drawn as |
|---|---|---|
| Model call | `af-span--model` | solid `span-model` |
| Tool call | `af-span--tool` | 1px `span-tool` outline with a faint fill, 8 px tall |
| Sandbox command | `af-span--sandbox` | solid `span-sandbox`, mid grey |
| Turn | `af-span--turn` | bracket line in `fg-subtle` |
| Waiting on a human | `af-span--wait af-span--open` | orange hatching, open arrow at the right edge; duration in orange |
| Failed | `af-span--failed` + `af-trace__row--failed` | red outline with a triangle after it; duration in red |
| Critical path | `af-trace__path` | continuous 1.5 px `brand-text` line |
| Selected | `aria-pressed="true"` on the row | `brand-wash` row, icon in `brand-text` |

Depth: `af-trace__row--d1..d3` indents 16 px a level and draws the tree elbow. Add `af-span--key` to draw a legend swatch from the same class.

## Interaction

Rows are buttons with `aria-pressed`; one is selected at a time and the side panel (`aria-live="polite"`) re-renders for it. Below 900 px of container width the panel drops under the timeline.

## When to use

A single turn or job of one agent: what ran, in what order, what was slow, what failed, what is waiting. For many sessions over time use SessionLanes.

## Do

- Keep span names as the agent or tool reported them (`read_file ×4`, `apply_patch`), in tree order.
- Show the turn as open while anything in it is waiting, and say what it waits for.
- Keep terminal output dark in both themes.

## Don't

- Don't color kinds; model, tool and sandbox are told apart by fill, outline and tone.
- Don't use brand yellow for anything but the critical path and the selection.
- Don't hide failed spans when collapsing the tree.
