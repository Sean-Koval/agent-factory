Inline data is keyed metadata on one line: a small mono capital key in `fg-subtle`, then a mono value in `fg-muted`, items 18 px apart and wrapping whole.

## You provide
- Pairs of key and value. Keys are one sentence-case word or two (`Policy`, `Harness`, `Last approval`) in small sans; values stay mono.
- Optionally a modifier per item: `--strong` for the subject (value in `fg`), `--approval` or `--failed` when the value is what needs a person.

## Markup
```html
<span class="af-meta">
  <span class="af-meta__item af-meta__item--strong"><span class="af-meta__key">sandbox</span><span class="af-meta__val">HGR-3MX9</span></span>
  <span class="af-meta__item"><span class="af-meta__key">harness</span><span class="af-meta__val">codex</span></span>
  <span class="af-meta__item"><span class="af-meta__key">model</span><span class="af-meta__val">gpt-5.1</span></span>
  <span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">policy</span><span class="af-meta__val">require-approval-main-push</span></span>
</span>
```

## When to use
- Under a title (card body, master caution, approval subject).
- In a card foot or table foot, opposite a link or button.
- In panel heads as a summary of counts (`running 31  waiting 1  failed 1`).

## Do
- Lead with the subject (`--strong`), then the facts in the order a person reads them: who, how, what changed, how long.
- Use one `--approval` or `--failed` item at most, and only for the value that explains the color elsewhere.
- Let it wrap. Items never break inside.

## Don't
- Never write metadata as "codex · gpt-5.1 · 41 min". Key every value.
- Don't use it for paragraphs or for more than about six items; move longer sets to an `af-kv` list.
- Don't change the key color or size per item.
