Product marks are outline tiles (1 px `line-strong`, `radius-control`) with a stroke glyph in the product hue; the hue appears nowhere else except docs headers and the 2 px marker under the active nav tab.

## You provide
- The product: `airframe`, `hangar`, `flightdeck`, `tower`, `aidlc` or `spaceport`, as an `af-hue--<product>` class (`af-hue--workspace` still works for Tower). It sets `--pc`, which the mark and the nav marker read.
- The glyph SVG (24 px viewBox) below. The tile sets stroke 1.6, square caps, miter joins, `currentColor`.

## Markup
```html
<span class="af-mark af-hue--hangar" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M3 20 V13 A9 9 0 0 1 21 13 V20"/><path d="M2 20 H22"/><path d="M9 20 V15 H15 V20"/></svg></span>

<!-- lockup: mark + name in the display face + an optional sub -->
<span class="af-lockup"><span class="af-mark af-hue--hangar">…</span>
  <span class="af-lockup__text"><span class="af-lockup__name">hangar</span><span class="af-lockup__sub">Sandbox control plane</span></span></span>
```

Sizes: `af-mark--sm` 24 px (menus, crumbs), default 30 px (headers, lockups), `af-mark--lg` 44 px (docs headers, covers).

The same glyphs live in `airframe/icons/marks.json`, which `scripts/banners.py` reads to generate each product's favicon, header mark, README banner and social preview (`brand/<product>/`). Change a glyph in both places; `tests/test_banners.py` checks they agree.

| Product | Class | Hue token | Glyph paths (viewBox 0 0 24 24) |
|---|---|---|---|
| Airframe | `af-hue--airframe` | `brand-text` | `<path d="M4 20 L12 4 L20 20"/><path d="M7.5 14 H16.5"/>` |
| hangar | `af-hue--hangar` | `product-hangar` | `<path d="M3 20 V13 A9 9 0 0 1 21 13 V20"/><path d="M2 20 H22"/><path d="M9 20 V15 H15 V20"/>` |
| flightdeck | `af-hue--flightdeck` | `product-flightdeck` | `<circle cx="12" cy="12" r="9"/><path d="M4.4 16.9 L21 12.8"/><path d="M6.5 11 H10 L12 13 L14 11 H17.5"/>` |
| Tower | `af-hue--tower` | `product-tower` | `<path d="M6 4 H18 L16.5 9 H7.5 Z"/><path d="M10 9 V20"/><path d="M14 9 V20"/><path d="M7 20 H17"/><path d="M12 4 V2"/>` |
| ai-dlc | `af-hue--aidlc` | `product-aidlc` | `<circle cx="12" cy="12" r="8"/><g fill="currentColor" stroke="none"><path d="M12 2.2 L14 5.6 H10 Z"/><path d="M18.93 14.2 L20.93 17.6 H16.93 Z"/><path d="M5.07 14.2 L7.07 17.6 H3.07 Z"/></g>` |
| Spaceport | `af-hue--spaceport` | `product-spaceport` | `<ellipse cx="12" cy="12" rx="10" ry="4.5" transform="rotate(-20 12 12)"/><path d="M12 5 L13.5 8 V17 H10.5 V8 Z"/><path d="M9.5 20 H14.5"/><circle cx="21.4" cy="8.6" r="1.4" fill="currentColor" stroke="none"/>` |

## The nav marker
Put the product's hue class on the header (`<header class="af-nav af-hue--hangar">`). The active tab (`aria-current="page"`) draws a 2 px bar in `--pc` on the header rule. That bar and the mark are the only places the hue shows in the app.

## Do
- Write product names as their owners do: hangar, flightdeck, ai-dlc in lower case; Airframe and Spaceport capitalized.
- Use the 30 px mark beside the name in the app header and the hero eyebrow.

## Don't
- Don't fill the tile with the hue, and don't tint backgrounds, buttons, charts or text with product hues.
- Don't redraw or rotate the glyphs, or set them in a circle.
- Don't use a product hue for status. Orange and red belong to approval and failure.
