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
- Survive forced colors (Windows Contrast Themes). The browser replaces colors there, so marks paint in `CanvasText`, lit edges and tonal tiles become outlines and selection uses `Highlight`; the shape and the word carry the status. Never set `forced-color-adjust: none` on a status.
- Light the master lamps from the same rule. MasterCaution shows `lamp-caution` when anything in its scope needs approval and `lamp-warning` when anything failed or was denied; when both apply, warning sits first. With nothing to say it stays dark (`af-master--clear`).

## Grouping: a group leads with what needs a person

A pool, environment, job, experiment or page header shows the status of the child that most needs attention, and
lists its children, columns and keyed counts in the same order:

1. **approval**: a person is needed now
2. **failed**: something broke and someone should look
3. **denied**: policy stopped it; already decided, kept on record
4. **running**
5. **queued**
6. **off**

A held request leads a denied one because the held one is work and the denied one is a record. (MasterCaution is the
exception: its two lamps follow the cockpit convention, warning before caution.)

- A pool with 16 running sandboxes and one waiting on approval shows **Needs approval**.
- A group that is all queued shows **Queued**; a group with any running child shows **Running**. A group is off only when every child is off.
- Pair the group mark with keyed counts so nothing is hidden: `WAITING 1  RUNNING 16  QUEUED 3`. Write zero counts as `0`; drop a count only when the role cannot occur in that scope.
- A lit group mark is a pointer, not a summary. Clicking it takes the person to the child that lit it.

## Examples by product

Keep the role; specialize the word only when it says more. The shape and color never change.

- **hangar.** `HGR-7Q2K` Running a turn. `HGR-5JD2` Queued for a slot in base-codex. `HGR-3MX9` Holding at PR (approval role): push to main held by `require-approval-main-push`. `HGR-0PZ4` Failed at test. `HGR-9KD4` Denied: egress blocked by policy. `HGR-1WQ8` Spun down (off role) when the pool went down at 01:00.
- **flightdeck.** `FDK-EXP-0142` Running, evaluating 9 behavior checks. Queued for a runner. Needs approval: promotion waits for an approver who is not the author. Failed: a behavior check failed or the run crashed. Denied: the author tried to approve their own promotion. Archived (off role).
- **Tower.** Active (running role): passport in force. Queued: request awaiting evaluation. `TWR-APR-0391` Needs approval. Failed: the decision point could not evaluate. Denied by `deny-secrets-egress`, no receipt issued. Expired (off role): passport lapsed. Every decided request links its receipt, `TWR-RCPT-88A1`.
- **ai-dlc.** The CLI prints the same shapes as glyphs: `●` running, `○` queued, `◆` needs approval, `▲` failed, `[DENIED]`, `·` off. The glyph carries the meaning without color; color only the lit three (`◆` orange, `▲` and `[DENIED]` red).
- **Spaceport.** Refreshing (running role). Queued. Needs approval: a schema change waits for the owner. Failed: the refresh failed. Denied: access request refused. Deprecated (off role).

Write the reason next to every lit status as keyed inline data: `POLICY require-approval-main-push`, `STAGE test`, `HELD 41 min`.

## A question is not an approval, but it is the same role

An agent that stops to ask ("Which database should the migration target?") needs a person as much as a held push does, so a
question takes the approval role: the orange diamond, the lit card, the place at the top of the queue. The word tells them
apart: **Needs approval** for a yes or no on an action, **Needs input** for a question with options or free text. Never a
new shape or a new color for questions; the sixth status is still `off`. See the ApprovalCard and Question components.

## Waiting on others stays grey

A request that needs more signatures than it has, where this person has signed or cannot sign, is **Waiting on others**: the
queued role (a grey ring) with words that say how many, `Waiting on 2 others`, and a quorum strip that says whose signature
is in. It is not orange, because nobody *here* is needed; the card is not lit and has no primary action. The moment it
becomes this person's turn it is an approval again. The same goes for a question addressed to someone else.

## Alert inhibition

Airbus inhibits alerts during takeoff and landing so a crew mid-task is not interrupted by anything that can wait. Airframe
inhibits them during a decision: while a dialog or a drawer is open, or a text field has focus (a deny reason, a steer, an
answer), non-critical notices are held and shown afterwards, in order. A notice about the thing the person is doing, or
about a connection that dropped, is critical and shows at once. MasterCaution is not inhibited; it is the summary the held
notices roll up into. The Toast component and `airframe.js` implement the rule; a product that writes its own notices follows it.

## Sources

Two references shaped these rules and say the same things in their own words. Carbon's status indicator pattern asks for
at least two of color, shape and symbol, 3:1 contrast on the mark, the highest-attention status for a group, and no more
than five or six indicators ([carbondesignsystem.com/patterns/status-indicator-pattern](https://www.carbondesignsystem.com/patterns/status-indicator-pattern)).
The Airbus ECAM color code maps onto the dark cockpit one to one: red for immediate action (failed, denied), amber for
awareness and possible action (needs approval), white for titles and labels, and blue for "an action or selection still to
be carried out", which is what the brand yellow means here; ECAM also clears an action line once the state is reached and
inhibits alerts by flight phase ([ECAM guide](https://flyawaysimulation.com/ask/answers/airbus-a320-ecam-how-to-use/),
[Airbus on alert inhibition](https://www2023.icao.int/ESAF/Documents/meetings/2017/AFI%20FOSAS%202017/Day%201%20Docs/Day_1_2_Airbuspihlo.pdf)).
