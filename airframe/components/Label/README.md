Labels are small sentence-case Red Hat Text (12 px, 500) in `fg-muted` that name a card, panel or section, with an optional sub (a count or scope) after a dim middle dot; a sub that is an ID or a region takes `af-mono`.

## You provide
- One or two words in sentence case. No capitals and no tracking: the mono capitals were retired in theme-v12, since they made every screen read as a printout.
- Optionally a sub: a count, region, ID or time window. Add `af-mono` (or `af-id`) when it is an ID, a region or a version, so codes stay mono.
- Optionally a leading icon; inside a label it is 14 px in `fg-muted`.
- Where the label is narrower than its place, the word stays whole and the sub ellipsizes as a last resort (a later sub before the first, so an ID outlasts `turn 7`); the full text stays in the DOM. In a card head the row wraps first (see Card).

## Markup
```html
<span class="af-lbl">Fleet<span class="af-lbl__sub af-mono">us-east4</span></span>
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
