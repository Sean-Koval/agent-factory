# How to lay out a table

## Tables

- Put a table in `af-table-wrap` (`raised`, no border, scrolls sideways when narrow). Never box a table again inside a card.
- Headers have no fill: `label-s` (sentence-case sans) in `fg-subtle`, left-aligned (right-aligned over numbers), with a 1px `line` rule beneath.
- Divide rows with `line-subtle`. No zebra stripes, no vertical rules. Hover is a faint `fg` tint; the selected row (`aria-selected="true"`) takes `selected` and a 2px `fg` edge on its first cell.
- Lead with the tail number. A hangar fleet table reads: ID, environment, harness and model, status, CPU, age, cost.
- Right-align numbers with `af-num` and tabular figures. Truncate descriptions with an ellipsis; never truncate an ID or a number.
- A row that needs a person (`is-attention`) takes a 3px `status-approval` edge on its first cell; nothing in a table is tinted. Failed and denied rows show their status mark and word only. A selected lit row keeps the status edge and says "selected" with its fill.
- Draw in-cell bars (CPU, budget) as 2px hairlines: `fg-muted` fill on a `line` track, never a status color.

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
