The fleet table lists sandboxes in dense 32 px rows on a tonal panel: tail number, environment, harness and model, status, a CPU micro-bar, age and cost, with an unfilled header, an attention tint for rows that need a person, and a brand edge on the selected row.

## You provide
- Rows of sandboxes: tail number, environment, harness, model, status, CPU (or — when not running), age as `hh:mm:ss`, cost.
- Which row needs a person (`is-attention`) and which is selected (`is-selected`; or `aria-selected="true"` when the table is an interactive `role="grid"`).
- A foot: what is shown on the left (keyed), selection and totals on the right.

## Markup
```html
<div class="af-table-wrap">
  <table class="af-table" style="min-width:760px">
    <thead><tr><th scope="col">Sandbox</th><th scope="col">Environment</th><th scope="col">Harness · model</th><th scope="col">Status</th>
      <th scope="col" class="af-num">CPU</th><th scope="col" class="af-num">Age</th><th scope="col" class="af-num">Cost</th></tr></thead>
    <tbody>
      <tr class="is-attention">
        <td class="af-table__id">HGR-3MX9</td>
        <td class="af-table__mono">base-codex</td>
        <td>codex<span class="af-table__sub">gpt-5.1</span></td>
        <td><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></td>
        <td class="af-num"><span class="af-cpu"><span class="af-cpu__bar"><b style="width:4%"></b></span><span class="af-table__mono af-cpu__val">4%</span></span></td>
        <td class="af-num af-table__mono">00:41:07</td>
        <td class="af-num af-table__mono">$1.18</td>
      </tr>
      <tr class="is-selected">…</tr>
    </tbody>
  </table>
  <div class="af-table__foot"><span class="af-meta">…showing, region…</span><span class="af-meta">…selected, today…</span></div>
</div>
```

| Part | Class |
|---|---|
| Wrapper (raised, scrolls sideways) | `af-table-wrap` |
| Tail number cell | `af-table__id` (mono 500, `fg`) |
| Mono data cell | `af-table__mono` (12.5 px, `fg-muted`, tabular) |
| Secondary text after a value | `af-table__sub` (`fg-subtle`, 8 px gap) |
| Numeric column | `af-num` on `th` and `td` |
| CPU micro-bar | `af-cpu` › `af-cpu__bar` › `<b style="width:N%">` + `af-cpu__val` |
| Attention row | `tr.is-attention` (7% `status-approval` tint) |
| Selected row | `tr.is-selected` or `tr[aria-selected="true"]` (`selected` ground, 2 px `brand-text` edge) |
| Compact (28 px) | `af-table--compact` |

## Do
- Right-align every number and set it in mono with tabular figures.
- Keep the header unfilled: `fg-subtle` mono capitals on a `line` rule.
- Tint only the rows that need a person. Failed and denied rows carry their status mark, not a tint.

## Don't
- Don't zebra-stripe, fill the header, or draw vertical rules.
- Don't put buttons in every row; act on the selected row from the inspector or the header.
- Don't let the table squeeze columns below their content; set a `min-width` and let the wrapper scroll.
