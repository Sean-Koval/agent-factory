Status is always color + shape + word, and follows the dark-cockpit rule: running and queued stay grey; only needs approval, failed and denied carry color.

## You provide
- One of six states and a short word. The mark is an empty `<i class="af-status__mark"></i>`; the class draws its shape.

## Markup
```html
<span class="af-status af-status--running"><i class="af-status__mark"></i>Running</span>
<span class="af-status af-status--queued"><i class="af-status__mark"></i>Queued</span>
<span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span>
<span class="af-status af-status--failed"><i class="af-status__mark"></i>Failed</span>
<span class="af-status af-status--denied"><i class="af-status__mark"></i>Denied</span>
<span class="af-status af-status--off"><i class="af-status__mark"></i>Spun down</span>

<!-- lit: the word takes the color too; for counts and panel headers -->
<span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>1 waiting on you</span>
```

| State | Token | Shape |
|---|---|---|
| running | `status-running` (quiet grey) | filled circle |
| queued | `status-queued` | hollow ring |
| approval | `status-approval` (orange) | diamond |
| failed | `status-failed` (red) | triangle |
| denied | `status-denied` fill, `on-status-denied` text | placard |
| off | `status-off` | small dot |

## The dark-cockpit rule
A screen that is working normally is dark. In a list of forty sandboxes, the only marks with color are the ones that need a person. Failed and approval marks keep their color; only the row waiting on a person also gets a tint (`af-list__row is-attention`, `af-table tr.is-attention`). Leave every other row alone.

## When to use
- Table and list cells, card tops, crumb rows, panel headers.
- `af-status--lit` for counts ("39 running", "1 failed") and for the status in the top of a lit card.

## Do
- Keep the word plain and short: Running, Queued, Needs approval, Failed, Denied, Spun down. Context words are fine ("Holding at PR", "Build failed").
- Give status columns a fixed width so marks line up down a list.

## Don't
- Don't put status in pill backgrounds. Plain text only; denied is the one placard.
- Don't use yellow for any status. Yellow is the brand; caution is orange.
- Don't light `af-status--off`: `status-off` is a mark color (3.4–3.7:1) and fails as text.
- Don't color running green. Normal is quiet.
