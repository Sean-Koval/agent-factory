<span class="af-eyebrow">Airframe</span>

# Icons

A custom set drawn on a 20 px grid: stroke only, 1.5 stroke, square caps, miter joins, `currentColor`. No icon fonts, no third-party sets, no emoji. Pair an icon with a word wherever there is room; an icon-only button needs an `aria-label`.

Use the sprite (`theme/airframe-icons.svg`, vendored next to the CSS):

```html
<svg class="af-ic" aria-hidden="true"><use href="airframe/airframe-icons.svg#af-agent"/></svg>
```

or paste one file from [`airframe/icons/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/icons) inline. `agent` is a hex unit, not an aircraft: aviation lives in the words and the logic, never in pictures of planes. `agent-alt-1` to `agent-alt-3` are candidates kept for comparison.

--8<-- "airframe-icons.md"
