The terminal is always dark in both themes: DM Mono output on `terminal-bg`, quiet ✓ lines, red ✗ lines, and the prompt and cursor in brand yellow. Its bar is a sentence-case label in sans: the product name in `terminal-fg`, then what runs and the tail number in `terminal-dim`.

## You provide
- For the bar: the product name (hangar, flightdeck and ai-dlc stay lowercase), a short title in sentence case (what runs, or the environment), the sandbox ID as a tail number, and whether the session is live.
- Output lines, wrapped in spans for their role.

## Markup
```html
<section class="af-term" aria-label="Terminal, hangar, HGR-7Q2K">
  <div class="af-term__bar"><svg class="af-ic" …>terminal</svg><b class="af-term__product">hangar</b><span aria-hidden="true">·</span><span>Fix the flaky auth refresh test</span><span aria-hidden="true">·</span><span class="af-term__id" title="sbx_01j9q2k7tx4m8c">HGR-7Q2K</span><span class="af-term__live">Live</span></div>
<pre><span class="af-term__p">$</span> hangar job submit <span class="af-term__kw">--repo</span> <span class="af-term__str">acme/api</span>
<span class="af-term__ok">✓ edit    <span class="af-term__num">+42 −17</span></span>
<span class="af-term__err">✗ test    38 of 41</span>  <span class="af-term__cm"># retrying with the fix</span>
<span class="af-term__p">$</span> <span class="af-term__cursor"></span></pre>
</section>
```

| Class | Token | Use |
|---|---|---|
| `af-term__bar` | `terminal-dim`, `font-sans` | The bar: a 12.5px sans label, sentence case |
| `af-term__product` | `terminal-fg` | The product name, the one bright word in the bar |
| `af-term__id` | `terminal-dim`, `font-mono` | The tail number; the real ID in `title`. Never truncated |
| `af-term__p`, `af-term__cursor` | `brand` | Prompt and cursor only |
| `af-term__ok` | `terminal-ok` | Whole ✓ line, quiet |
| `af-term__err` | `terminal-err` | The ✗ glyph and the failing step |
| `af-term__dim` | `terminal-dim` | Timings, IDs, secondary output |
| `af-term__kw` `__fn` `__str` `__num` `__cm` | `code-*` | Flags, commands, strings, numbers, comments |

## When to use
- Live sandbox sessions, job logs, and command examples in docs.

## Do
- Separate the bar's parts with a `·` span marked `aria-hidden`. A long title is cut with an ellipsis; the product name, the ID and Live never are.
- Keep success quiet and let the one failing line be the only red.
- Use `brand` (not `brand-text`) for the prompt: the ground is dark in both themes.

## Don't
- Don't set the bar in capitals or tracked mono: it is a label, and labels are sentence-case sans.
- Don't switch the terminal to a light ground in Day.
- Don't use green for success or color whole blocks of output.
- Don't put more than one cursor on screen.
