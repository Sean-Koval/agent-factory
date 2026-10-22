# How to consume

How a tool loads Airframe: the files, the order and the first card.

Airframe lives in [Sean-Koval/agent-factory](https://github.com/Sean-Koval/agent-factory): this folder is the source, `theme/` is what tools load. Tool repos vendor the `theme/` files at a `theme-vN` tag with their own `scripts/sync-airframe.sh` and never edit them.

1. Load `airframe.css`: every token as `--af-<name>`. It is generated from `tokens.json`; never edit it by hand. Night values sit under `:root, [data-theme="dark"]`, Day under `[data-theme="light"]` (and the OS light preference when no theme is pinned); spacing, radius, layout, icon, font tokens and `--af-font-display`, `--af-font-sans`, `--af-font-mono` sit on `:root`.
2. Load `airframe-components.css`: the font import, the `.af-type-<style>` classes, then `base.css`, `core.css` and `viz.css`.
3. Headlines use `font-family: var(--af-font-display); font-stretch: var(--af-display-stretch)`. Google serves Archivo as one variable family with a width axis; the stretch gives Archivo Expanded.
4. Set `data-theme="dark"` or `data-theme="light"` on `<html>` (or on any element, for a nested scope).
5. Build with the `af-` classes (BEM: `af-card__foot`, `af-btn--primary`). For anything new, use tokens as `var(--af-<name>)`; never hard-code a color, size or font.

```html
<html data-theme="dark">
<head>
  <link rel="stylesheet" href="airframe/airframe.css">
  <link rel="stylesheet" href="airframe/airframe-components.css">
</head>
<body>
  <article class="af-card">
    <div class="af-card__top">
      <span class="af-lbl">Sandbox<span class="af-lbl__sub af-mono">us-east4</span></span>
      <span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span>
    </div>
    <span class="af-id">HGR-3MX9</span>
    <span class="af-meta">
      <span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">Policy</span><span class="af-meta__val">require-approval-main-push</span></span>
      <span class="af-meta__item"><span class="af-meta__key">Harness</span><span class="af-meta__val">codex</span></span>
    </span>
    <div class="af-card__foot"><span>Held <b>41 min</b></span><button class="af-btn af-btn--primary af-btn--sm">Review</button></div>
  </article>
</body>
</html>
```

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
