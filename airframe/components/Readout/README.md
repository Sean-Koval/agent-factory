A readout is a big DM Mono number with each digit on an unlit cell (`readout-cell`), set inside a recessed display window (`display-window`) with a small capital key below.

## You provide
- The value, one `<b>` per digit or letter. Punctuation (`,` `.` `:` `$` `%`) goes in `<b class="af-readout__p">` so it sits on no cell.
- A key for the window: what the number counts, in a few words.
- Optionally a unit (`af-readout__unit`, small, after a gap) or a minor part such as cents (`af-readout__minor`, smaller, no gap).

## Markup
```html
<div class="af-readouts">                         <!-- 3 windows; set style="--af-cols:2" for two -->
  <div class="af-window">
    <span class="af-readout af-readout--m"><b>2</b><b class="af-readout__p">,</b><b>4</b><b>8</b><b>1</b></span>
    <span class="af-window__key">Sandboxes this week</span>
  </div>
  <div class="af-window">
    <span class="af-readout af-readout--m"><b>1</b><b class="af-readout__p">.</b><b>8</b><span class="af-readout__unit">s</span></span>
    <span class="af-window__key">To resume from a snapshot</span>
  </div>
</div>

<!-- a single window on its own -->
<div class="af-window af-window--cell">…</div>
```

| Size | Class | Where |
|---|---|---|
| L | `af-readout--l` (34–60 px, fluid) | Hero numbers and report covers, one per window |
| M | `af-readout--m` (30 px) | Summary cards, hero panel windows |
| S | `af-readout--s` (20 px) | Compact windows beside a key, inspector panels |

## When to use
- Two to four numbers that define a screen: sandboxes this week, held for a human, spend today.
- Inside summary cards, readouts sit on the card without a window.

## Do
- Put windows in an `af-readouts` grid inside a card or panel; the 2 px gaps show the canvas between windows.
- Keep numbers short (five characters or fewer before units).

## Don't
- Don't use readouts in tables or running text; use `.af-mono` with tabular figures.
- Don't color the digits. A readout is never a status.
- Don't add glow, gradients or segment fonts; the cells are the whole effect.
