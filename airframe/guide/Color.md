# Color

Which color goes where: the roles every token plays, why the brand yellow is never a status, and the two themes.

## Color roles

- **Ground.** `canvas` for the page; `surface` for recessed wells (inputs, the terminal bar, display windows, the command in a decision); `raised` for cards and panels; `lifted` for the one step above them (an opened row, the top card of a deck, a sheet, a dialog), with `edge-hi` as its 1px top highlight and `shadow-1` or `shadow-2` under it; `overlay` for menus and popovers; `selected` for the selected row or tab.
- **Lines.** `line-subtle` between rows inside cards and tables; `line` for hairlines (table header rule, chips, keys); `line-strong` for control borders (3:1 or better on `surface` and `raised`); `rule` for section rules and chart axes where there is no card.
- **Text.** `fg` for primary text and values; `fg-muted` for secondary text and inline values; `fg-subtle` for labels, keys and timestamps (the lowest text tone, 4.9:1 or better); `fg-dim` for separators and disabled marks, never text.
- **Brand.** `brand` fill with `on-brand` text; `brand-hover`; `brand-text` for brand as text or a 1px line; `focus` for the ring. `brand-wash` is deprecated: selection is `selected` with a neutral `fg` edge or ring, never a yellow tint.
- **Status.** `status-running`, `status-queued`, `status-approval`, `status-failed`, `status-denied` with `on-status-denied`, `status-off`. Lamps `lamp-caution` and `lamp-warning` with `on-lamp` text are the only large color fields in the UI, and only in MasterCaution.
- **Terminal and code.** `terminal-*` and `code-*` stay dark in both themes. Code is greyscale; only `terminal-err` carries color.
- **Data.** `span-model`, `span-tool`, `span-sandbox`; `stage-plan`, `stage-edit`, `stage-test`; `rail`, `rail-done`, `rail-glow` for progress (rail, ring, capsule, track); `chart-1` to `chart-6`; `readout-cell`, `display-window`; `dot-field`.
- **Product.** `product-hangar`, `product-flightdeck`, `product-tower`, `product-aidlc`, `product-spaceport`: marks, docs headers and the 2px nav marker only.

## The brand is never a status

Use `brand` for the primary action, focus, the active route (trace critical path, now line) and selected marks, and nothing else. Never color a status, alert, badge or chart series yellow. Caution is orange for exactly this reason: cockpits paint caution amber, and an amber "needs approval" beside a yellow primary button would read as one signal. So `status-approval` is orange (`#FF8A3D` Night, `#B04E00` Day) and always a diamond, and a yellow fill always means "your action". Product hues never carry state either.

## Night and Day

- Set the theme on the root: `<html data-theme="dark">` for Night (the default) or `data-theme="light"` for Day. Tokens re-declare per theme; never branch on theme in component CSS.
- Night is true black (`canvas` `#000000`) with `raised` `#141414` cards. Day is paper grey (`canvas` `#F4F4F2`) with white `raised` cards.
- The `brand` fill is the same yellow in both. For brand as text or a line use `brand-text`, which drops to dark gold `#7A5F00` in Day, since yellow on paper is 1.5:1.
- Terminals, code blocks and lamp fills keep their values in both themes.
- Check every component in both themes: text 4.5:1 on its ground; 3:1 for text 24px and up, meaningful borders, icons and the focus ring.

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
