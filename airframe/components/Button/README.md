Buttons are DM Mono capitals on a 2px radius: a solid signal-yellow primary, a hairline secondary, a quiet ghost and a red-outline danger, at 34 px or 28 px; the text variant sets them in sentence-case Red Hat Text where people read.

## You provide
- A short verb phrase in sentence case ("Approve push", "Fork session"). The CSS sets the capitals and tracking; never type capitals yourself.
- Optionally one icon from the Airframe set before the text: `<svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg>`. Buttons size it to 14 px (13 px small).
- An `aria-label` on icon-only buttons.

## Markup
```html
<button type="button" class="af-btn af-btn--primary"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true"><path d="M6 3.5v13l10-6.5z"/></svg>Start a sandbox</button>
<button type="button" class="af-btn af-btn--secondary">Read the docs</button>
<button type="button" class="af-btn af-btn--ghost af-btn--sm">Open trace</button>
<button type="button" class="af-btn af-btn--danger af-btn--sm">Deny</button>
<button type="button" class="af-btn af-btn--secondary af-btn--icon" aria-label="Snapshot sandbox"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg></button>
<button type="button" class="af-btn af-btn--primary" disabled>Start a sandbox</button>
<button type="button" class="af-btn af-btn--primary af-btn--text">Approve for this session</button>
```

| Class | Use |
|---|---|
| `af-btn--primary` | The one action the view exists for. `brand` fill, `on-brand` text. |
| `af-btn--secondary` | Every other real action. `line-strong` hairline, no fill. |
| `af-btn--ghost` | Navigation-like actions inside rows and banners (View diff, Open trace). |
| `af-btn--danger` | Destroy, Deny, Revoke. Red outline and text, never a red fill. |
| `af-btn--sm` | 28 px, inside cards, banners, table rows and card feet. |
| `af-btn--icon` | Square, icon only. Combine with `--sm` for 28 px. |
| `af-btn--text` | Sentence-case Red Hat Text 13.5 px (13 small) instead of mono capitals. Same kinds and sizes. |

## Friendlier where people read, mono where data is

Mono capitals are the default: they belong where the button sits among IDs, counts and keyed data (fleet boards, tables, approval cards, terminals). `af-btn--text` is for surfaces people read as prose: Tower's desk and spaces, dialogs with a sentence in them, question cards, settings. Pick one per surface, not per button: a view mixes the two only where a data panel sits inside a reading page. The kinds, sizes, order and the one-primary rule do not change.

## When to use
- Decisions in approval cards and master caution banners: ghost to inspect, primary to approve, danger to deny.
- Card feet: one small secondary or ghost button on the right.

## Do
- Keep one primary per view region. Approve is primary; Deny is danger beside it.
- Order a decision as inspect (ghost), refuse (danger), accept (primary), left to right.
- Use the native `disabled` attribute; the style follows it.
- Use `af-btn--text` for a whole reading surface (Tower's desk, a dialog with prose), never for one button in a data view.

## Don't
- Don't fill a button with a status color, and don't use yellow for anything that isn't the primary action.
- Don't add shadows, gradients or rounded pills. Radius stays `radius-control` (2px).
- Don't put more than one icon in a button, or an icon after the text.
