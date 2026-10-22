# Data

Airframe consoles are mostly data. Make the data the brightest thing on the screen and everything around it quieter.

## Where each rule lives

Each page answers one question.

- <span id="tables"></span>**[How to lay out a table](Tables.md)**: headers, rows, alignment, the attention row and in-cell bars.
- <span id="inline-data-keyed"></span><span id="objects-by-reference"></span>**[How to show data inline](Inline.md)**: keyed metadata instead of dot-separated strings, and objects from other systems as chips.
- <span id="readouts"></span><span id="charts"></span>**[How to show the numbers a view is about](Charts.md)**: readouts, greyscale charts, sparklines and gauges.
- <span id="traces"></span><span id="lanes"></span>**[How to draw work over time](Traces.md)**: trace spans for one turn and session lanes for the last hour.
- <span id="fleet-board"></span>**[How to show a whole fleet](Fleet.md)**: stands grouped by pool, the runway views and progress as a claim.
- <span id="diffs"></span>**[How to show a change](Diffs.md)**: a greyscale diff with the sign column carrying the meaning.

## Density

- Size rows at `row-h` (32px); dense tables at `row-h-compact` (28px). Session lanes are `lane-h` (30px), trace spans `span-h` (28px).
- Set UI text in `body` (14px) and table cells in `body-s` (13px). Set IDs in `mono`, numbers in `data`, inline values in `mono-s`, keys and headers in `label-s`.
- Pad cards `space-16`; gap card grids `space-12`. Don't add air to a dense view; add hierarchy.

## Tabular figures

Every number that can sit above another uses tabular figures: `font-variant-numeric: tabular-nums`. The `data` style, `af-num`, `af-mono`, `af-meta__val` and `af-readout` already set it. Right-align numeric columns and keep decimals consistent within a column.

Part of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
