# Iconography

Which icons to use, at what size and in what color.

- Use the Airframe icon set only: custom, drawn on a 20 px grid, stroke-only, `--icon-stroke` 1.5, square caps, miter joins, `fill: none`, `stroke: currentColor`. No icon fonts, no third-party sets, no emoji.
- Markup: `<svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg>`. Default size is 16px (`icon-size`); use `af-ic--14` in small buttons, `af-ic--20` in nav and headers, `af-ic--24` for empty states.
- Color icons with text tokens: `fg-subtle` beside a label, `fg` when active, `brand-text` when selected. An icon takes a status color only when it is that status's mark.
- Pair icons with a word wherever space allows. An icon-only button needs an `aria-label`.
- The `agent` glyph replaced the Lab's aircraft silhouette: agents are not airplanes. Aviation lives in the words and the logic (dark cockpit, tail numbers, master caution), never in pictures of aircraft.
- Files: one SVG per icon in `icons/<name>.svg`, the sprite `icons/airframe-icons.svg` and the index `icons/icons.json`. See the [Icons](../components/Icons/README.md) component.

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
