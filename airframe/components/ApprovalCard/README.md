An approval card shows one held action waiting on a reviewer: the exact command, the Cedar policy that held it, the checks that passed, when it expires, the decision (inspect, deny with a reason, approve, approve edited, approve for the session), who else must approve, and the receipt it will file; a verdict row records a decided action on one line.

## You provide
- The approval ID (`TWR-APR-0391`) and the held command in mono (`git push origin main`), with keyed facts about it (repo, from, files, diff).
- Who asked (the agent's avatar and the sandbox tail number) and for whom.
- The policy name and, optionally, its Cedar source in an `af-code` block.
- Checks as a list with check icons, an expiry in plain words, the reviewer, and the receipt ID the decision will file.
- The decision buttons in inspect, refuse, accept order; a second accept ("Approve for this session") only when the policy allows a grant, with a hint that says what the grant covers and how long it lasts.
- For deny: a reason field. **A reason is required when denying and optional when approving.** The field is neutral until Deny is pressed with it empty; only then is it invalid, with the failed mark and words, never a red fill.
- For edit-then-approve: the arguments in an editable mono field, what they were, and the primary reads "Approve edited".
- For a quorum: the approvers as a stacked avatar group (pending ones dashed), "1 of 2 approved", and keyed `approved` / `waiting` facts.
- For a verdict row: the outcome (denied placard, or a quiet check for approved), the action, its reason, keyed policy / sandbox / receipt, and a time.

## Markup
```html
<article class="af-card af-card--lit af-approval">
  <div class="af-card__top">
    <span class="af-lbl"><svg class="af-ic" …>approval</svg>Approval<span class="af-lbl__sub af-mono">TWR-APR-0391</span></span>
    <span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>Needs approval</span>
  </div>
  <div class="af-approval__subject">
    <p class="af-approval__cmd">git push origin main</p>
    <span class="af-meta">…repo, from, files, diff…</span>
  </div>
  <dl class="af-kv">
    <dt>Requested by</dt><dd><span class="af-who"><span class="af-avatar af-avatar--agent af-avatar--22">…</span><span class="af-id">HGR-3MX9</span></span> <span class="af-muted">codex, for Sean, 41 min ago</span></dd>
    <dt>Policy</dt><dd><span class="af-mono">require-approval-main-push</span> <span class="af-tag">cedar</span><pre class="af-code">…</pre></dd>
    <dt>Checks</dt><dd><ul class="af-checks"><li><svg class="af-ic" …>check</svg>tests 212 of 212</li>…</ul></dd>
    <dt>Expires</dt><dd>in <span class="af-mono">54 min</span>, then the push is dropped</dd>
  </dl>
  <div class="af-approval__act">
    <span class="af-meta">…reviewer…</span>
    <div class="af-approval__btns">
      <button type="button" class="af-btn af-btn--ghost af-btn--sm">View diff</button>
      <button type="button" class="af-btn af-btn--danger af-btn--sm">Deny</button>
      <button type="button" class="af-btn af-btn--secondary af-btn--sm">Approve for this session</button>
      <button type="button" class="af-btn af-btn--primary af-btn--sm">Approve push</button>
    </div>
  </div>
  <p class="af-approval__hint"><svg class="af-ic" …>info</svg><span>For this session extends the mandate: … until the session ends, in <b>2 h 10 min</b>, filed as <b>TWR-GRT-0A12</b>.</span></p>
  <div class="af-approval__quorum">
    <span class="af-avatars"><span class="af-avatar af-avatar--person af-avatar--22">PN</span><span class="af-avatar af-avatar--person af-avatar--22 af-avatar--pending">PO</span></span>
    <span class="af-approval__signed"><b>1 of 2</b> approved</span>
    <span class="af-meta">…approved Priya, 14:02 · waiting you…</span>
  </div>
  <div class="af-card__foot"><span class="af-receipt"><svg class="af-ic" …>receipt</svg>Your decision is filed as receipt <b>TWR-RCPT-88A1</b></span></div>
</article>
```

Deny with a reason (shown in place of the action row once Deny is pressed). The field opens neutral, with a hint:

```html
<div class="af-approval__reason" role="group" aria-labelledby="deny-lbl">
  <label class="af-field">
    <span class="af-field__label" id="deny-lbl">Reason for denying (required)</span>
    <span class="af-input af-input--area af-input--sans"><textarea rows="2" required aria-describedby="deny-hint" placeholder="What the requester should change"></textarea></span>
    <span class="af-field__hint" id="deny-hint">It goes on the receipt and back to HGR-4KQ1.</span>
  </label>
  <div class="af-approval__btns">
    <button type="button" class="af-btn af-btn--ghost af-btn--sm">Cancel</button>
    <button type="button" class="af-btn af-btn--danger af-btn--sm">Deny refund</button>
  </div>
</div>
```

Only when Deny is pressed with the field empty does it turn invalid: `is-invalid` on the input (the Controls border),
`aria-invalid="true"` on the textarea, and the hint swapped for the error:

```html
<span class="af-input af-input--area af-input--sans is-invalid"><textarea rows="2" required aria-invalid="true" aria-describedby="deny-err" placeholder="What the requester should change"></textarea></span>
<span class="af-field__error" id="deny-err"><span class="af-status af-status--failed"><i class="af-status__mark"></i>Give a reason. It goes on the receipt and back to HGR-4KQ1.</span></span>
```

Edit, then approve (`af-approval--editing` on the card):

```html
<label class="af-field">
  <span class="af-field__label">Arguments (edited)</span>
  <span class="af-input af-input--area af-approval__edit"><textarea rows="3" aria-label="Arguments">--squash
--delete-branch</textarea></span>
  <span class="af-field__hint">Was <span class="af-mono">--merge --delete-branch</span>. The receipt records both versions.</span>
</label>
… <button type="button" class="af-btn af-btn--primary af-btn--sm">Approve edited</button>
```

Waiting on others (`af-approval--waiting`, no `af-card--lit`): the status is the queued ring with words, `Waiting on 2 others`, the quorum strip says whose approval is in, and the only button is a ghost "Open".

Verdict rows:

```html
<div class="af-verdict">
  <span class="af-status af-status--denied"><i class="af-status__mark"></i>Denied</span>
  <span class="af-verdict__body">
    <span class="af-verdict__cmd">curl -X POST https://api.stripe.com/v1/refunds</span>
    <span class="af-verdict__why">Refund the original charge, not a new one. Reason by Sean.</span>
    <span class="af-meta">…policy, receipt…</span>
  </span>
  <span class="af-verdict__time">14:07:40</span>
</div>
<div class="af-verdict">
  <span class="af-verdict__ok"><svg class="af-ic" …>check</svg>Approved</span>
  …
</div>
```

`af-code` is the theme-following code block (`surface` ground; `af-code__k` keywords in `fg`, `af-code__s` strings in `fg-muted`, `af-code__c` comments in `fg-subtle`). Use the Terminal for command output. `af-approval__hint` is a one-line note with an icon; `af-approval__quorum` sits above the foot.

| State | Status | Card | Primary |
|---|---|---|---|
| Yours to decide | `af-status--approval` `af-status--lit`, Needs approval | `af-card--lit` | Approve … |
| Denying | same | same, `af-approval__reason` open | Deny … (danger; the reason is required) |
| Editing | same | same, `af-approval--editing` | Approve edited |
| Waiting on others | `af-status--queued`, Waiting on 2 others | plain, `af-approval--waiting` | none; a ghost Open |
| Decided | verdict row | `af-verdict` | none |

### In a narrow place

A docked detail panel or a phone gives the card 320 px or less. Nothing is cut: the head (`af-card__top`) wraps, so the
status drops under the label, whole and visible ("Needs approval" never runs past the edge); the label's sub (the ID)
ellipsizes only when the label alone is wider than the head, and a second sub (`editing`) gives way first. The decision
row wraps, and once it has wrapped the buttons share each line so the primary never sits alone at the end of a ragged row;
inspect (the ghost) keeps its size. At full width nothing stretches. No container query or product CSS is needed; the
preview's last card shows it at 320 px.

## When to use
- The approvals queue, the approval drawer, and inline in a session when it holds.
- Verdict rows in approval history and in a session's timeline.
- For a question from an agent (needs input rather than a yes or no), use Question instead.

## Do
- Use the decision words in guide/Status.md: **Needs approval** as the status, **Approve** and **Deny** as the buttons (with the object when it helps), **Denied** on the verdict.
- Show the exact action being approved, not a summary of it; when the person edits it, show what it was.
- Order the decision as inspect (ghost), refuse (danger), accept (primary). Put a second accept, such as approve for the session, as a secondary between them, and say in a hint what it grants and for how long.
- Require a reason to deny and make it optional to approve. Send the reason to the requester and put it on the receipt.
- Say what happens on expiry. Say where the receipt goes before the decision is made.
- Keep the card lit only while it waits on this person. A quorum that is not yet met and not this person's turn is "Waiting on others": grey ring, no lit ring, no primary, because nobody here is needed.
- Once decided, turn the card into a verdict row. Approved is a quiet check and a word: allowed is not green.

## Don't
- Don't label the act Sign, Decline, Reject or Blocked. A receipt may say it was signed; the person approves.
- Don't make Deny a solid red button or Approve a green one. Don't show the reason field invalid before Deny is pressed, and don't fill it red; the failed mark and the words carry the error.
- Don't hide the policy behind a link when it fits in four lines.
- Don't show more than one held action per card.
- Don't light a card orange for a person who cannot decide it.
- Don't fix a narrow card in product CSS (a `max-width` on the head, a container query on the buttons); the card wraps on its own, and a product that needs more proposes it here.
