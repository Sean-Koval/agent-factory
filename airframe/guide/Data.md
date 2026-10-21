# Data

Airframe consoles are mostly data. Make the data the brightest thing on the screen and everything around it quieter.

## Density

- Size rows at `row-h` (32px); dense tables at `row-h-compact` (28px). Session lanes are `lane-h` (30px), trace spans `span-h` (28px).
- Set UI text in `body` (14px) and table cells in `body-s` (13px). Set IDs in `mono`, numbers in `data`, inline values in `mono-s`, keys and headers in `label-s`.
- Pad cards `space-16`; gap card grids `space-12`. Don't add air to a dense view; add hierarchy.

## Tables

- Put a table in `af-table-wrap` (`raised`, no border, scrolls sideways when narrow). Never box a table again inside a card.
- Headers have no fill: `label-s` (sentence-case sans) in `fg-subtle`, left-aligned (right-aligned over numbers), with a 1px `line` rule beneath.
- Divide rows with `line-subtle`. No zebra stripes, no vertical rules. Hover is a faint `fg` tint; the selected row (`aria-selected="true"`) takes `selected` and a 2px `fg` edge on its first cell.
- Lead with the tail number. A hangar fleet table reads: ID, environment, harness and model, status, CPU, age, cost.
- Right-align numbers with `af-num` and tabular figures. Truncate descriptions with an ellipsis; never truncate an ID or a number.
- A row that needs a person (`is-attention`) takes a 3px `status-approval` edge on its first cell; nothing in a table is tinted. Failed and denied rows show their status mark and word only. A selected lit row keeps the status edge and says "selected" with its fill.
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

- Keys are short nouns in small sentence-case sans, `fg-subtle`: Policy, Harness, Model, Env, Stage, CPU, Cost, Age, Region, Held.
- Values are mono in `fg-muted`. Use `af-meta__item--strong` (`fg`) for the one value that matters most.
- Only a policy or approval value may take a status color: `af-meta__item--approval` or `af-meta__item--failed`.
- Order items from most identifying to least. Keep to five per line; let the rest wrap.
- For an inspector or detail pane, use `af-kv` (a key/value grid) instead.
- The middle dot exists in one place only: the sub-label of `af-lbl` (`Fleet · us-east4`).

## Readouts

- Use a readout for the one to four numbers a view is about: sandboxes this week, held for a human, spend today, turn to PR.
- Build it as digits on unlit cells inside a recessed window: `af-window` (`display-window`) holding `af-readout` with `--l`, `--m` or `--s`. Each digit or letter is a `<b>` on a `readout-cell`; punctuation is `<b class="af-readout__p">`.
- Put the unit and caption outside the cells: the unit in `body` `fg-subtle` beside it ("of 40 sandboxes"), the caption in `label` below it.
- Never use readout cells in tables, inline data or running text.

## Traces

TraceSpans draws one turn's spans on a shared time axis.

- Rows are `span-h`, indented 16px per depth, with the span name, its kind in `mono-s` `fg-subtle`, and its duration right-aligned in `data`.
- Model calls are solid `span-model`. Tool calls are a 1px `span-tool` outline with a faint fill. Sandbox commands are solid `span-sandbox`.
- Waiting on a human is hatched `status-approval` with an open end while it waits.
- A failed span is a hollow 1.5px `status-failed` outline with a triangle at its end; never a solid red bar and never a tint. Its duration turns `status-failed`; a waiting span's turns `status-approval`.
- Draw the critical path as one 1.5px `brand-text` line through the spans that set the turn's duration. It is the only yellow in the trace; the selected row is `selected` with a 2px `fg` edge.
- Label the axis in 10px mono `fg-subtle` (`0s` … `60s`) on a `line` rule; gridlines are `line-subtle`. Selecting a span opens its detail beside the trace: keyed data and the command output on `terminal-bg`.

## Lanes

SessionLanes draws one lane per session over the last hour.

- Each lane is `lane-h`, labelled with the tail number in mono and harness and model in `fg-subtle`.
- Stages are fills on a greyscale ramp: `stage-plan`, `stage-edit`, `stage-test` (the ramp runs toward `fg` as work advances, in both themes). PR is a 1px outline in `fg-muted`; a merged PR ends in a check in a ring. Queued time is a dashed `status-queued` outline.
- Waiting on a human is hatched `status-approval`. A failure ends the lane with a `status-failed` triangle; a denial with a small `status-denied` placard.
- The now line is a 1px `brand-text` rule at the right edge with a square cap, and the axis runs `-60 min` to `now` (the `now` tick in `brand-text`).
- A selected lane takes `selected` and a 2px `fg` edge on its label.

