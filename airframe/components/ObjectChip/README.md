An object chip is a business object by reference (a ticket, a pull request, an account, a trade, a repo): a source glyph, the key in mono, the title and a state word on a 26 px `surface` tile with a hairline, never a pill and never a status fill; hovering or focusing it shows a trust line (source, freshness, provenance), and a restricted object shows its key only.

## You provide
- The source glyph from the icon set (`job` for a ticket, `pr`, `database` for an account, `branch` for a repo, `lock` when restricted), the key in mono (`PAY-412`, `acme/api#412`, `001Qx…88A`), an optional title, and a state as a word (`In progress`, `Open`, `Account`).
- `href` when the viewer may open it (`<a class="af-obj af-obj--link">`); a `span` otherwise.
- `af-obj--restricted` when the viewer may not see the object: the lock, the key and the word `restricted`; no title, no state, no link.
- The approval mark on the state (`af-obj__state af-status af-status--approval`) when a decision about this object waits: the one color a chip may carry.
- A trust line (`af-obj__trust`) as keyed data: `SOURCE` (the connector and site), `READ` (when the title and state were fetched), `BY` (which agent or person read or touched it last, with the receipt), shown on hover and focus. Give a non-link chip `tabindex="0"` so the keyboard reaches it.

## Markup
```html
<a class="af-obj af-obj--link" href="https://acme.atlassian.net/browse/PAY-412">
  <svg class="af-ic" …>job</svg>
  <span class="af-obj__key">PAY-412</span>
  <span class="af-obj__title">Refund double charge on order 88231</span>
  <span class="af-obj__state">In progress</span>
  <span class="af-obj__trust" role="tooltip"><span class="af-meta">
    <span class="af-meta__item"><span class="af-meta__key">source</span><span class="af-meta__val">Jira, acme.atlassian.net</span></span>
    <span class="af-meta__item"><span class="af-meta__key">read</span><span class="af-meta__val">2 min ago</span></span>
    <span class="af-meta__item"><span class="af-meta__key">by</span><span class="af-meta__val">Breaks, receipt TWR-RCPT-0101</span></span>
  </span></span>
</a>

<span class="af-obj af-obj--restricted" tabindex="0"><svg class="af-ic" …>lock</svg><span class="af-obj__key">TR-88231</span><span class="af-obj__state">restricted</span></span>

<a class="af-obj af-obj--link" href="…"><svg class="af-ic" …>pr</svg><span class="af-obj__key">acme/api#418</span><span class="af-obj__title">Rotate signing keys</span><span class="af-obj__state af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></a>

<div class="af-objs">…chips…</div>
```

With airframe.js: `obj({source: "job", key: "PAY-412", title: "…", state: "In progress", href, trust: {source, read, by}})`, `obj({key: "TR-88231", restricted: true})`, `obj({…, approval: true})`.

| Variant | Class | What shows |
|---|---|---|
| link | `af-obj--link` on an `<a>` | glyph, key, title, state; the title underlines on hover |
| plain | `af-obj` on a `span` | the same, not openable from here |
| restricted | `af-obj--restricted` | lock, key, `restricted`; transparent tile |
| approval | state with `af-status--approval` | the diamond before the state word |

## When to use
- On approval cards, receipts, run steps, Tower's desk and object pages, hangar's job rows: wherever an agent's work touches a thing outside the suite.
- Inline in a sentence ("ticketed the fourth as `PAY-412`") and in list rows.

## Do
- Show the real key and keep it in mono; truncate the title, never the key.
- Say where the title and state came from and when, on hover; they are a cache, not the record.
- Render a chip the viewer may not open as restricted, so they learn that the object exists and nothing more.
- Keep the state a word. Only an approval about the object puts a mark on it.

## Don't
- Don't make a chip a pill, tint it by source, or fill it with a status color; "In progress" is a word, not a running circle.
- Don't show a logo in the glyph slot; the icon set only.
- Don't link a restricted chip, and don't leak its title in the trust line.
