<span class="af-eyebrow">Airframe</span>

# Icons

Airframe has 57 icons, drawn on a 20 px grid: stroke only, 1.5 stroke, square caps, miter joins, `currentColor`. Use this set only: no icon fonts, no third-party sets, no emoji.

## Place an icon

Reference the sprite, `airframe-icons.svg`, which is vendored next to the CSS. Each icon's id is `af-` plus its name.

```html
<svg class="af-ic" aria-hidden="true"><use href="airframe/airframe-icons.svg#af-agent"/></svg>
```

Or paste one file from [`airframe/icons/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe/icons) inline.

| Class | Size | Use it |
| --- | --- | --- |
| `af-ic` | 16 px | The default, beside a label. |
| `af-ic--14` | 14 px | In small buttons. |
| `af-ic--20` | 20 px | In navigation and headers. |
| `af-ic--24` | 24 px | In empty states. |

## Rules

- **Pair an icon with a word** wherever there is room. An icon-only button needs an `aria-label`.
- **Color with text tokens.** `fg-subtle` beside a label, `fg` when active, `brand-text` when selected.
- **Status color is for status marks.** An icon takes a status color only when it is that status's mark.
- **No aircraft.** `agent` is a hex unit: aviation lives in the words and the logic, never in pictures of planes.

The [Iconography](guide/iconography.md) page of the brand book has the full rule.

## The set

Each tile shows an icon and its name. `agent-alt-1` to `agent-alt-3` are candidates kept for comparison.

--8<-- "airframe-icons.md"
