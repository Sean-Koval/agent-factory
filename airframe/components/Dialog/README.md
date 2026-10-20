A dialog is a native `<dialog>` on the raised tone: a title in the body face, a body, and a footer whose buttons run inspect, refuse, accept from left to right; the confirm variant replaces `window.confirm()`, and the danger variant makes the confirming verb a danger button instead of the primary.

## You provide
- `<dialog class="af-dialog">` with `aria-labelledby` pointing at the title; `showModal()` opens it, so the backdrop is the scrim and focus is trapped.
- A `<form method="dialog" class="af-dialog__form">` inside, so buttons with a `value` close the dialog and set `returnValue` ("ok", "cancel").
- A title as a question or a verb phrase ("Destroy HGR-3MX9?", "Fork this session"), a body of one or two sentences with the consequence and the IDs, optionally fields (`af-field`) or keyed data (`af-kv`).
- A footer: an optional ghost inspect button on the left (Open trace), the refusing button as secondary (Keep it, Not now, Cancel), the confirming verb last as primary, or as danger when it destroys something (`af-dialog--danger`).
- `af-btn--text` on the buttons where people read (Tower's desk, forms), `af-dialog--wide` (640 px) for a form with several fields.

## Markup
```html
<dialog class="af-dialog af-dialog--danger" aria-labelledby="d2">
  <form method="dialog" class="af-dialog__form">
    <header class="af-dialog__head"><h2 class="af-dialog__title" id="d2">Destroy <span class="af-id">HGR-3MX9</span>?</h2></header>
    <div class="af-dialog__body">
      <p>The sandbox and its 2 snapshots are deleted. The job's receipt stays on the record.</p>
      <p>It is holding a push to main that <b>Priya</b> has not decided yet; destroying it drops the request.</p>
    </div>
    <footer class="af-dialog__foot">
      <button type="button" class="af-btn af-btn--ghost">Open trace</button>
      <button type="submit" class="af-btn af-btn--secondary" value="cancel">Keep it</button>
      <button type="submit" class="af-btn af-btn--danger" value="ok">Destroy</button>
    </footer>
  </form>
</dialog>
```

With airframe.js, which builds exactly this and returns a promise:

```js
import { confirm } from "./airframe/airframe.js";
if (await confirm({ title: "Destroy HGR-3MX9?", body: "The sandbox and its 2 snapshots are deleted.", ok: "Destroy", cancel: "Keep it", danger: true })) destroy();
```

`confirm({title, body, ok, cancel, danger, inspect: {label, onClick}, html, text})` resolves `true` on the confirming button and `false` on the refusing one, on Escape and on a click outside; focus returns to the element that had it, and toasts held meanwhile show after it closes.

| Part | Class | Notes |
|---|---|---|
| Dialog | `af-dialog` | 480 px (`--wide` 640), `lifted`, the 18 px sheet radius, `shadow-2` and the `edge-hi` highlight; no border. `::backdrop` is the canvas at 72%. |
| Title | `af-dialog__title` | `title-m`: Red Hat Text 20/600. An eyebrow `af-lbl` may sit above it. |
| Body | `af-dialog__body` | 14 px `fg-muted`; `b`, `af-mono` and `af-id` in `fg`. Scrolls when tall. |
| Footer | `af-dialog__foot` | Right-aligned; a leading ghost button is pushed to the left. |

## When to use
- A decision that must be made before anything else happens: destroy, revoke, leave with unsaved edits, approve for the session.
- A short form that creates one thing (fork, new environment) when a page would be too much.
- Not for an approval of an agent's action (that is an ApprovalCard, in the page or a drawer) and not for information (that is a toast or the page).

## Do
- Put the consequence in the body with the real numbers and IDs, and name the confirming button with the verb: Destroy, Revoke, Fork session. Never OK.
- Order inspect, refuse, accept. Make the refusing button the first in focus order, so Enter does not destroy.
- Use the danger variant only when something is lost; approving is primary.

## Don't
- Don't fill the confirming button red; danger is a red outline and text.
- Don't open a dialog from a dialog, and don't open one to show a result.
- Don't use `window.confirm()` or `alert()`; they ignore the theme, the fonts and the order.
