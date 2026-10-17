# Status

Airframe has six statuses and no others. Every status is color + shape + word, so it survives greyscale, color blindness and a glance.

| Role | Meaning | Token | Shape | Label | Class |
|---|---|---|---|---|---|
| running | Engaged and healthy. Work is happening; nobody is needed. | `status-running` | Filled circle | Running | `af-status--running` |
| queued | Armed, waiting to start. | `status-queued` | Hollow ring | Queued | `af-status--queued` |
| approval | Needs a human: an approval or decision gate is holding the work. | `status-approval` | Diamond | Needs approval | `af-status--approval` |
| failed | Stopped on an error: a test, a build, a crash. | `status-failed` | Triangle | Failed | `af-status--failed` |
| denied | Hard stop by policy. Nothing a retry will fix. | `status-denied` + `on-status-denied` | Placard: capitals on a red fill | Denied | `af-status--denied` |
| off | Spun down, expired, archived. | `status-off` | Small dot | Off, Spun down, Expired | `af-status--off` |

```html
<span class="af-status af-status--running"><i class="af-status__mark"></i>Running</span>
<span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span>
<span class="af-status af-status--denied"><i class="af-status__mark"></i>Denied</span>
```

## The dark-cockpit rule

- Keep normal quiet. Running is grey (`status-running`), queued is a grey ring. Neither ever takes a hue; there is no green.
- Spend color only on needs approval (orange), failed (red) and denied (red placard). A view with no color on it is a view where nobody is needed.
- Set the status word in `fg` by default. Add `af-status--lit` to color the word too, only where the status is the subject: an alert, an inspector header, a master caution line.
- Never put a pill or background behind a status word. The one fill is the denied placard.
- Never animate a status. No pulse, no blink, no spinner on running.
- Never use `brand` or a product hue for a status, and never a status color for anything that is not a status. The one exception is `chart-5`, the attention series, which borrows the caution orange to mean "look here".
- Keep failed and denied apart by shape, not hue: failed is a triangle with a word, denied is a placard.
- Light the master lamps from the same rule. MasterCaution shows `lamp-caution` when anything in its scope needs approval and `lamp-warning` when anything failed or was denied; when both apply, warning sits first. With nothing to say it stays dark (`af-master--clear`).

## Grouping: a group shows its most severe child

A pool, environment, job, experiment or page header shows the status of its most severe child, in this order:

1. **denied**
2. **failed**
3. **approval**
4. **running**
5. **queued**
6. **off**

- A pool with 16 running sandboxes and one waiting on approval shows **Needs approval**.
- A group that is all queued shows **Queued**; a group with any running child shows **Running**. A group is off only when every child is off.
- Pair the group mark with keyed counts so nothing is hidden: `RUNNING 16  WAITING 1  QUEUED 3`. Write zero counts as `0`; drop a count only when the role cannot occur in that scope.
- A lit group mark is a pointer, not a summary. Clicking it takes the person to the child that lit it.

## Examples by product

Keep the role; specialize the word only when it says more. The shape and color never change.

- **hangar.** `HGR-7Q2K` Running a turn. `HGR-5JD2` Queued for a slot in base-codex. `HGR-3MX9` Holding at PR (approval role): push to main held by `require-approval-main-push`. `HGR-0PZ4` Failed at test. `HGR-9KD4` Denied: egress blocked by policy. `HGR-1WQ8` Spun down (off role) when the pool went down at 01:00.
- **flightdeck.** `FDK-EXP-0142` Running, evaluating 9 behavior checks. Queued for a runner. Needs approval: promotion waits for an approver who is not the author. Failed: a behavior check failed or the run crashed. Denied: the author tried to approve their own promotion. Archived (off role).
- **Tower.** Active (running role): passport in force. Queued: request awaiting evaluation. `WS-APR-0391` Needs approval. Failed: the decision point could not evaluate. Denied by `deny-secrets-egress`, no receipt issued. Expired (off role): passport lapsed. Every decided request links its receipt, `WS-RCPT-88A1`.
- **ai-dlc.** The CLI prints the same shapes as glyphs: `●` running, `○` queued, `◆` needs approval, `▲` failed, `[DENIED]`, `·` off. The glyph carries the meaning without color; color only the lit three (`◆` orange, `▲` and `[DENIED]` red).
- **Spaceport.** Refreshing (running role). Queued. Needs approval: a schema change waits for the owner. Failed: the refresh failed. Denied: access request refused. Deprecated (off role).

Write the reason next to every lit status as keyed inline data: `POLICY require-approval-main-push`, `STAGE test`, `HELD 41 min`.
