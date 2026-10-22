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

## Where each rule lives

Each page answers one question.

- <span id="the-dark-cockpit-rule"></span><span id="accepted-bends"></span>**[When a status takes color](Cockpit.md)**: the dark-cockpit rule, forced colors, the master lamps, and the three accepted bends.
- <span id="attention-is-edge-mark-word-theme-v12"></span>**[How a thing shows it needs a person](Attention.md)**: edge, mark, word on cards, rows, tiles and decisions, with the measured contrast.
- <span id="grouping-a-group-leads-with-what-needs-a-person"></span>**[Which status a group shows](Grouping.md)**: the attention-first order and keyed counts.
- <span id="examples-by-product"></span>**[What each product calls its statuses](Examples.md)**: the words hangar, flightdeck, Tower, ai-dlc and Spaceport use for each role.
- <span id="a-question-is-not-an-approval-but-it-is-the-same-role"></span><span id="decision-words"></span><span id="waiting-on-others-stays-grey"></span><span id="alert-inhibition"></span>**[Which words a decision uses](Decisions.md)**: Needs approval and Needs input, Approve and Deny, waiting on others, and alert inhibition.

## Sources

Two references shaped these rules and say the same things in their own words. Carbon's status indicator pattern asks for
at least two of color, shape and symbol, 3:1 contrast on the mark, the highest-attention status for a group, and no more
than five or six indicators ([carbondesignsystem.com/patterns/status-indicator-pattern](https://www.carbondesignsystem.com/patterns/status-indicator-pattern)).
The Airbus ECAM color code maps onto the dark cockpit one to one: red for immediate action (failed, denied), amber for
awareness and possible action (needs approval), white for titles and labels, and blue for "an action or selection still to
be carried out", which is what the brand yellow means here; ECAM also clears an action line once the state is reached and
inhibits alerts by flight phase ([ECAM guide](https://flyawaysimulation.com/ask/answers/airbus-a320-ecam-how-to-use/),
[Airbus on alert inhibition](https://www2023.icao.int/ESAF/Documents/meetings/2017/AFI%20FOSAS%202017/Day%201%20Docs/Day_1_2_Airbuspihlo.pdf)).

Part of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
