# AgentRow

The Runway row: one agent per 58 px line with everything a person asks of it at a glance (what, why, who, how far, cost), opening in place into a console. Mark, tail, the work and a live now-line with its heartbeat, owner, harness and model, the stage rail, the last two stages' times, a token sparkline, cost, a chevron.

## What you provide

- Per agent: tail number, status (running, queued, approval or input, failed, denied, off), the work's title, a one-line now ("running pytest, 191 passed", "waiting on you: push to main"), seconds since the last activity, owner, harness and model, stage and progress, the time spent in each stage so far, tokens per five minutes for the last hour, spend.
- The console for an open row: a decision when one waits (an approval, a question, a failure, a denial), the now panel (heartbeat, now-line, labeled rail, facts, actions) and the ActivityTimeline.
- Pools or environments as groups, with the slots used.

## Markup

```html
<section class="af-runway__group" aria-label="base-codex pool">
  <div class="af-runway__head"><h3><svg class="af-ic">…environment…</svg>base-codex</h3><span class="af-note">15 of 24 slots</span><span class="af-cap af-cap--sm"><span class="af-cap__bar"><i style="width:62%"></i></span></span></div>
  <div class="af-runway" role="group">
    <article class="af-agent af-agent--lit is-open" data-id="HGR-3MX9">
      <button type="button" class="af-agent__line" aria-expanded="true" aria-label="HGR-3MX9, Needs approval, Push the refunds migration to main">
        <span class="af-status af-status--approval" aria-hidden="true"><i class="af-status__mark"></i></span>
        <span class="af-agent__tail">3MX9</span>
        <span class="af-agent__ttl"><span class="af-agent__work">Push the refunds migration to main</span>
          <span class="af-agent__sub"><span class="af-agent__now">waiting on you: push to main</span><span class="af-hb af-hb--wait"><i class="af-hb__dot"></i>41 min</span></span></span>
        <span class="af-agent__who"><span class="af-avatar af-avatar--person af-avatar--22">SK</span><span>Sean</span></span>
        <span class="af-agent__rig"><span class="af-avatar af-avatar--agent af-avatar--22">cx</span><span class="af-mono">gpt-5.1</span></span>
        <span class="af-rail af-rail--approval" style="--p:98%">…</span>
        <span class="af-stages"><span>Test<b>2 min</b></span><span class="is-now">PR<b>43 min</b></span></span>
        <svg class="af-spark af-spark--mini">…</svg>
        <span class="af-agent__cost">$0.62</span>
        <svg class="af-ic af-agent__chev">…chevron-right…</svg>
      </button>
      <div class="af-agent__body"><div>
        <div class="af-console">
          <section class="af-console__panel af-console__panel--decide" aria-label="Decision">…af-lead, af-cmd, af-pairs, af-acts…</section>
          <section class="af-console__panel af-console__panel--now" aria-label="Now">
            <div class="af-console__now"><span class="af-hb af-hb--wait">…</span><span class="af-console__big">waiting on you: push to main</span></div>
            <span class="af-rail af-rail--labeled af-rail--approval">…</span>
            <div class="af-pairs af-pairs--wide"><span><small>Owner</small>Sean Koval</span>…</div>
            <div class="af-acts">…Terminal, Run agent, Fork, Snapshot, Pause, +1 h; <div class="af-acts__end">Destroy</div></div>
          </section>
          <section class="af-console__panel af-console__panel--hist" aria-label="Activity">…ActivityTimeline…</section>
        </div>
      </div></div>
    </article>
  </div>
</section>
```

| Part | Class | Notes |
|---|---|---|
| Row | `af-agent` | `raised`, `radius-card`, a 1 px `edge-hi` top highlight; hover is a 4% `fg` tint. `--lit` (approval or input), `--failed`, `--denied` add the 3 px status edge on the left, inset from the corners; `--off` is hollow with a `line` hairline and dim text. `is-open` lifts it (`lifted`, `shadow-2`). |
| Line | `af-agent__line` | A `button` with `aria-expanded`; a ten-column grid at 1440, seven below 1200 (harness, sparkline and cost go), a stacked card below 760. |
| Parts | `__tail`, `__ttl` > `__work` + `__sub` > `__now` + `af-hb`, `__who`, `__rig`, `af-rail`, `af-stages`, `af-spark--mini`, `__cost`, `__chev` | Mono for the tail, the model, the cost and the stage times; sans for the work and the now-line. The sparkline ends in `fg`, not brand. |
| Body | `af-agent__body` > `div` > `af-console` | A grid-rows accordion (0fr → 1fr over `dur-open` with `ease-open`); the console fades in 80 ms later. Render the console only for the open row. |
| Console | `af-console` > `af-console__panel--decide` / `--now` / `--hist` | Two columns: the timeline left, the decision over the now panel right; one column below 760. Without a decision the now panel takes the first row. |

## Behaviour

`expand.wire(root)` in airframe.js toggles a row on click and closes it on Escape; `expand.open(el)` closes the other open row in the same `af-runway`, scrolls the row into view when it is off screen and focuses its line, and `expand.close(el)` returns focus to the line. `roving(root)` gives the runway one tab stop: arrows move between lines, Home and End jump, Enter opens. Refresh the now-line, heartbeat and rail in place on a tick; a full re-render would steal focus.

## When to use

hangar's Fleet in its default (List) view, and any list of agents where a lead reads sixty at once: the row holds what a tile cannot at 58 px per agent, stacks naturally on a phone, and opens where the person is looking. Switch it with AgentCard over one data model and one selection; the open agent stays open across the switch.

## Do

- Keep attention-first order inside a group: approval and input, then failed, denied, running, queued, off.
- Write the now-line as the agent would say it, in sentence case, present tense: "editing refunds/models.py".
- Keep the needs-you reason whole on a lit row; truncate the work, never the reason.

## Don't

- Don't tint a lit row; the edge, the mark and the word carry it. Selection and the open state are neutral.
- Don't put the brand yellow on a row: the primary action lives in the console.
- Don't move running rows while someone is looking; a new agent joins at the end of its group.