## Fleet board

FleetView shows every sandbox in a fleet as a stand (tile), grouped by pool, and switches between the board and lanes with two `aria-pressed` buttons.

- Each pool header shows the pool name, keyed counts (`Running 16  Waiting 1  Queued 3`) and capacity (`22 of 24 slots`). The fleet header carries the pool schedule.
- A stand is tonal: a faint `fg` tint on `raised`, no border, `radius-control`, `space-4` from its neighbours. It shows the short code (`7Q2K`), its status mark, four stage pips (plan, edit, test, PR, on the `rail` tokens) and nothing else.
- Running and queued stands stay grey. Needs approval, failed and denied stands keep the same neutral ground and take a 3px status edge on their leading side; their current pip lights in the status color too. Off stands are a 1px `line` outline with no fill; free slots a dashed `line` outline.
- A selected stand takes a 1px `fg` outline offset 2px (focus adds the 2px `focus` ring), and the inspector line under the board shows its keyed data and actions.
- Where there is room for words, the fleet is the runway: AgentRow (rows) and AgentCard (board cards) over the same model, with StageRail for progress and DecisionDeck for what needs a person. FleetConsole composes them. hangar's Fleet keeps List and Board as its two views, with Owners as a filter.
- Progress is a claim: fill a rail, ring or capsule solid only for a pct the agent reported. An estimate (elapsed time against the stage's usual length) is dotted from the stage start with a hollow head (`af-rail--est`), and its label says "about"; with neither, fill to the stage start and stop.

## Diffs

A diff is greyscale, like code. The change is the brightest thing: additions in `fg` with a 2px `fg` bar in the gutter,
deletions in `fg-muted` with a 2px `line-strong` bar, context in `fg-subtle`, the sign column (`+`, `−`) carrying the meaning
without hue, line numbers in mono. The stat is two mono numbers, `+42 −17`, in the same tones. No red, no green, no fills:
a change is work, not a state, and the rule that color appears only when a person is needed holds. The one mark a diff may
carry is the failed triangle in the header of the hunk a failing test points at, with the test in the words (`test 38 of 41
points here`). Line comments route to the agent and say so. See the Diff component.

## Objects by reference

A business object from another system (a ticket, a pull request, an account) is a chip: source glyph, mono key, title, state
word, on a `surface` tile with a hairline. Its title and state are a cache with a timestamp, never the record, so the chip
shows source, freshness and provenance on hover. A chip the viewer may not open shows the key alone with the word
`restricted`. The approval diamond is the only color a chip may carry. See the ObjectChip component.

## Charts

- Draw charts in greyscale: `chart-1` (primary, `fg`-strength), `chart-2`, `chart-3`, `chart-4`, with `chart-6` for grid emphasis.
- Spend at most one attention series per chart, in `chart-5`. It shares the caution orange on purpose: it means "look here".
- Yellow appears in a chart only as the now line or now point, or a target or limit marker.
- Never use product hues or status colors as series. Errors are `status-failed` markers or outlines, never fills.
- Use single-hue greyscale for sequential scales and heatmaps; never red-to-green.
- Draw axes in `rule`, gridlines in `line-subtle`, tick labels in 10px mono `fg-subtle`. Label series directly where possible instead of a legend.
- Draw sparklines as a thin `fg-muted` line over a `line` baseline, ending in a `brand` dot on the latest value (the now point). In a list of agents (`af-spark--mini`) the end dot is `fg`: sixty yellow points would say sixty things are yours. Gauges are a `line` track with an `fg-muted` fill and a `brand-text` bug at the limit.
- One gauge on its own marks its limit with a `brand-text` bug. In a list or in a console opened from a row (`af-gauge--mini`), the bug is `fg-muted`, for the same reason as the list sparkline: one yellow tick per row would say every row is yours.

## Tabular figures

Every number that can sit above another uses tabular figures: `font-variant-numeric: tabular-nums`. The `data` style, `af-num`, `af-mono`, `af-meta__val` and `af-readout` already set it. Right-align numeric columns and keep decimals consistent within a column.
