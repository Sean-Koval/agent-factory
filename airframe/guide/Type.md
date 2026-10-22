# Type

Which face, size and weight to set: three families and one scale.

Three families: `--font-display` Archivo Expanded for headlines (700, sentence case, −0.01em); `--font-sans` Red Hat Text for body, UI, labels, buttons and keys; `--font-mono` DM Mono for IDs, numbers, commands and data values.

| Style | Family | Size / line | Weight | Tracking | Use |
|---|---|---|---|---|---|
| `display-xl` | display | 64 / 1 | 700 | −0.01em | Hero headline |
| `display-l` | display | 48 / 1.02 | 700 | −0.01em | Page headline |
| `display-m` | display | 36 / 1.05 | 700 | −0.005em | Section headline |
| `title-l` | display | 22 / 1.15 | 600 | 0 | Card and panel titles in the brand face |
| `title-m` | sans | 20 / 1.3 | 600 | −0.01em | Dialog and drawer titles |
| `title-s` | sans | 16 / 1.35 | 600 | −0.005em | Card titles in the body face |
| `body-l` | sans | 16 / 1.55 | 400 | 0 | Lead paragraphs |
| `body` | sans | 14 / 1.5 | 400 | 0 | Default UI text |
| `body-s` | sans | 13 / 1.45 | 400 | 0 | Dense UI, table cells, captions |
| `label` | sans | 12 / 1.2 | 500 | 0 | Labels, buttons, section names, sentence case |
| `label-s` | sans | 11 / 1.2 | 500 | 0 | Inline data keys, table headers, stage words, sentence case |
| `mono` | mono | 13 / 1.5 | 400 | 0 | IDs, commands, digests |
| `mono-s` | mono | 12 / 1.45 | 400 | 0 | Inline data values, durations |
| `data` | mono | 13 / 1.3 | 500 | 0 | Numbers in tables and readouts, tabular |

- Use the display face for headlines (`title-l` and up) and for product names beside their marks. Never set body, data or labels in it.
- Set labels, buttons, keys and table headers in `label` or `label-s`, in sentence case. The middle of the type scale (12–14 px sans) is where a console's words live; the display face and the small mono are its ends.
- Set every number with tabular figures (`font-variant-numeric: tabular-nums`; built into `af-num`, `af-mono`, `af-meta__val` and `af-readout`).
- Never set body copy in mono, and never set an ID, a number or a command in sans. Emphasize with `fg` against `fg-muted`, not italics; a status as the subject of a headline may take its color (`<em>` in a page title: "Two need you").
- Each style compiles to a class of the same name in tokens.css (`.display-l`, `.body-s`, `.label`).

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
