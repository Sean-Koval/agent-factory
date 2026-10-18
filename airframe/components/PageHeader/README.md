A page header is the top of every console view: a title in the display face at one of two sizes, a lede, a summary line (a status mark, keyed counts, capacity) and an actions slot on the right; below 760 px the actions stack under the text.

## You provide
- A title: `af-page-head__title` at 36 px for a page (`Fleet`, `Approvals`), or `af-page-head--s` on the header for 24 px on a detail (`HGR-3MX9 is holding at PR`, with the tail number in `af-id`). Use `h1` on a page and `h2` on a detail.
- Optionally an eyebrow `af-lbl` above the title (`SANDBOX · base-codex · us-east4`) and a one-sentence lede in `fg-muted`.
- A summary line: the status that leads (the group rule: needs you first, lit when it is yours), keyed counts in `af-meta` (`RUNNING 31  QUEUED 4  FAILED 1`), and capacity as `af-cap`.
- Actions: at most one primary, then secondary and ghost, in `af-page-head__actions`. Small buttons on a detail header.
- `af-page-head--rule` when the header sits straight on the canvas above a list; omit it above cards.

## Markup
```html
<header class="af-page-head af-page-head--rule">
  <div class="af-page-head__text">
    <h1 class="af-page-head__title">Fleet</h1>
    <p class="af-page-head__lede">Forty sandboxes across three environments. One needs you.</p>
    <div class="af-page-head__sum">
      <span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>1 waiting on you</span>
      <span class="af-meta">…RUNNING 31 · QUEUED 4 · FAILED 1 · OFF 3…</span>
      <span class="af-cap af-cap--sm">27 of 120 slots<span class="af-cap__bar"><i style="width:22.5%"></i></span></span>
    </div>
  </div>
  <div class="af-page-head__actions">
    <button type="button" class="af-btn af-btn--ghost">Filter</button>
    <button type="button" class="af-btn af-btn--primary">Start a sandbox</button>
  </div>
</header>

<header class="af-page-head af-page-head--s">
  <div class="af-page-head__text">
    <span class="af-lbl">Sandbox<span class="af-lbl__sub">base-codex</span></span>
    <h2 class="af-page-head__title"><span class="af-id">HGR-3MX9</span> is holding at PR</h2>
    <p class="af-page-head__lede">Push to main needs your approval. …</p>
    <div class="af-page-head__sum">…</div>
  </div>
  <div class="af-page-head__actions">…small buttons…</div>
</header>
```

| Part | Class | Notes |
|---|---|---|
| Title | `af-page-head__title` | Archivo Expanded 36/1.05 (28 when narrow); `--s` gives 24/1.1 (22 narrow). An `af-id` inside takes DM Mono at .86em. |
| Lede | `af-page-head__lede` | 14 px `fg-muted`, 62ch max. |
| Summary | `af-page-head__sum` | A wrapping row: status, `af-meta`, `af-cap`. |
| Actions | `af-page-head__actions` | Right-aligned, bottom-aligned with the summary; wraps; one primary. |

## When to use
- The top of every view in hangar (Fleet, Jobs, Sessions, Environments, Approvals) and Tower (Desk, Needs you, Agents, Record), and the head of a detail page or a drawer that has a page of its own.

## Do
- Lead the summary with what needs a person, lit only when it is this person; then counts in the attention order, then capacity.
- Write the lede as a statement of the view ("Forty sandboxes across three environments. One needs you."), not a description of the feature.
- Keep the title short; the lede carries the sentence.

## Don't
- Don't put more than one primary action in the header, and don't put a status color on a button.
- Don't repeat the summary counts in the lede.
- Don't stack a rule and a card: use `--rule` only above a list or table on the canvas.
