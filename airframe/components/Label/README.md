Labels are small tracked DM Mono capitals in `fg-muted` that name a card, panel or section, with an optional sub (a count or scope) after a dim middle dot.

## You provide
- One or two words in sentence or lower case; the CSS sets capitals and 0.08em tracking.
- Optionally a sub: a count, region, ID or time window.
- Optionally a leading icon; inside a label it is 14 px in `fg-muted`.

## Markup
```html
<span class="af-lbl">Fleet<span class="af-lbl__sub">us-east4</span></span>
<span class="af-lbl"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg>Waiting on you</span>

<div class="af-card__top">
  <span class="af-lbl"><svg class="af-ic" …>…</svg>Spend today</span>
  <span class="af-card__meta">limit $200</span>
</div>
```

## When to use
- The left side of every card top and panel head.
- Section captions above a group of cards or a table.
- Readout keys use the same voice through `af-window__key`; table headers through `th`.

## Do
- Name the thing, not the action: "Sessions", "Spend today", "Approval".
- Put scope in the sub, not in the label: `Sessions · last 60 min`.

## Don't
- Don't use a label as body text, a button or a link.
- Don't write a sentence in a label, or a label longer than about 24 characters.
- Don't color a label. Status and product hues never appear here.
