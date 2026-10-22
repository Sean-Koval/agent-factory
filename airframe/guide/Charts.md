# How to show the numbers a view is about

A readout for the one to four headline numbers; a greyscale chart for everything over time or across things.

## Readouts

- Use a readout for the one to four numbers a view is about: sandboxes this week, held for a human, spend today, turn to PR.
- Build it as digits on unlit cells inside a recessed window: `af-window` (`display-window`) holding `af-readout` with `--l`, `--m` or `--s`. Each digit or letter is a `<b>` on a `readout-cell`; punctuation is `<b class="af-readout__p">`.
- Put the unit and caption outside the cells: the unit in `body` `fg-subtle` beside it ("of 40 sandboxes"), the caption in `label` below it.
- Never use readout cells in tables, inline data or running text.

## Charts

- Draw charts in greyscale: `chart-1` (primary, `fg`-strength), `chart-2`, `chart-3`, `chart-4`, with `chart-6` for grid emphasis.
- Spend at most one attention series per chart, in `chart-5`. It shares the caution orange on purpose: it means "look here".
- Yellow appears in a chart only as the now line or now point, or a target or limit marker.
- Never use product hues or status colors as series. Errors are `status-failed` markers or outlines, never fills.
- Use single-hue greyscale for sequential scales and heatmaps; never red-to-green.
- Draw axes in `rule`, gridlines in `line-subtle`, tick labels in 10px mono `fg-subtle`. Label series directly where possible instead of a legend.
- Draw sparklines as a thin `fg-muted` line over a `line` baseline, ending in a `brand` dot on the latest value (the now point). In a list of agents (`af-spark--mini`) the end dot is `fg`: sixty yellow points would say sixty things are yours. Gauges are a `line` track with an `fg-muted` fill and a `brand-text` bug at the limit.
- One gauge on its own marks its limit with a `brand-text` bug. In a list or in a console opened from a row (`af-gauge--mini`), the bug is `fg-muted`, for the same reason as the list sparkline: one yellow tick per row would say every row is yours.

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
