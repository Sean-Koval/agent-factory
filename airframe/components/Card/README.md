Cards are tonal: a `raised` block with a 4 px radius and 16 px padding, no border and no shadow, separated from the canvas by tone and from each other by a 12 px gap.

## You provide
- A top row: a label (with optional icon and sub) on the left; meta text or a status on the right.
- A body: title, description, inline data, readouts or a short list.
- Optionally a foot: a summary on the left and one link or small button on the right.

## Markup
```html
<article class="af-card">
  <div class="af-card__top">
    <span class="af-lbl"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg>Session<span class="af-lbl__sub">turn 7</span></span>
    <span class="af-card__meta">2 min ago</span>
  </div>
  <div class="af-card__body">
    <h3 class="af-card__title">Fix the flaky auth refresh test</h3>
    <p class="af-card__desc">Freeze the clock in the test instead of the code.</p>
    <span class="af-meta">…</span>
  </div>
  <div class="af-card__foot"><span class="af-status af-status--running"><i class="af-status__mark"></i>Running</span><span><b>$0.42</b> so far</span></div>
</article>

<article class="af-card af-card--lit">…</article>   <!-- needs a person -->
```

| Part | Class | Notes |
|---|---|---|
| Card | `af-card` | Column, 12 px between parts. `af-card--airy` for 24 px padding. |
| Top | `af-card__top` | Space-between row that wraps: in a narrow place the status or meta drops under the label, whole. `af-card__meta` is mono 11 px `fg-subtle`. `af-card__lead` holds an icon + `af-card__name` (mono ID or environment name). |
| Body | `af-card__body` | `af-card__title` (16/600 Red Hat Text), `af-card__desc` (13 px `fg-muted`), `af-card__value` + `af-card__unit` for numbers. |
| Foot | `af-card__foot` | Pinned to the bottom on a `line-subtle` divider; `<b>` inside reads `fg`. |
| Lit | `af-card--lit` | Orange ring at 45% and a 6% orange tint. |
| Panel | `af-panel` | Same tone with no padding, for tables, lists and window grids. |

## When to use
- Grid cards: `af-grid af-grid--2|3|4` gives the 12 px gap and collapses on narrow screens.
- `af-card--lit` only while something waits on a person (an approval, a held push). Remove it the moment it's decided.

## Do
- Keep the foot to one line. Give every card in a row the same foot so the dividers line up.
- Use a link (`af-link`) or a small button in the foot, never both.

## Don't
- Don't add borders, drop shadows, gradients or a colored left edge.
- Don't light a card for failures; the failed status mark carries that. Lit means "a person is needed".
- Don't nest cards. Use `af-panel` sections or a list inside one card instead.
