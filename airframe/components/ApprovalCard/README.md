An approval card shows one held action waiting on a reviewer: the exact command, the Cedar policy that held it, the checks that passed, when it expires, the Deny / Approve decision and the receipt it will file; a verdict row records a decided or denied action on one line.

## You provide
- The approval ID (`WS-APR-0391`) and the held command in mono (`git push origin main`), with keyed facts about it (repo, from, files, diff).
- Who asked (the sandbox tail number) and for whom.
- The policy name and, optionally, its Cedar source in an `af-code` block.
- Checks as a list with check icons, an expiry in plain words, the reviewer, and the receipt ID the decision will file.
- For a verdict row: the outcome (denied placard), the action, keyed policy / sandbox / receipt, and a time.

## Markup
```html
<article class="af-card af-card--lit af-approval">
  <div class="af-card__top">
    <span class="af-lbl"><svg class="af-ic" …>approval</svg>Approval<span class="af-lbl__sub">WS-APR-0391</span></span>
    <span class="af-status af-status--approval af-status--lit"><i class="af-status__mark"></i>Needs approval</span>
  </div>
  <div class="af-approval__subject">
    <p class="af-approval__cmd">git push origin main</p>
    <span class="af-meta">…repo, from, files, diff…</span>
  </div>
  <dl class="af-kv">
    <dt>Requested by</dt><dd><span class="af-id">HGR-3MX9</span> <span class="af-muted">for sean, 41 min ago</span></dd>
    <dt>Policy</dt><dd><span class="af-mono">require-approval-main-push</span> <span class="af-tag">cedar</span>
      <pre class="af-code"><span class="af-code__k">forbid</span> (principal, action == Action::<span class="af-code__s">"git:push"</span>, resource) …</pre></dd>
    <dt>Checks</dt><dd><ul class="af-checks"><li><svg class="af-ic" …>check</svg>tests 212 of 212</li>…</ul></dd>
    <dt>Expires</dt><dd>in <span class="af-mono">54 min</span>, then the push is dropped</dd>
  </dl>
  <div class="af-approval__act">
    <span class="af-meta"><span class="af-meta__item"><span class="af-meta__key">reviewer</span><span class="af-meta__val">platform-oncall</span></span></span>
    <div class="af-approval__btns">
      <button type="button" class="af-btn af-btn--danger af-btn--sm">Deny</button>
      <button type="button" class="af-btn af-btn--primary af-btn--sm">Approve push</button>
    </div>
  </div>
  <div class="af-card__foot"><span class="af-receipt"><svg class="af-ic" …>receipt</svg>Your decision is filed as receipt <b>WS-RCPT-88A1</b></span></div>
</article>

<div class="af-verdict">
  <span class="af-status af-status--denied"><i class="af-status__mark"></i>Denied</span>
  <span class="af-verdict__body">
    <span class="af-verdict__cmd">write secrets/prod.env</span>
    <span class="af-meta"><span class="af-meta__item af-meta__item--failed"><span class="af-meta__key">policy</span><span class="af-meta__val">deny-secret-paths</span></span>…</span>
  </span>
  <span class="af-verdict__time">14:07:40</span>
</div>
```

`af-code` is the theme-following code block (`surface` ground; `af-code__k` keywords in `fg`, `af-code__s` strings in `fg-muted`, `af-code__c` comments in `fg-subtle`). Use the Terminal for command output.

## When to use
- The approvals queue, the approval drawer, and inline in a session when it holds.
- Verdict rows in approval history and in a session's timeline.

## Do
- Show the exact action being approved, not a summary of it.
- Say what happens on expiry. Say where the receipt goes before the decision is made.
- Keep the card lit only while it waits; once decided, it becomes a verdict row.

## Don't
- Don't make Deny a solid red button or Approve a green one.
- Don't hide the policy behind a link when it fits in four lines.
- Don't show more than one held action per card.
