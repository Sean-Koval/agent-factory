# StageRail

Plan, edit, test, PR as real progress: a rail with four stops and a glowing head (rows and consoles), a ring of four arcs (board cards) or a four-segment capsule (cards and tiles). One component, three shapes, one rule: grey while running, the status color on the head or current segment when a person is needed or the agent stopped.

## What you provide

- The current stage (0–3, or none for an agent that has not started) and how far through it (0–1). The rail's `--p` is `(stage + fraction) × 33.333%`.
- Whether that fraction was reported by the agent or is an estimate (from elapsed time against the stage's usual length). Fill solid only for a reported pct; an estimate takes `--est`.
- The status, when it is approval, failed or denied, as the modifier.
- For the labeled rail, the four stage words.

## Markup

```html
<!-- rail: the track, the done part, four stops (<b>), optional labels (<span>), the head -->
<span class="af-rail" role="img" aria-label="Test stage, 60%" style="--p:86.7%">
  <i class="af-rail__track"></i><i class="af-rail__done"></i>
  <b class="af-rail__stop is-on"></b><b class="af-rail__stop is-on"></b><b class="af-rail__stop is-on"></b><b class="af-rail__stop"></b>
  <i class="af-rail__head"></i>
</span>
<span class="af-rail af-rail--labeled af-rail--approval" style="--p:98%">…<span class="af-rail__lab">Plan</span><span class="af-rail__lab">Edit</span><span class="af-rail__lab">Test</span><span class="af-rail__lab">PR</span><i class="af-rail__head"></i></span>
<span class="af-rail af-rail--est" role="img" aria-label="Test stage, about 45% (estimate)" style="--s:66.7%;--p:81.7%">…</span>   <!-- estimated: dotted from the stage start, hollow head -->
<span class="af-rail af-rail--none" aria-hidden="true"><i class="af-rail__track"></i><b class="af-rail__stop"></b>…</span>   <!-- not started -->

<!-- ring: four arcs of a 30 px circle; draw the arcs with stroke-dasharray (the preview shows the arithmetic) -->
<svg class="af-ring af-ring--approval" viewBox="0 0 30 30" role="img" aria-label="PR stage">
  <circle class="af-ring__track" …/><circle class="af-ring__fill" …/> … <text x="15" y="18">PR</text>
</svg>

<!-- capsule: four segments, the current one filled to --p -->
<span class="af-capsule" role="img" aria-label="Stage Test">
  <i class="af-capsule__seg is-done"></i><i class="af-capsule__seg is-done"></i><i class="af-capsule__seg is-now" style="--p:60%"></i><i class="af-capsule__seg"></i>
</span>
```

| Part | Class | Notes |
|---|---|---|
| Rail | `af-rail` | 16 px tall, `--p` 0–100%. `__track` is `rail`, `__done` is `rail-done` to `--p`, `__stop` (`is-on` once passed), `__head` an 8 px dot ringed by `--ground` (set it to the surface the rail sits on; `raised` by default) with a soft `rail-glow`. `--labeled` adds 16 px for the `__lab` row; `--none` dashes the track. |
| Ring | `af-ring` | An SVG: `__track` arcs in `rail`, `__fill` arcs in `rail-done`; the stage letter in the middle; `--none` is a dotted ring. |
| Capsule | `af-capsule` | 5 px tall; `__seg` `is-done` is full, `is-now` fills to `--p`; `--none` hides it. |
| Estimate | `--est` on any of the three | Solid fill is only for what the agent reported. With `--est`, the rail fills solid to the current stage's start (`--s`) and dotted from there to `--p`, and the head is a hollow ring with no glow; the ring dots the current arc (`__est`); the capsule dots the current segment. Say "about" and "estimate" in the label. |
| Status | `--approval`, `--failed`, `--denied` | On any of the three: the head, the fill of the current arc or the current segment takes the status color; the rest stays grey. The glow follows it. |

## When to use

Wherever the old four dashes were: AgentRow (rail), AgentCard (ring in the head, capsule under the now-line), the opened console (labeled rail), FleetBays and FleetView tiles (`af-track` and `af-stand__pips` share the `rail` tokens). Use the ring where there is only a corner, the capsule where there is a line but no words, the rail where there is room for stops.

## Do

- Animate `--p` in place when a tick arrives (the fill and the head transition over 900 ms); never re-render the rail.
- Keep the head's glow: it says "moving". It is the one glow in the system besides the latest timeline dot.
- Give the rail a `role="img"` and a label that says the stage and the percentage.

## Don't

- Don't color a running agent's rail: `rail-done` is grey in both themes.
- Don't draw an estimate solid. If the agent did not report a pct, the current stage is dotted (`--est`) or empty; a solid fill is a claim.
- Don't add a fifth stop or rename the four; the stages are plan, edit, test, PR everywhere.
- Don't use the rail for anything that is not an agent's progress through its work (capacity is `af-cap`; a gauge is `af-gauge`).
