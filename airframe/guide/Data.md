# Data

Airframe consoles are mostly data. Make the data the brightest thing on the screen and everything around it quieter.

## Density

- Size rows at `row-h` (32px); dense tables at `row-h-compact` (28px). Session lanes are `lane-h` (30px), trace spans `span-h` (28px).
- Set UI text in `body` (14px) and table cells in `body-s` (13px). Set IDs in `mono`, numbers in `data`, inline values in `mono-s`, keys and headers in `label-s`.
- Pad cards `space-16`; gap card grids `space-12`. Don't add air to a dense view; add hierarchy.

## Tables

- Put a table in `af-table-wrap` (`raised`, no border, scrolls sideways when narrow). Never box a table again inside a card.
- Headers have no fill: `label-s` capitals in `fg-subtle`, left-aligned (right-aligned over numbers), with a 1px `line` rule beneath.
- Divide rows with `line-subtle`. No zebra stripes, no vertical rules. Hover is a faint `fg` tint; the selected row (`aria-selected="true"`) takes `selected` and a 2px `brand-text` edge on its first cell.
- Lead with the tail number. A hangar fleet table reads: ID, environment, harness and model, status, CPU, age, cost.
- Right-align numbers with `af-num` and tabular figures. Truncate descriptions with an ellipsis; never truncate an ID or a number.
- A row that needs a person (`is-attention`) takes a faint `status-approval` tint; nothing else in the table is tinted. Failed and denied rows show their status mark and word only.
- Draw in-cell bars (CPU, budget) as 2px hairlines: `fg-muted` fill on a `line` track, never a status color.

## Inline data: keyed

Write metadata as key and value pairs, never as `a · b · c` strings.

```html
<span class="af-meta">
  <span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">Policy</span><span class="af-meta__val">require-approval-main-push</span></span>
  <span class="af-meta__item"><span class="af-meta__key">Harness</span><span class="af-meta__val">codex</span></span>
  <span class="af-meta__item af-meta__item--strong"><span class="af-meta__key">Model</span><span class="af-meta__val">gpt-5.1</span></span>
</span>
```

- Keys are short nouns in small mono capitals, `fg-subtle`: POLICY, HARNESS, MODEL, ENV, STAGE, CPU, COST, AGE, REGION, HELD.
- Values are mono in `fg-muted`. Use `af-meta__item--strong` (`fg`) for the one value that matters most.
- Only a policy or approval value may take a status color: `af-meta__item--approval` or `af-meta__item--failed`.
- Order items from most identifying to least. Keep to five per line; let the rest wrap.
- For an inspector or detail pane, use `af-kv` (a key/value grid) instead.
- The middle dot exists in one place only: the sub-label of `af-lbl` (`FLEET · US-EAST4`).

## Readouts

- Use a readout for the one to four numbers a view is about: sandboxes this week, held for a human, spend today, turn to PR.
- Build it as digits on unlit cells inside a recessed window: `af-window` (`display-window`) holding `af-readout` with `--l`, `--m` or `--s`. Each digit or letter is a `<b>` on a `readout-cell`; punctuation is `<b class="af-readout__p">`.
- Put the unit and caption outside the cells: the unit in `body` `fg-subtle` beside it ("of 40 sandboxes"), the caption in `label` capitals below it.
- Never use readout cells in tables, inline data or running text.

## Traces

TraceSpans draws one turn's spans on a shared time axis.

- Rows are `span-h`, indented 16px per depth, with the span name, its kind in `mono-s` `fg-subtle`, and its duration right-aligned in `data`.
- Model calls are solid `span-model`. Tool calls are a 1px `span-tool` outline with a faint fill. Sandbox commands are solid `span-sandbox`.
- Waiting on a human is hatched `status-approval` with an open end while it waits.
- A failed span is a 1.5px `status-failed` outline over a faint tint, with a triangle at its end; never a solid red bar. Its duration turns `status-failed`; a waiting span's turns `status-approval`.
- Draw the critical path as one 1.5px `brand-text` line through the spans that set the turn's duration. It is the only yellow in the trace besides a selected row (`brand-wash`).
- Label the axis in 10px mono `fg-subtle` (`0s` … `60s`) on a `line` rule; gridlines are `line-subtle`. Selecting a span opens its detail beside the trace: keyed data and the command output on `terminal-bg`.

## Lanes

SessionLanes draws one lane per session over the last hour.

- Each lane is `lane-h`, labelled with the tail number in mono and harness and model in `fg-subtle`.
- Stages are fills on a greyscale ramp: `stage-plan`, `stage-edit`, `stage-test` (the ramp runs toward `fg` as work advances, in both themes). PR is a 1px outline in `fg-muted`; a merged PR ends in a check in a ring. Queued time is a dashed `status-queued` outline.
- Waiting on a human is hatched `status-approval`. A failure ends the lane with a `status-failed` triangle; a denial with a small `status-denied` placard.
- The now line is a 1px `brand-text` rule at the right edge with a square cap, and the axis runs `-60 min` to `now` (the `now` tick in `brand-text`).
- A selected lane takes `brand-wash` and a 2px `brand` edge on its label.

## Fleet board

FleetView shows every sandbox in a fleet as a stand (tile), grouped by pool, and switches between the board and lanes with two `aria-pressed` buttons.

- Each pool header shows the pool name, keyed counts (`RUNNING 16  WAITING 1  QUEUED 3`) and capacity (`22 of 24 slots`). The fleet header carries the pool schedule.
- A stand is tonal: a faint `fg` tint on `raised`, no border, `radius-control`, `space-4` from its neighbours. It shows the short code (`7Q2K`), its status mark, four stage pips (plan, edit, test, PR) and nothing else.
- Running and queued stands stay grey. Needs approval, failed and denied stands take a 1px inset ring and a faint tint in their status color, and their current pip lights in it too. Off stands are a 1px `line` outline with no fill; free slots a dashed `line` outline.
- A selected stand takes a 1px `brand-text` outline offset 2px, and the inspector line under the board shows its keyed data and actions.

## Charts

- Draw charts in greyscale: `chart-1` (primary, `fg`-strength), `chart-2`, `chart-3`, `chart-4`, with `chart-6` for grid emphasis.
- Spend at most one attention series per chart, in `chart-5`. It shares the caution orange on purpose: it means "look here".
- Yellow appears in a chart only as the now line or now point, or a target or limit marker.
- Never use product hues or status colors as series. Errors are `status-failed` markers or outlines, never fills.
- Use single-hue greyscale for sequential scales and heatmaps; never red-to-green.
- Draw axes in `rule`, gridlines in `line-subtle`, tick labels in 10px mono `fg-subtle`. Label series directly where possible instead of a legend.
- Draw sparklines as a thin `fg-muted` line over a `line` baseline, ending in a `brand` dot on the latest value (the now point). Gauges are a `line` track with an `fg-muted` fill and a `brand-text` bug at the limit.

## Tabular figures

Every number that can sit above another uses tabular figures: `font-variant-numeric: tabular-nums`. The `data` style, `af-num`, `af-mono`, `af-meta__val` and `af-readout` already set it. Right-align numeric columns and keep decimals consistent within a column.
