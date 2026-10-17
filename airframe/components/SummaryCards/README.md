Summary cards are the four numbers at the top of a console (running, waiting on you, spend today, turn to PR), each a card with a label, a readout, one small graphic and a foot.

## You provide
- For each card: label and icon, a time window as meta (`24 h`, `now`, `limit $200`, `median, 7 d`), the value, a unit, and a foot (change on the left, scope on the right).
- One graphic per card: a sparkline (`af-spark`), a gauge (`af-gauge`), or for the waiting card the held item itself.

## Markup
```html
<div class="af-grid af-grid--4">
  <article class="af-card">
    <div class="af-card__top"><span class="af-lbl"><svg class="af-ic" …>…</svg>Running</span><span class="af-card__meta">24 h</span></div>
    <div class="af-card__value"><span class="af-readout af-readout--m"><b>3</b><b>9</b></span><span class="af-card__unit">of 40 sandboxes</span></div>
    <svg class="af-spark" viewBox="0 0 200 34" role="img" aria-label="Running sandboxes over 24 hours, rising from 28 to 39">
      <line class="af-spark__base" x1="4" y1="30" x2="196" y2="30"/>
      <polyline class="af-spark__line" points="4,30 25.3,25.3 … 196,4"/>
      <circle class="af-spark__end" cx="196" cy="4" r="2.6"/>
    </svg>
    <div class="af-card__foot"><span><b>+4</b> since yesterday</span><span>us-east4</span></div>
  </article>

  <!-- spend: cents as a minor part, gauge with the alert bug -->
  <div class="af-card__value"><span class="af-readout af-readout--m"><b class="af-readout__p">$</b><b>1</b><b>4</b><b>2</b><span class="af-readout__minor">.18</span></span></div>
  <div class="af-gauge" role="img" aria-label="71 percent of the daily limit; alert at 90 percent">
    <b class="af-gauge__fill" style="width:71%"></b><span class="af-gauge__bug" style="left:90%"></span>
  </div>
</div>
```

Sparkline geometry: viewBox `0 0 200 34`, 4 px inset; x = 4 + i/(n−1)·192, y = 30 − (v−min)/(max−min)·26. The line is `fg-muted`, the baseline `line`, the endpoint dot `brand` with a `brand-text` ring.

## When to use
- The first row of a fleet, cost or eval overview. Four cards, or two on narrow screens.
- Light the waiting card (`af-card--lit`) while its count is above zero; show the held sandbox with an approval status and keyed `held` / `expires`.

## Do
- Give each sparkline and gauge a `role="img"` and an `aria-label` that states the trend in words.
- Keep feet parallel: a change in `<b>` on the left, scope on the right.

## Don't
- Don't color sparklines by direction (no green up, red down). The brand dot marks "now", nothing else.
- Don't add axes, gridlines or tooltips to a sparkline; link to the full chart instead.
- Don't put more than one number per card.
