<span class="af-eyebrow">Airframe</span>

# Tokens

Every value Airframe uses, generated from [`airframe/tokens.json`](https://github.com/Sean-Koval/agent-factory/blob/main/airframe/tokens.json). Use a token for what its note says, not for the color it happens to be today.

## Use a token

In CSS each token is a custom property, `var(--af-<name>)`, from `airframe.css`. Never write a color, size or font as a literal.

```css
.my-panel {
  background: var(--af-raised);
  color: var(--af-fg);
  padding: var(--af-space-16);
  border-radius: var(--af-radius-card);
}
```

| You need | Look under |
| --- | --- |
| A background, a divider or a text tone | [Ground](#ground), [Lines](#lines), [Text](#text) |
| The primary action or the focus ring | [Brand](#brand) |
| A state that may need a person | [Status](#status) |
| A chart, a trace or a progress rail | [Traces, lanes, rails and readouts](#traces-lanes-rails-and-readouts), [Charts](#charts) |
| A product's mark or nav marker | [Product hues](#product-hues) |
| A font, a size or a weight | [Type](#type) |
| A gap, a radius or a row height | [Space, shape and layout](#space-shape-and-layout) |

Other toolchains read the same values: a Tailwind v4 `@theme` and the W3C Design Tokens files install from the [Registry](registry.md).

## Color

Each row shows the token, its Night and Day values and what it is for. The swatches are live: switch the site's theme and they follow.

Text tokens meet 4.5:1 on `canvas`, `surface` and `raised` in both themes. `line-strong`, `focus` and the status colors meet 3:1. The tests in `tests/test_airframe.py` hold every release to that.

--8<-- "airframe-colors.md"

## Type

Three families and one scale. The display face is for headlines, the sans for reading and labels, the mono for IDs, numbers and commands. The [Type](guide/type.md) page of the brand book has the rules.

--8<-- "airframe-type.md"

## Space, shape and layout

Space sits on a 4px base. Controls, cards and sheets each have one radius. The [Layout](guide/layout.md) page says which to use where.

--8<-- "airframe-shape.md"
