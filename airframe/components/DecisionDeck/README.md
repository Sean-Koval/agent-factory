# DecisionDeck

What needs you, one decision at a time: the soonest to expire on top as a lifted sheet, the next two peeking behind it, "1 of 5", previous and next, and an up-next list to skip around. Deciding (approve, deny with a required reason, answer with chips or free text, retry or start over, acknowledge) happens inline; the card slides away and the next one rises. When nothing waits, a calm empty state says so and counts what is running.

## What you provide

- The decisions (approval, question), ordered by time left to expiry; they are the stack and the count ("1 of 5" matches the nav badge and "Five waiting on you").
- What stopped (failed, denied), newest first. It is listed under the up-next list as **Stopped**, never mixed into the stack; with no decision left, the stopped ones become the stack. Every item, decision or stopped, has its agent's tail number and work, who runs it for whom, the expiry or age, and its body: the approval's lead, command, facts and buttons; the question's words, context, options and free text; the failure's message, retry and start over; the denial's reason and acknowledge.
- The verdict sentence after a decision ("Approved by Sean. Receipt TWR-RCPT-88A1 filed; codex is pushing.") and when the card may leave.
- The counts for the empty state.

## Markup

```html
<section class="af-deck" aria-label="Needs you">
  <div class="af-deck__stack">
    <article class="af-decision af-decision--approval" data-k="0" data-id="HGR-3MX9" aria-label="HGR-3MX9, Needs approval">
      <div class="af-decision__hd"><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span><span class="af-decision__exp">54 min left</span></div>
      <div class="af-decision__who"><button type="button" class="af-decision__link"><span class="af-id">HGR-3MX9</span>Push the refunds migration to main</button><span class="af-decision__by"><span class="af-avatar af-avatar--agent af-avatar--22">cx</span>codex for Sean</span></div>
      <div class="af-decision__bd">
        <p class="af-lead">codex wants to push to main. Policy <code>require-approval-main-push</code> holds it.</p>
        <pre class="af-cmd">git push origin main</pre>
        <div class="af-pairs"><span><small>Diff</small>+184 −27, 6 files</span><span><small>Checks</small>3 of 3 green</span><span><small>From</small><span class="af-mono">codex/refunds-migration</span></span><span><small>Receipt</small><span class="af-mono">TWR-RCPT-88A1</span></span></div>
        <div class="af-acts"><button class="af-btn af-btn--ghost af-btn--sm">View diff</button><div class="af-acts__end"><button class="af-btn af-btn--danger af-btn--sm">Deny</button><button class="af-btn af-btn--primary af-btn--sm">Approve push</button></div></div>
      </div>
    </article>
    <article class="af-decision af-decision--approval" data-k="1" inert>…</article>
    <article class="af-decision af-decision--approval" data-k="2" inert>…</article>
  </div>
  <aside class="af-deck__side">
    <h2 class="af-deck__title">Needs you<span class="af-deck__count">1 of 5</span></h2>
    <p>One decision at a time, soonest to expire on top. Decide and the next one rises; the agent continues the moment you do.</p>
    <div class="af-deck__nav"><button class="af-btn af-btn--secondary af-btn--sm af-btn--icon" aria-label="Previous">…</button><button class="af-btn af-btn--secondary af-btn--sm af-btn--icon" aria-label="Next">…</button><span class="af-note">Skip for now</span></div>
    <ul class="af-deck__upnext"><li><button type="button"><span class="af-status af-status--approval"><i class="af-status__mark"></i></span><span class="af-id">HGR-7Q2K</span><span class="af-deck__what">Backfill order totals for Q3</span><span class="af-deck__when">1 h 54 min left</span></button></li>…</ul>
    <h3 class="af-deck__subtitle">Stopped</h3>
    <ul class="af-deck__stopped"><li><button type="button"><span class="af-status af-status--failed"><i class="af-status__mark"></i></span><span class="af-id">HGR-0PZ4</span><span class="af-deck__what">Round refunds to the cent</span><span class="af-deck__when">Failed</span></button></li>…</ul>
  </aside>
</section>

<!-- deny: the reason is required; the error is the failed mark and a sentence, never a red fill -->
<div class="af-reason"><label for="r">Reason for denying (required, goes on the receipt and back to HGR-3MX9)</label>
  <div class="af-input af-input--area af-input--sans is-invalid"><textarea id="r" rows="2" aria-invalid="true" placeholder="What the agent should change"></textarea></div>
  <span class="af-field__error"><span class="af-status af-status--failed"><i class="af-status__mark"></i>Give a reason.</span></span>
  <div class="af-acts"><div class="af-acts__end"><button class="af-btn af-btn--ghost af-btn--sm">Cancel</button><button class="af-btn af-btn--danger af-btn--secondary af-btn--sm">Deny push</button></div></div></div>

<!-- after a decision -->
<div class="af-verdict-line"><svg class="af-ic">…check…</svg><span>Approved by Sean. Receipt TWR-RCPT-88A1 filed; codex is pushing.</span><button class="af-btn af-btn--ghost af-btn--sm">Dismiss</button></div>

<!-- empty -->
<div class="af-deck__stack"><div class="af-empty af-empty--compact af-deck__empty">…<h3 class="af-empty__title">Nothing waits on you.</h3><p class="af-empty__text">17 agents running, 3 queued. You will hear when one needs you.</p></div></div>
```

