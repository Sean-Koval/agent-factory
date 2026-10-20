The hero pairs an Archivo Expanded headline ("Forty agents. One needs you."), a short lede and two actions with a live-looking panel: three readouts in display windows and three fleet rows, one of them waiting on a person, over an optional dot field.

## You provide
- An eyebrow: the product mark and a label with the version.
- A headline of two short sentences, each in its own `<span>` so the break falls between them.
- A lede of one sentence (about 20 words) and one supporting note.
- One primary and one secondary action.
- The panel: a label with scope, a lit count, three readouts with keys, and three rows (tail number, model, status, time) with exactly one `is-attention` row.

## Markup
```html
<section class="af-hero" aria-labelledby="hero-title">
  <div class="af-hero__copy">
    <span class="af-row"><span class="af-mark af-hue--hangar">…</span><span class="af-lbl">hangar<span class="af-lbl__sub af-mono">v0.9</span></span></span>
    <h1 class="af-hero__title" id="hero-title"><span>Forty agents.</span> <span>One needs you.</span></h1>
    <p class="af-hero__lede">hangar runs coding agents in isolated cloud sandboxes, holds risky steps for a human, and files a receipt for every decision.</p>
    <div class="af-hero__actions">
      <button type="button" class="af-btn af-btn--primary">Start a sandbox</button>
      <button type="button" class="af-btn af-btn--secondary">Read the docs</button>
    </div>
    <p class="af-hero__note">Works with Claude Code, Codex, pi and Antigravity. MCP server included.</p>
  </div>
  <div class="af-hero__stage">
    <div class="af-dotfield" aria-hidden="true"></div>
    <div class="af-panel af-hero__panel">
      <div class="af-hero__panel-head"><span class="af-lbl">Fleet<span class="af-lbl__sub af-mono">us-east4</span></span><span class="af-status af-status--running af-status--lit"><i class="af-status__mark"></i>39 running</span></div>
      <div class="af-readouts">…three af-window…</div>
      <ul class="af-list">
        <li class="af-list__row is-attention"><span class="af-list__main"><span class="af-list__id">HGR-3MX9</span><span class="af-list__sub">gpt-5.1</span></span>
          <span class="af-status af-status--approval"><i class="af-status__mark"></i>Holding at PR</span><span class="af-list__time">00:41:07</span></li>
      </ul>
    </div>
  </div>
</section>
```

The headline scales with its column (`10.8cqi`, 32–64 px, `display-xl` at full size). Below 900 px the panel moves under the copy.

`af-list` is the compact row list used here and in status examples: rows are 32 px on `line-subtle` dividers; set `--af-list-status` / `--af-list-time` to size the status and time columns.

## Do
- Keep it to one hero per page, with real numbers and real tail numbers.
- Use the dot field only behind this panel; it is the one texture allowed in marketing.

## Don't
- Don't add gradients, glows, photos or 3D renders behind the headline.
- Don't set the headline in all caps or add a third sentence.
- Don't light more than one row in the panel.
