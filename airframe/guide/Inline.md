# How to show data inline

Metadata beside a title, and an object that lives in another system, both read as keyed data.

## Inline data: keyed

Write metadata as key and value pairs, never as `a · b · c` strings.

```html
<span class="af-meta">
  <span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">Policy</span><span class="af-meta__val">require-approval-main-push</span></span>
  <span class="af-meta__item"><span class="af-meta__key">Harness</span><span class="af-meta__val">codex</span></span>
  <span class="af-meta__item af-meta__item--strong"><span class="af-meta__key">Model</span><span class="af-meta__val">gpt-5.1</span></span>
</span>
```

- Keys are short nouns in small sentence-case sans, `fg-subtle`: Policy, Harness, Model, Env, Stage, CPU, Cost, Age, Region, Held.
- Values are mono in `fg-muted`. Use `af-meta__item--strong` (`fg`) for the one value that matters most.
- Only a policy or approval value may take a status color: `af-meta__item--approval` or `af-meta__item--failed`.
- Order items from most identifying to least. Keep to five per line; let the rest wrap.
- For an inspector or detail pane, use `af-kv` (a key/value grid) instead.
- The middle dot exists in one place only: the sub-label of `af-lbl` (`Fleet · us-east4`).

## Objects by reference

A business object from another system (a ticket, a pull request, an account) is a chip: source glyph, mono key, title, state
word, on a `surface` tile with a hairline. Its title and state are a cache with a timestamp, never the record, so the chip
shows source, freshness and provenance on hover. A chip the viewer may not open shows the key alone with the word
`restricted`. The approval diamond is the only color a chip may carry. See the ObjectChip component.

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
