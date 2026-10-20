A drawer is a sheet over the page: on the right at 480 px for the detail of one object, or along the bottom at 40vh for a terminal or log; it has a head, a body and a foot, sits over a scrim, and keeps the order toast above drawer above scrim; airframe.js adds Escape, focus return and an inert page.

## You provide
- `<aside class="af-drawer af-drawer--right">` or `af-drawer--bottom`, with `role="dialog"` and `aria-labelledby` when it has a scrim (airframe.js sets `aria-modal`), and an `af-scrim` before it (airframe.js inserts one).
- A head: the object's status mark, a title with the tail number in `af-id`, and an icon-only ghost Close button; a bottom drawer's head is 40 px with an `af-lbl` (`TERMINAL · HGR-3MX9`), a word about who has control, and the actions.
- A body (`af-drawer__body`, scrolls) and, on a right sheet, a foot with the decision in inspect, refuse, accept order.
- `is-open` to show it; `--af-drawer-w` and `--af-drawer-h` to change the size per page; `af-drawer__grip` on a bottom drawer that resizes.

## Markup
```html
<div class="af-scrim"></div>
<aside class="af-drawer af-drawer--right" id="approval" role="dialog" aria-labelledby="dr1">
  <header class="af-drawer__head">
    <span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i></span>
    <h2 class="af-drawer__title" id="dr1"><span class="af-id">TWR-APR-0391</span> git push origin main</h2>
    <button type="button" class="af-btn af-btn--ghost af-btn--sm af-btn--icon" aria-label="Close"><svg class="af-ic" …>close</svg></button>
  </header>
  <div class="af-drawer__body">…af-kv, checks, receipt…</div>
  <footer class="af-drawer__foot">
    <button type="button" class="af-btn af-btn--ghost af-btn--sm">View diff</button>
    <button type="button" class="af-btn af-btn--danger af-btn--sm">Deny</button>
    <button type="button" class="af-btn af-btn--primary af-btn--sm">Approve push</button>
  </footer>
</aside>

<aside class="af-drawer af-drawer--bottom" id="terminal" aria-labelledby="dr2">
  <span class="af-drawer__grip" aria-hidden="true"></span>
  <header class="af-drawer__head">
    <span class="af-lbl"><svg class="af-ic" …>terminal</svg>Terminal<span class="af-lbl__sub af-mono">HGR-3MX9</span></span>
    <h2 class="af-drawer__title" id="dr2">Agent has control</h2>
    <button type="button" class="af-btn af-btn--secondary af-btn--sm">Take over</button>
    <button type="button" class="af-btn af-btn--ghost af-btn--sm af-btn--icon" aria-label="Close">…</button>
  </header>
  <div class="af-drawer__body"><div class="af-term">…</div></div>
</aside>
```

With airframe.js:

```js
import { drawer } from "./airframe/airframe.js";
drawer.open("#approval");        // scrim, inert page, focus in, Escape and scrim-click close
drawer.close("#approval");       // focus returns, held toasts show
drawer.open("#terminal", { scrim: false });   // a bottom drawer the page keeps working above
```

`drawer.open(el, {scrim})`, `drawer.close(el)`, `drawer.toggle(el)` and `drawer.isOpen(el)`; the element fires `af:open` and `af:close`. A bottom drawer sets `html.af-drawer-open--bottom`, which moves the toast region up by `--af-drawer-inset` (the drawer height).

| Part | Class | Notes |
|---|---|---|
| Scrim | `af-scrim` | The canvas at 72%, `--af-z-scrim` (100). `is-open` shows it. |
| Drawer | `af-drawer--right` / `--bottom` | `raised`, a 1px `line` on the inner edge, `--af-z-drawer` (110). Full width below 760 px. |
| Head | `af-drawer__head` | 56 px (40 on a bottom drawer), `line-subtle` below; title 16/600 in the body face, one line. |
| Body | `af-drawer__body` | 20 px padding (none on a bottom drawer); scrolls. |
| Foot | `af-drawer__foot` | Right-aligned; a leading ghost button goes left. |

## When to use
- The right sheet: the detail of one row (an approval, a sandbox, a receipt) when the list should stay in view; Tower's record and approval drawers; hangar's Fleet detail when the page is narrower than 1080 px.
- The bottom drawer: a terminal, a log or a trace under the page the person keeps reading; it opens without a scrim.
- Not for a decision with nothing behind it (that is a dialog) and not for navigation.

## Do
- Keep one drawer per side open at a time; a second detail replaces the first.
- Put the object's status and tail number in the head, and the decision in the foot in inspect, refuse, accept order.
- Say who has control in a terminal drawer's head ("Agent has control", "You have control") and make the hand-off a button.
- Return focus to the opener on close and keep the toasts above the drawer.

## Don't
- Don't nest a dialog in a drawer except for a confirm; don't open a drawer from a dialog.
- Don't add a shadow to a drawer; the scrim and the 1px line do the work.
- Don't make the bottom drawer modal; the page above stays usable.
