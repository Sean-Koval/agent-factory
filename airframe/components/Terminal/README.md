The terminal is always dark in both themes: DM Mono on `terminal-bg`, a bar with the sandbox tail number and scope, quiet ✓ lines, red ✗ lines, and the prompt and cursor in brand yellow.

## You provide
- The sandbox ID and two or three scope words for the bar (environment, region), and whether the session is live.
- Output lines, wrapped in spans for their role.

## Markup
```html
<section class="af-term" aria-label="Terminal, HGR-7Q2K">
  <div class="af-term__bar"><svg class="af-ic" …>terminal</svg><span class="af-term__id">HGR-7Q2K</span><span>base-codex</span><span>us-east4</span><span class="af-term__live">live</span></div>
<pre><span class="af-term__p">$</span> hangar job submit <span class="af-term__kw">--repo</span> <span class="af-term__str">acme/api</span>
<span class="af-term__ok">✓ edit    <span class="af-term__num">+42 −17</span></span>
<span class="af-term__err">✗ test    38 of 41</span>  <span class="af-term__cm"># retrying with the fix</span>
<span class="af-term__p">$</span> <span class="af-term__cursor"></span></pre>
</section>
```

| Class | Token | Use |
|---|---|---|
| `af-term__p`, `af-term__cursor` | `brand` | Prompt and cursor only |
| `af-term__ok` | `terminal-ok` | Whole ✓ line, quiet |
| `af-term__err` | `terminal-err` | The ✗ glyph and the failing step |
| `af-term__dim` | `terminal-dim` | Timings, IDs, secondary output |
| `af-term__kw` `__fn` `__str` `__num` `__cm` | `code-*` | Flags, commands, strings, numbers, comments |

## When to use
- Live sandbox sessions, job logs, and command examples in docs.

## Do
- Keep success quiet and let the one failing line be the only red.
- Use `brand` (not `brand-text`) for the prompt: the ground is dark in both themes.

## Don't
- Don't switch the terminal to a light ground in Day.
- Don't use green for success or color whole blocks of output.
- Don't put more than one cursor on screen.
