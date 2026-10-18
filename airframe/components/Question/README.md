A question card is an agent asking a person: the question, the context it has, the options it sees as chips plus a free-text field, and one primary action; it uses the approval role (a person is needed) with the word "Needs input", because a question is not an approval.

## You provide
- Who asks (the sandbox tail number and turn) and the status `Needs input` on the approval role.
- The question as one sentence, and one or two sentences of context with the real names in `code`.
- Up to five options as chips (`af-chip`, `aria-pressed`), in the agent's order; `af-chip--mono` for values that are code.
- A free-text field under the options. Free text dismisses the options: once the person types, the chips dim (no script needed, the CSS uses `:has()`), and the answer is the text.
- One primary action, "Answer", and keyed facts: when it was asked and what the agent is doing meanwhile (holding the turn, or working on something else).
- Once answered: a verdict row with a quiet check, the question, the answer and who gave it.

## Markup
```html
<article class="af-card af-card--lit af-question">
  <div class="af-card__top">
    <span class="af-lbl"><svg class="af-ic" …>agent</svg>Question<span class="af-lbl__sub">HGR-3MX9</span><span class="af-lbl__sub">turn 7</span></span>
    <span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>Needs input</span>
  </div>
  <p class="af-question__q">Which database should the migration target?</p>
  <p class="af-question__ctx">The repo has two: <code>orders</code> (Postgres 15) and <code>orders_legacy</code> (Postgres 12). …</p>
  <div class="af-question__opts" role="group" aria-label="Options">
    <button type="button" class="af-chip af-chip--mono" aria-pressed="true">orders</button>
    <button type="button" class="af-chip af-chip--mono" aria-pressed="false">orders_legacy</button>
    <button type="button" class="af-chip" aria-pressed="false">Stop and ask the ticket owner</button>
  </div>
  <label class="af-field af-question__free">
    <span class="af-field__label">Or answer in your own words</span>
    <span class="af-input af-input--area af-input--sans"><textarea rows="2" placeholder="Free text dismisses the options"></textarea></span>
  </label>
  <div class="af-question__act">
    <span class="af-meta">…ASKED 6 min ago · WHILE holding the turn…</span>
    <button type="button" class="af-btn af-btn--primary af-btn--sm">Answer</button>
  </div>
</article>

<div class="af-verdict">
  <span class="af-verdict__ok"><svg class="af-ic" …>check</svg>Answered</span>
  <span class="af-verdict__body"><span class="af-verdict__cmd">Which database should the migration target?</span><span class="af-verdict__why">orders. By Sean, as the agent's next message.</span></span>
  <span class="af-verdict__time">14:18:22</span>
</div>
```

| Part | Class | Notes |
|---|---|---|
| Question | `af-question__q` | 17/600 Red Hat Text, balanced. |
| Context | `af-question__ctx` | 13.5 px `fg-muted`; names in `code` take mono and `fg`. |
| Options | `af-question__opts` > `af-chip` | Pressed inverts, like a segment. Dimmed and dashed once the free text has content. |
| Free text | `af-question__free` | An `af-field` with `af-input af-input--area af-input--sans`. |
| Action | `af-question__act` | Keyed facts left, the one primary right. |

## When to use
- A session or job where the agent stopped to ask (Devin's `waiting_for_user`, Linear's `elicitation`, LangGraph's `respond`): hangar's sessions page, a Tower run, a chat card.
- Not for a yes or no on a held action; that is an ApprovalCard. Not for a free-form steer while the agent runs; that is a Composer.

## Do
- Keep the same diamond as an approval: both mean a person is needed now. The word tells them apart.
- Show the agent's options in its own words and let the person override them with text; say that the text wins.
- Say what the agent does while it waits, and put the answer on the run's record.
- Light the card only for the person who can answer; a question for someone else is "Waiting on others" (see ApprovalCard).

## Don't
- Don't invent options the agent did not offer, and don't offer more than five; the free text covers the rest.
- Don't make the answer a modal. The question sits in the run where it was asked.
- Don't turn an answered question green; it becomes a quiet verdict row.
