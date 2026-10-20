# ActivityTimeline

What an agent has done so far, as a vertical list: the wall-clock time and how long ago, then the event; stage boundaries in `fg`, holds and questions with the approval dot, failures with the failed dot, and the latest dot lit with a soft glow so the eye finds now.

## What you provide

- A head: the facts so far (files, commits, tests, tokens, spend) and a token sparkline for the last hour.
- The events, oldest first: a wall-clock time, how long ago, a kind (start, stage, files, commit, test, pr, hold, ask, fail, deny, off, ok) and one sentence.

## Markup

```html
<div class="af-timeline__head">
  <h4>Activity</h4>
  <span class="af-facts"><span>8 files</span><span>4 commits</span><span>202 tests</span><span>48.6k tok</span><span>$0.62</span></span>
  <svg class="af-spark af-spark--mini" …>…</svg><span class="af-note">tokens, last hour</span>
</div>
<ol class="af-timeline">
  <li class="af-timeline__ev af-timeline__ev--start"><i class="af-timeline__dot"></i><time class="af-timeline__time">13:34<small>57 min ago</small></time><span class="af-timeline__text">Sandbox started in base-codex</span></li>
  <li class="af-timeline__ev af-timeline__ev--stage"><i class="af-timeline__dot"></i><time class="af-timeline__time">13:41<small>50 min ago</small></time><span class="af-timeline__text">Plan done in 7 min</span></li>
  <li class="af-timeline__ev af-timeline__ev--hold is-last"><i class="af-timeline__dot"></i><time class="af-timeline__time">13:51<small>41 min ago</small></time><span class="af-timeline__text">git push origin main held by require-approval-main-push</span></li>
</ol>
```

| Part | Class | Notes |
|---|---|---|
| Head | `af-timeline__head` | A row: the word, `af-facts`, a mini sparkline pushed right, its note. |
| List | `af-timeline` | An `ol` with a 1 px `line-subtle` spine; scrolls past 420 px. Set `--ground` to the surface it sits on (`raised`; `lifted` inside an opened console) so the dots cut the spine cleanly. |
| Event | `af-timeline__ev` | A grid: `__dot`, `__time` (mono; the `small` is how long ago), `__text`. |
| Kinds | `--stage`, `--hold`, `--ask`, `--fail`, `--deny` | Stage boundaries are `fg` at 500 with an `fg-muted` dot; hold and ask take the approval dot and `fg` text; fail and deny the failed dot. Anything else is grey. |
| Latest | `is-last` | An `fg` dot with the `rail-glow` while the agent is moving; a latest hold, question or stop keeps its status dot and does not glow. |

## When to use

The history panel of an opened AgentRow or AgentCard, and a sandbox or job page's "so far". It is the most legible answer to "what has it done"; the compact facts row stays in the row itself.

## Do

- Keep the sentences short and specific: "pytest: 202 passed", "Opened PR #210 on acme/checkout-api".
- Show both times: the clock for the record, the relative time for the glance.
- Append new events at the end and move `is-last`; do not re-sort.

## Don't

- Don't color a stage dot or a commit: only a hold, a question, a failure or a denial carries color.
- Don't put a status word in the list; the event text says what happened.
