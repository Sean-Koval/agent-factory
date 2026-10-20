# FleetBays

The fleet as bays: one box per sandbox, grouped by environment, showing what it is doing, for whom, how far it has got and the one action it needs.

## What you provide

- **Groups**: environment name and icon (`environment`, or `gpu`), keyed counts, the repo.
- **Per sandbox**: tail number, state (running, queued, approval, failed, denied, off), the work (job title or session name), kind and owner, harness, stage (plan, edit, test, PR or none), age, hours left of its lease, and for attention states the reason (`Held`, `Question`, `Policy`, `Error`) and its text.
- **One action per bay**: Review or Answer (primary, needs approval), Retry or Decision (secondary), Terminal, Resume or Open job (ghost).

## Markup

```html
<div class="af-bays">
  <article class="af-bay af-bay--approval" aria-label="HGR-3MX9, Needs approval">
    <div class="af-bay__top"><span class="af-bay__id">HGR-3MX9</span><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></div>
    <p class="af-bay__title">Push the refunds migration to main</p>
    <span class="af-meta"><span class="af-meta__item"><span class="af-meta__key">job by</span><span class="af-meta__val">sean</span></span><span class="af-meta__item"><span class="af-meta__key">harness</span><span class="af-meta__val">codex</span></span></span>
    <div class="af-track" aria-label="Stage PR">
      <span class="af-track__seg af-track__seg--done"><i></i>Plan</span><span class="af-track__seg af-track__seg--done"><i></i>Edit</span>
      <span class="af-track__seg af-track__seg--done"><i></i>Test</span><span class="af-track__seg af-track__seg--now"><i></i>PR</span>
    </div>
    <p class="af-bay__note"><b>Held</b>Push to main held by require-approval-main-push.</p>
    <div class="af-bay__foot">
      <span class="af-bay__time"><span><b>41 min</b> · 2.1 h left</span><span class="af-bay__left" aria-hidden="true"><i style="width:53%"></i></span></span>
      <button type="button" class="af-btn af-btn--primary af-btn--sm">Review</button>
    </div>
  </article>
  <button type="button" class="af-bay af-bay--new"><svg class="af-ic">…plus…</svg>Start in base-codex</button>
</div>
```

| State | Modifier | Box | Track's current segment |
|---|---|---|---|
| Running | (none) | tonal | `fg` |
| Starting | `af-bay--queued` | tonal, no stage | none |
| Needs approval | `af-bay--approval` | 1px orange inset ring, faint tint | orange |
| Failed / Denied | `af-bay--failed` / `--denied` | 1px red inset ring, faint tint | red |
| Paused / spun down | `af-bay--off` | hollow hairline, muted text | none |
| Selected | `is-selected` | 1px brand ring outside | unchanged |

The `af-track` stage track's words are `label-s` in `fg-subtle` (a reached stage `fg-muted`, the current one `fg`), so the stages ahead still read; the pips carry the position. The track and the `af-bay__left` lease bar are shared with other views; `af-cap` (capacity) and `af-person` sit beside them in `viz.css`.

## When to use

The middle density of the fleet: enough room to read each task and act on it without opening anything, for up to about 60 sandboxes. Use FleetView (Board) for the whole fleet at a glance, FleetColumns to sort by what needs a person, FleetOwners to see who is using the capacity. All four take the same data; offer them as views of one page.

## Do

- Order each group attention first (approval, failed, denied), then running, starting, paused (the order in `guide/Status.md`).
- Keep one action per bay; the rest live in the sandbox's detail.
- End each group with the dashed "Start in …" bay, so capacity reads as room, not as empty boxes.

## Don't

- Don't color running bays, the track or the lease bar.
- Don't put more than one primary button in a bay, or a primary button on anything but needs approval.
- Don't truncate the tail number; the title clamps to two lines instead.
