# How to draw work over time

A trace is one turn's spans; lanes are every session over the last hour. Both share one vocabulary.

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

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