| Part | Class | Notes |
|---|---|---|
| Deck | `af-deck` | Two columns (the stack up to 640 px, the side); one below 1000 px, where the up-next list goes. |
| Stack | `af-deck__stack` | Cards carry `data-k`: 0 is on top (in flow), 1 and 2 peek behind it (12 px down and 3.5% smaller each, inert, with no status edge: only the top card carries it), the rest are hidden. 24 px of bottom padding leaves room for the peek. |
| Decision | `af-decision` | A lifted sheet (`lifted`, `radius-sheet`, `shadow-2`, the `edge-hi` highlight) with the 3 px status edge; `--approval` (also questions), `--failed`, `--denied`; `--done` dims it after the verdict; `is-leaving` slides it out. |
| Head, who, body | `__hd` (status word in its color, `__exp` right), `__who` (`__link` to the agent, `__by`), `__bd` | The body is the decision's own words and controls: `af-lead`, `af-ctx`, `af-cmd`, `af-pairs`, `af-chips`, `af-reason`, `af-acts` with `af-acts__end`. |
| Side | `af-deck__side` | `__title` with `__count`, a sentence, `__nav` (previous, next, "Skip for now"), `__upnext` (mark, id, what, when). |
| Empty | `af-deck__empty` on `af-empty af-empty--compact` | A hairline, no sheet, no color. |

## Behaviour

`deck.next(stack)`, `deck.prev(stack)` and `deck.go(stack, i)` in airframe.js rotate the cards and renumber `data-k`; `deck.leave(card)` plays the exit over `dur-open`, removes the card, lets the next one rise and moves focus to it. Each fires `af:deck` on the stack with `{top, count}`, so the side can repaint "n of N" and the up-next list. A deny reveals `af-reason` and focuses the field; an empty reason is refused with the failed mark and "Give a reason." A question's free text dims the chips (`is-dismissed`). After a verdict, show `af-verdict-line` for a few seconds, then `deck.leave`.

## When to use

hangar's Needs you, and the top of its Fleet; Tower's Desk for a person who clears their queue rather than scanning it. It is the focused layout of the decision queue: for an inbox that stays open on a second screen, lay the same `af-decision` cards out in a column instead of a stack; outside a stack they rest on `shadow-1`.

## Do
- Use the decision words in guide/Status.md: **Needs approval** or **Needs input** on the card, **Approve** and **Deny** as the buttons, **Denied** for what policy stopped.

- Order by what expires first. Count only the decisions, so the deck, the nav badge and the page header agree.
- List what stopped under **Stopped** (`af-deck__subtitle`, `af-deck__stopped`); it stays visible at every width, unlike up-next.
- Mutate the fleet when a decision lands: the agent's row flips to running with a new now-line, the nav count follows.
- Keep the agent's words in the lead: "codex wants to push to main. Policy require-approval-main-push holds it."

## Don't
- Don't label the act Sign, Decline, Reject or Blocked, or a card "Needs your signature".

- Don't fill a button red. Deny is red words; the confirmed deny is red words on a hairline. The one red fill is the denied placard.
- Don't let a card leave before the verdict was readable, and never without the agent having been told.
- Don't tint the sheet. The edge, the diamond and the word say it needs you; the yellow button says what to do.
