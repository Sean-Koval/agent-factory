# Heartbeat

A recency dot and the time since an agent last did something, beside its now-line: it breathes only for a live agent, shows the wait in orange for one that is waiting on a person, and is still for everything else.

## What you provide

- The seconds since the agent's last activity, formatted (`12 s`, `41 min`, `2.5 h`); refresh the text in place every few seconds.
- Whether the agent is live (running) or waiting on a person.

## Markup

```html
<span class="af-hb af-hb--live" title="Last activity 12 s ago"><i class="af-hb__dot"></i>12 s</span>   <!-- running -->
<span class="af-hb af-hb--wait" title="Held 41 min"><i class="af-hb__dot"></i>41 min</span>             <!-- waiting on a person -->
<span class="af-hb"><i class="af-hb__dot"></i>2.5 h</span>                                               <!-- queued, stopped, spun down -->
```

| Part | Class | Notes |
|---|---|---|
| Heartbeat | `af-hb` | Mono 11 px, tabular, `fg-subtle`; a 6 px dot in `fg-dim`. |
| Live | `af-hb--live` | The dot is `status-running` and breathes (opacity 1 → .35 → 1 over 2.4 s). Under `prefers-reduced-motion` it is still. |
| Waiting | `af-hb--wait` | Dot and number in `status-approval`; no motion. The agent is not moving: a person is the reason. |

## When to use

In an AgentRow's sub-line and an AgentCard's foot, and at the head of an opened console's now panel. Anywhere the question is "is this agent alive right now", as opposed to "what state is it in" (that is the Status component).

## Do

- Pair it with the now-line ("running pytest, 191 passed · 12 s"), so the number has a subject.
- Update the number in place; never re-render the row for a tick.
- Let it be the one thing that moves in a quiet view. Waiting agents do not move, which is the point.

## Don't

- Don't use it as a status. A heartbeat is recency; Running, Failed and Needs approval are the six statuses with their marks.
- Don't make the dot pulse for a failed or queued agent, and never color it red.
- Don't animate it under reduced motion (base.css already stops it; do not override).
