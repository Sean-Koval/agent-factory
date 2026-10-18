A composer is the input a person steers an agent with: a text field on a recessed well, suggestion chips, one send button, a queued row for a message that waits for the agent's current tool call to end (with a take-back), and a disabled state that says why.

## You provide
- A textarea (`af-composer__input`, sans 14 px, grows with its content) with a placeholder that names the act: "Steer the agent", "Reply", "Ask Breaks".
- Up to four suggestion chips (`af-chip af-chip--sm`) that fill the field when pressed; one primary send button, `af-btn--primary af-btn--sm`, with the arrow icon.
- While the agent is busy: a queued row above the box, an `af-lbl` reading `Queued · applies after this tool call`, the queued message in full, and an icon-only ghost button to take it back. A `why` line under the box with the queued ring: "The agent is busy; your message will queue and apply after this tool call."
- When sending is impossible: `is-disabled` on the composer, `disabled` on the field, chips and button, and a `why` line that says what happened and what would enable it: "The sandbox spun down at 01:00 with the pool. Start it to send; the conversation is kept."

## Markup
```html
<div class="af-composer">
  <div class="af-composer__queued">
    <span class="af-lbl">Queued<span class="af-lbl__sub">applies after this tool call</span></span>
    <span class="af-composer__qmsg">Use the legacy table and keep the old index.</span>
    <button type="button" class="af-btn af-btn--ghost af-btn--sm af-btn--icon" aria-label="Take back the queued message"><svg class="af-ic" …>close</svg></button>
  </div>
  <div class="af-composer__box">
    <textarea class="af-composer__input" rows="1" placeholder="Steer the agent" aria-label="Message to the agent"></textarea>
    <div class="af-composer__row">
      <div class="af-composer__chips" role="group" aria-label="Suggestions">
        <button type="button" class="af-chip af-chip--sm">Run the tests first</button>
        <button type="button" class="af-chip af-chip--sm">Open a draft PR</button>
      </div>
      <button type="button" class="af-btn af-btn--primary af-btn--sm af-composer__send"><svg class="af-ic" …>arrow-right</svg>Send</button>
    </div>
  </div>
  <p class="af-composer__why"><span class="af-status af-status--queued"><i class="af-status__mark"></i></span>The agent is busy; your message will queue and apply after this tool call.</p>
</div>

<div class="af-composer is-disabled">
  <div class="af-composer__box">…field, chips and send with disabled…</div>
  <p class="af-composer__why">The sandbox spun down at 01:00 with the pool. Start it to send; the conversation is kept.</p>
</div>
```

| State | What shows |
|---|---|
| Idle agent | The box alone. Send applies at once. |
| Busy agent | The box, a `why` line with the queued ring; after sending, the queued row with the message and a take-back. |
| Disabled | `is-disabled`, controls disabled, a `why` line with the cause and the remedy. Never a disabled control without a reason. |

The box takes the focus ring as a whole (`:focus-within`), like an input. Inside a Diff thread the box sits on `raised`; elsewhere on `surface`.

## When to use
- Steering a running session (hangar sessions, Tower runs), replying in a Diff comment thread, asking an agent from a Tower desk or space.
- Not for an answer to a Question card, which has its own field, and not for a search box.

## Do
- Let the person type while the agent runs. Queue the message, show it queued, and let them take it back until it applies.
- Say when a queued message applies ("after this tool call", "when the turn ends"), in the agent's terms.
- Keep one send button and at most four suggestions; suggestions are the agent's or the product's, in sentence case.
- Hold non-critical toasts while the field has focus (airframe.js does this), and show them after.

## Don't
- Don't disable Send while the agent runs without a queue; the person loses the thought.
- Don't put a status color on the composer. Busy is the grey ring and words; a failed send is a toast with the failed mark.
- Don't animate a "thinking" indicator in the box. The session's status says what the agent is doing.
