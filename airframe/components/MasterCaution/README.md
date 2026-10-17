The master caution banner is the one large block of color in Airframe: a flat lamp (orange caution or red warning, black legend) beside a sentence, keyed data and up to two actions; when nothing needs a person, the lamp goes dark.

## You provide
- The level: `af-master--caution` (a person is needed: an approval, a held push) or `af-master--warning` (something failed and stopped).
- One sentence that names the sandbox and what it needs: "HGR-3MX9 is holding at PR. Push to main needs a reviewer."
- Keyed data, with the cause marked `--approval` or `--failed`.
- One or two small buttons: an inspect action (ghost) and the decision (primary for approve, secondary for retry).

## Markup
```html
<section class="af-master af-master--caution" role="alert" aria-label="Master caution">
  <div class="af-master__lamp" aria-hidden="true">Master<br>caution</div>
  <div class="af-master__body">
    <p class="af-master__title">HGR-3MX9 is holding at PR. Push to main needs a reviewer.</p>
    <span class="af-meta"><span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">policy</span><span class="af-meta__val">require-approval-main-push</span></span>…</span>
  </div>
  <div class="af-master__act">
    <button type="button" class="af-btn af-btn--ghost af-btn--sm">View diff</button>
    <button type="button" class="af-btn af-btn--primary af-btn--sm">Approve push</button>
  </div>
</section>

<!-- nothing pending: the lamp is unlit -->
<section class="af-master af-master--clear" aria-label="No cautions">
  <div class="af-master__lamp" aria-hidden="true">Master<br>caution</div>
  <div class="af-master__body"><p class="af-master__title">No cautions.</p><span class="af-meta">…</span></div>
  <div class="af-master__act"></div>
</section>
```

Lamp fills are `lamp-caution` and `lamp-warning` with `on-lamp` text (8.9:1 and 6.4:1). The clear lamp is `readout-cell` with `fg-subtle` text.

## When to use
- At the top of a console, under the header, one banner per open item, newest first; stack them 8 px apart.
- Keep the clear state on screen so people learn where to look.

## Do
- Write the sentence as what happened, then what is needed.
- Remove the banner when the item is decided; its receipt lives in the approval history.

## Don't
- Don't add gloss, gradients, glow, blinking or icons to the lamp. Flat fill, black capitals.
- Don't use a lamp for information, success or progress.
- Don't use brand yellow for a lamp. Caution is orange so it never reads as the brand.
