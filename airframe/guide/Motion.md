# Motion and focus

How things move, and how focus shows.

## Motion

- Transition color, background, border and opacity over `--af-dur` (200 ms) with `--af-ease` (`cubic-bezier(.2,0,0,1)`); a press or a hover tint over `--af-dur-fast` (120 ms). Buttons press to `scale(.97)`.
- Something opening or closing in place (a row's console, a deck card leaving, a drawer, a toast rising) takes `--af-dur-open` (300 ms) with `--af-ease-open` (`cubic-bezier(.32,.72,0,1)`): it decelerates and never overshoots. A rail head and a capsule fill glide to a new value over 900 ms.
- No bounce, springs, overshoot or parallax. A status never animates to get attention; its color and shape do that. The one thing that breathes is the heartbeat dot of a live agent (Heartbeat), and it says recency, not state.
- `prefers-reduced-motion: reduce` switches all transitions and animations off and zeroes the duration tokens (base.css), so scripts that time an exit skip it. Never override it.

## Focus

- Show `:focus-visible` on every interactive element as a 2px solid `focus` outline, offset 2px; base.css sets it globally. `focus` is yellow in Night (13:1 on `canvas`) and dark gold in Day (5.5:1).
- Never remove the outline. Inset it (`outline-offset: -2px`) only where an offset ring would be clipped, as in dense rows.

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
