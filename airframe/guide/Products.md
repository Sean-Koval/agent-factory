# Products

Five products share one system. They differ only in name, glyph and hue, and the hue stays out of the UI.

## Family rules

- Every product uses the same tokens, components, statuses and voice. Never fork a component for one product; add a variant to Airframe.
- Identify a product by its mark and its name, set in the display face. Names keep their case: hangar, flightdeck, Tower (the governed workspace), ai-dlc, Spaceport.
- Use a product hue in three places only: the product mark, the docs or marketing header for that product, and the 2px nav marker under the active tab.
- Never use a product hue for state, buttons, links, focus, selection or chart series. Inside a console, everything but the mark and the nav marker is greyscale, brand yellow or status.
- Tail-number prefixes belong to a product: `HGR-` hangar, `FDK-` flightdeck, `TWR-` Tower.

## Product hues

The five hues share one OKLCH lightness per theme (0.74 Night, 0.52 Day) at matched chroma, so no product shouts over another. All meet 3:1 as marks on `raised` and `canvas`.

| Product | Token | Night | Day | Hue family |
|---|---|---|---|---|
| hangar | `product-hangar` | `#EE8F63` | `#A44C1D` | clay |
| flightdeck | `product-flightdeck` | `#D98CD2` | `#914A8C` | orchid |
| Tower | `product-tower` | `#C5A93B` | `#816600` | brass |
| ai-dlc | `product-aidlc` | `#69C27E` | `#1D7D3E` | green |
| Spaceport | `product-spaceport` | `#B199F4` | `#6F57AB` | violet |

There is no blue in the family. hangar's clay sits near the caution orange and Tower's brass near the brand yellow; that is why product hues stay in marks, headers and the nav marker, where nothing can mistake them for a status or an action.

## Marks

```html
<span class="af-mark af-hue--hangar" aria-hidden="true"><svg viewBox="0 0 24 24">…glyph…</svg></span>
```

- A mark is an outline tile: transparent fill, 1px `line-strong` border, `radius-control`, with the product glyph stroked in the product hue. `af-hue--<product>` sets the hue (`--pc`); the glyph draws in `currentColor`.
- Sizes: 30px by default, `af-mark--sm` (24px) in dense rows, `af-mark--lg` (44px) in docs headers and heroes.
- Glyphs are drawn on a 24px grid with the icon rules: line only, 1.6 stroke, square caps, miter joins; small solid details only where a shape needs them (ai-dlc's waypoints, Spaceport's satellite).
- The Airframe mark uses `af-hue--airframe`, which is `brand-text`: the family mark is the one mark in the brand color.
- Set the product name beside the mark in the display face. Never fill the tile with the hue, add a gradient or shadow, recolor the glyph, or show the mark without its name the first time a product appears on a page.

## Nav marker

- In a console nav, the active tab (`af-nav__tab` with `aria-current="page"`) gets a 2px bar along its bottom edge in the current product's hue. Put `af-hue--<product>` on the nav or the tab to set it.
- Everything else in the nav stays greyscale: tabs in `label` (sentence-case sans), `fg-muted` at rest, `fg` when active; counts in mono `fg-subtle`. The one exception is the Needs-you count, an orange badge (`af-nav__badge`) while it is above zero.
- The marker says where you are; it never means state. Attention in the nav uses the status marks.

## Glyph meanings

| Product | Glyph | Why |
|---|---|---|
| Airframe | An A-frame: two struts meeting at the top, one crossbar. | The structure every product is built on. |
| hangar | A quonset arch over a baseline, with a door. | Where the fleet of sandboxes is kept and serviced. |
| flightdeck | An attitude indicator: a circle, a tilted horizon, small wings. | Reading how a harness actually flies. |
| Tower | A control tower: a cab on a stem. | The one point that clears or holds every request. |
| ai-dlc | A closed loop with three waypoint triangles. | A flight plan flown the same way every time: the dev loop. |
| Spaceport | An orbit ellipse, a launch tower and a satellite dot. | Where data products are launched and tracked. |

## Brand surfaces

A product's README banner, social preview, favicon and docs header mark are generated, never drawn: `scripts/banners.py` builds them from the tokens, `icons/marks.json` and the fonts in `fonts/` into `brand/<product>/`, and each tool repo vendors its own with `scripts/sync-brand.sh`.

- One composition for the family: eyebrow (`Agent factory · Run`; the role word alone, never "plane", which collides with flightdeck's data plane), the mark beside the name in the display face, the product's line, and the suite strip with the 2px marker under this product's role. The strip tells the suite story: four planes (Define = the team harness, Run = hangar, Judge = flightdeck, Govern = Tower), then ai-dlc as Setup and Spaceport as the capability. The hue appears in the mark and the marker only; the brand yellow is the eyebrow hairline.
- Night and Day both ship; a README shows them with `<picture>` and `prefers-color-scheme`. The social preview is Night.
- Text is outlined, because images served by GitHub load no web fonts. Change copy in the script, not in a file.
- The repository description, the docs `site_description` and the banner's line say the same thing.
