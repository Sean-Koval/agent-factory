# Icons

Airframe's 55 icons (published to tool repos as `theme/airframe-icons.svg`) as standalone SVG files, one symbol sprite and a JSON map for code.

- **Ink**: every file strokes in `currentColor`. Inline, or through the sprite, an icon takes the text color around it (use text tokens: `fg-subtle` beside a label, `fg` when active, `brand-text` when selected). Through `<img>` it renders black; to recolor an `<img>`, inline the markup instead or use the file as a CSS `mask-image` over a token color.
- **Grid**: `viewBox="0 0 20 20"`, live area 2.5–17.5, `fill="none"`, `stroke-width="1.5"`, `stroke-linecap="square"`, `stroke-linejoin="miter"`. Show at 16 px in UI, 20 px in nav and headers, 14 px in dense rows, 24 px in empty states.

## Files

| File | What |
|---|---|
| `<name>.svg` | One icon, `currentColor`, 20 × 20. 55 files. |
| `airframe-icons.svg` | Sprite: a `<symbol id="af-<name>">` per icon in `currentColor`. It also lays the symbols out as a contact sheet, so the file previews as an image. |
| `icons.json` | `{ "<name>": "<inner SVG markup>" }` for code. |

## Using the sprite

```html
<!-- same-origin reference -->
<svg class="af-ic" aria-hidden="true"><use href="airframe/airframe-icons.svg#af-agent"/></svg>

<!-- or inline the file once, hidden, and reference by id -->
<div hidden><!-- contents of airframe-icons.svg --></div>
<svg class="af-ic af-ic--20" aria-hidden="true"><use href="#af-fleet"/></svg>
```

## From code

```js
import icons from "./icons.json";
const icon = (name, cls = "af-ic") =>
  `<svg class="${cls}" viewBox="0 0 20 20" aria-hidden="true">${icons[name]}</svg>`;
```

## Agent candidates

The aircraft glyph was retired. Four candidates were drawn; the strongest became `agent`, the rest are kept.

| File | Idea | Verdict |
|---|---|---|
| `agent.svg` | Unit, running: a hex unit drawn as an open loop around a solid core | Chosen. Reads as a worker mid-task at 16 px, avoids spinner, robot and sparkle tropes, and tiles into `fleet`. |
| `agent-alt-1.svg` | Orbit: a core inside a running orbit with a lead node | Clear motion, but reads as a loading spinner at small sizes. |
| `agent-alt-2.svg` | Actor: a pointer with a target | Strong for computer use; easy to take for a select tool. |
| `agent-alt-3.svg` | Beacon: a core broadcasting | Reads as live or wireless rather than as a worker. |
