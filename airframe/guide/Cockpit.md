# When a status takes color

Color appears only when a person is needed. This page is the dark-cockpit rule and the three places it knowingly bends.

## The dark-cockpit rule

- Keep normal quiet. Running is grey (`status-running`), queued is a grey ring. Neither ever takes a hue; there is no green.
- Spend color only on needs approval (orange), failed (red) and denied (red placard). A view with no color on it is a view where nobody is needed.
- Set the status word in `fg` by default. Add `af-status--lit` to color the word too, only where the status is the subject: an alert, an inspector header, a master caution line.
- Never put a pill or background behind a status word. The fills are the denied placard, the two lamps, and one more: the orange count badge on a console's Needs-you nav item (`af-nav__badge`), which is a count of people needed, not a status word; at zero it is a grey count.
- Never mix a status color into a surface. A lit card, row or tile is a neutral ground with a 3px status edge on its leading side, the mark and the word: **edge, mark, word**. Selection is neutral (`selected` with a `fg` edge or ring), so the brand yellow never sits around the orange.
- Never animate a status. No pulse, no blink, no spinner on running. The heartbeat dot that breathes beside a live agent's now-line is recency (seconds since it last did something), not a status, and it is still under reduced motion. The glow on a rail head says "moving" for the same reason.
- Never use `brand` or a product hue for a status, and never a status color for anything that is not a status. The one exception is `chart-5`, the attention series, which borrows the caution orange to mean "look here".
- Keep failed and denied apart by shape, not hue: failed is a triangle with a word, denied is a placard.
- Survive forced colors (Windows Contrast Themes). The browser replaces colors there, so marks paint in `CanvasText`, the status edge becomes a 3px `CanvasText` border, tonal tiles become outlines and selection uses `Highlight`; the shape and the word carry the status. Never set `forced-color-adjust: none` on a status.
- Light the master lamps from the same rule. MasterCaution shows `lamp-caution` when anything in its scope needs approval and `lamp-warning` when anything failed or was denied; when both apply, warning sits first. With nothing to say it stays dark (`af-master--clear`).

## Accepted bends

theme-v12 knowingly bends three rules above, each for one job and nowhere else:

1. **The Needs-you count badge** (`af-nav__badge`). An orange fill (`lamp-caution`, `on-lamp` number, 8.95:1) behind the count on the console's Needs-you nav item, the one place an inbox count earns a fill. It is a count of people needed, not a status word; at zero it is the grey `af-nav__count`, never an empty badge. In Day the badge against the canvas is 2.13:1, so the number (8.95:1 on the fill) and the word "Needs you" beside it carry it, never the fill alone.
2. **The heartbeat pulse** (`af-hb--live`). The dot beside a live agent's now-line breathes (opacity 1 → .35 over 2.4 s). It says recency, not state: it never runs on a waiting, failed, denied, queued or spun-down agent, and under `prefers-reduced-motion` it is still. A status still never animates.
3. **The rail-head glow** (`rail-glow`, `0 0 12px`). Around a live rail head and the latest dot of an activity timeline, and nowhere else. It says "moving". An estimate (`af-rail--est`) never glows, and forced colors drop it.

Part of [Status](Status.md), a chapter of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
