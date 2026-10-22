# Layout

How a screen is spaced and shaped: spacing, radius, borders, tonal cards and the two textures.

## Spacing and layout

- Space on a 4px base: `space-2`, `-4`, `-8`, `-12`, `-16`, `-20`, `-24`, `-28`, `-32`, `-40`, `-48`, `-64`, `-104`, `-160`.
- Pad cards with `space-16` (airy: `space-24`). Gap card grids by `space-12` and blocks by `space-28`. Gutter pages by `space-32` on desktop and `space-16` on phones. Pad sections with `space-64` (compact `space-48`, marketing `space-104`, hero top `space-160`).
- Cap content at `container-max` (1280px). The app header is `header-h` (56px).
- Rows are `row-h` (32px; dense tables `row-h-compact`, 28px). Session lanes are `lane-h` (30px), trace spans `span-h` (28px).
- Put `space-8` between an icon and its label and `space-4` between fleet tiles.

## Radius

- `radius-control` (8px): buttons, inputs, chips, tags, segments, fleet tiles, product mark tiles. The segmented control's well is 11px (control + 3px inset).
- `radius-card` (12px): cards, panels, agent rows and board cards.
- `radius-sheet` (18px): what opens or sits on top: an agent's console, the top card of the decision deck, a dialog, a bottom drawer's top corners.
- `radius-none`: tables, lanes, trace bars. The denied placard is 4px.
- `radius-round`: status dots, heartbeat dots, avatars and the switch. Chips, tags and counts are not pills; the one pill is the nav's Needs-you badge.

## Borders and dividers

- Cards and panels have no border.
- Inside a card, divide rows and the footer (`af-card__foot`) with `line-subtle`. Rule under a table header with `line`.
- Border controls with 1px `line-strong`: inputs, secondary buttons, switches, product mark tiles.
- Rule sections that sit on the canvas with `rule`.
- Mark a card that needs a person with `af-card--lit`: the ground stays `raised` and a 3px `status-approval` edge sits on its leading side, inset from the corners, with the diamond and the word. `af-card--failed` and `--denied` light the same edge in red for a stopped card. Never tint a card, never ring it, and never put the edge on anything that does not need a person or has not stopped.
- Never box a table, list or chart inside a card, and never double a line.

## Cards are tonal

- Put content on `af-card` (padded, `raised`, `radius-card`) or `af-panel` (unpadded, for tables, lanes and traces).
- Separate cards by tone and `space-12`, not borders. Never nest `raised` in `raised`; for a well inside a card use `surface` or `display-window`.
- Resting cards cast no shadow. `lifted` surfaces carry `shadow-1` (resting lift) or `shadow-2` (open on top); `shadow-overlay` is for menus, popovers and toasts.

## Texture

- Use two textures and nothing else.
- **Dot field.** Small dots on an 8px pitch in `dot-field`, behind hero data only, once per page at most.
- **Hatching.** 135° stripes in `status-approval` for time spent waiting on a human, in lanes and trace spans.
- No gradients, noise, grain, blur, gloss or background images. The one glow is `rail-glow` around a live rail head and the latest timeline dot: it means "moving", never a status.

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
