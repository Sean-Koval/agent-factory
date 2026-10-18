A toast is a short notice at the bottom centre of the screen on the overlay tone: one sentence, an optional action, the failed mark for a bad outcome, `role="status"`; it lifts above an open bottom drawer, and while a person is mid-decision (a dialog or drawer open, a field focused) non-critical toasts are held and shown afterwards.

## You provide
- A region `af-toasts` with `role="status"` and `aria-live="polite"`, once per page (airframe.js creates it on first use).
- One sentence per toast, with the IDs in `b` (mono): "Snapshot of `HGR-3MX9` saved.", "Approved. Receipt `TWR-RCPT-88A1` is on the record."
- Optionally one action as a small ghost button (`af-toast__act`): Open, Open log, Receipt. Never two.
- `af-toast--bad` with the failed status mark (no word; the sentence says what failed) for a failed outcome.
- Timing: 3.5 s for a plain toast, 7 s with an action or the failed mark; a toast whose cause persists (the connection is lost) stays until it clears.

## Markup
```html
<div class="af-toasts" role="status" aria-live="polite">
  <div class="af-toast"><span class="af-toast__msg">Snapshot of <b>HGR-3MX9</b> saved.</span><button type="button" class="af-btn af-btn--ghost af-btn--sm af-toast__act">Open</button></div>
  <div class="af-toast af-toast--bad"><span class="af-status af-status--failed" aria-hidden="true"><i class="af-status__mark"></i></span><span class="af-toast__msg"><b>HGR-0PZ4</b> failed at test. 38 of 41 passed.</span><button type="button" class="af-btn af-btn--ghost af-btn--sm af-toast__act">Open log</button></div>
</div>
```

With airframe.js:

```js
import { toast } from "./airframe/airframe.js";
toast("Snapshot of HGR-3MX9 saved.", { action: { label: "Open", onClick: openSnapshot } });
toast("HGR-0PZ4 failed at test. 38 of 41 passed.", { tone: "bad", action: { label: "Open log", onClick: openLog } });
toast("Connection to hangar lost. Reconnecting.", { tone: "bad", critical: true, timeout: 0 });
```

`toast(msg, {tone, action, timeout, critical, html})` returns the element (with a `dismiss()`), or `null` when it was held. `inhibited()` says whether toasts are being held; `flush()` shows the held ones.

## Alert inhibition
Airbus inhibits alerts during takeoff and landing; Airframe inhibits them during a decision. While an `af-dialog` is open, an `af-drawer` is open, or a text field has focus, a non-critical toast is not shown. It is held, in order, and shown when the dialog or drawer closes or the field loses focus. A toast with `critical: true` (the connection dropped, the session ended) shows at once. This keeps a denial reason or a steer from being interrupted by "Snapshot saved."

## Z-order
Toast above drawer above scrim: `--af-z-toast` 120, `--af-z-drawer` 110, `--af-z-scrim` 100. A `<dialog>` uses the browser's top layer, above all three, and inhibits toasts while it is open. When a bottom drawer is open (`html.af-drawer-open--bottom`, set by airframe.js), the region moves up by `--af-drawer-inset`, so a toast never hides under a terminal.

## When to use
- The outcome of an action the person just took, when the page does not show it already: saved, approved, sent, copied.
- A failure of such an action, with the way to see more.
- Not for anything that needs a decision (that is a dialog or a card), and not for what the page shows on its own (a status change in a row the person is looking at).

## Do
- Write the sentence with the ID and the number; let the action be the noun it opens.
- Keep a toast quiet: `overlay` ground, a hairline, the one shadow Airframe allows on floating surfaces. No color unless the outcome failed.
- Hold toasts while a person is mid-decision, and show them after, in order.

## Don't
- Don't stack more than three; the oldest leaves.
- Don't use a toast for success theatre ("Great job!") or for a status the dark cockpit already shows.
- Don't color a toast by tone, add an icon per kind, or animate it in. It appears and it leaves.
