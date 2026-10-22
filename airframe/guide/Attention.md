# How a thing shows it needs a person

A lit card, row or tile keeps a neutral ground and shows a 3px status edge, the mark and the word.

## Attention is edge, mark, word (theme-v12)

Until theme-v11 a lit card was its status mixed into the surface (6–9% orange in `raised`, a brown in Night) with a 1px orange ring, and a selected tile added a yellow ring outside that: two warm hues 21° apart on one tile. theme-v12 drops every status wash and outline:

| Thing | Ground | Status | Selected / open |
|---|---|---|---|
| Card (`af-card--lit`, `--failed`, `--denied`) | `raised` | 3px edge on the leading side, inset from the corners; mark; word | n/a |
| Agent row and card (`af-agent--lit`, `--failed`, `--denied`) | `raised`; `lifted` + `shadow-2` when open | the same edge; the mark; the word in the now-line; the rail head | open: `lifted`, focus ring in `fg` |
| Fleet tile, bay, mini card (`af-stand`, `af-bay`, `af-mini`) | neutral tone | the same edge; the mark; the current pip | 1px `fg` ring, 2px off the tile |
| Table and list row (`is-attention`) | unchanged | 3px edge on the first cell | `selected` + 2px `fg` edge (an attention row keeps its orange edge) |
| Decision (`af-decision`) | `lifted`, `radius-sheet`, `shadow-2` | the edge, the mark, the word in its hue | n/a |

`brand-wash` is deprecated: no Airframe rule uses it. Selection is neutral everywhere, so the yellow never sits around orange.

Measured (WCAG 2.x, Night / Day; the test suite holds the floor):

| Pair | Night | Day | Floor |
|---|---|---|---|
| `status-approval` word on `raised` / on `lifted` | 7.86 / 7.27 | 5.34 / 5.34 | 4.5 text |
| `status-failed` word on `raised` / on `lifted` | 5.63 / 5.21 | 5.63 / 5.63 | 4.5 text |
| `status-denied` edge on `raised` / on `lifted` | 3.88 / 3.59 | 5.63 / 5.63 | 3 UI part |
| `fg-muted` on `lifted` | 7.00 | 9.30 | 4.5 |
| `fg-subtle` on `lifted` | 4.94 | 5.75 | 4.5 |
| `fg` selection ring on `canvas` / `fg` on `selected` | 21.0 / 16.48 | 17.98 / 15.83 | 3 UI part |
| `rail-done` (fill, head, dotted estimate) on `rail` | 9.88 | 11.16 | 3 UI part |
| `on-lamp` number on the Needs-you badge | 8.95 | 8.95 | 4.5 text |

Part of [Status](Status.md), a chapter of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
