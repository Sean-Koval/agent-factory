# FleetConsole

The composed Fleet page hangar's console mirrors: the headline in words ("19 agents at work. Two need you, 2 stopped."), the DecisionDeck on top, and the fleet below as the runway (AgentRow) or the board (AgentCard), switched by one segmented control over one data model and one selection; an agent opens in place into its console. The nav's Needs-you count is the orange badge.

## What you provide

Everything AgentRow, AgentCard and DecisionDeck ask for, plus the fleet's totals (agents at work, how many need you, how many stopped, slots used, spend today) and the pools with their slots. The preview is one live fixture: deciding on the deck changes the row, a quiet ticker moves the running agents, and `?view=board`, `?open=HGR-3MX9` and `?deny=1` show the other states.

## Markup

```html
<header class="af-nav af-hue--hangar">…<a class="af-nav__tab" href="#needs">Needs you<span class="af-nav__badge">2</span></a><a class="af-nav__tab" aria-current="page">Fleet<span class="af-nav__count">27</span></a>…</header>
<main>
  <h1 class="af-page-head__title">19 agents at work. <em>Two need you</em>, 2 stopped.</h1>
  <span class="af-seg" role="group" aria-label="View"><button class="af-seg__btn" aria-pressed="true">List</button><button class="af-seg__btn" aria-pressed="false">Board</button></span>
  <button class="af-btn af-btn--primary">New sandbox</button>
  <section class="af-deck" aria-label="Needs you">…DecisionDeck…</section>
  <section class="af-runway__group">…AgentRow rows, or af-board of AgentCard…</section>
  <div class="af-runway__key">…the six marks, a rail, the keys…</div>
</main>
```

| Part | Notes |
|---|---|
| Headline | Archivo Expanded in sentence case; the `<em>` ("Two need you") is the status as the subject and the one colored word on the page. |
| Nav badge | `af-nav__badge`: the orange count. Zero is `af-nav__count`, grey. |
| View switch | `af-seg`: the open agent stays open across List and Board. |
| Key | `af-runway__key`: marks, not prose; the keyboard hint sits at its end and goes on a phone. |

## When to use

As the reference for hangar's Fleet and Needs you pages and for Tower's Desk; it is the one place every runway part is composed, so a change to any of them is checked here in Night, Day, 1440 and 390.

## Do

- Keep the deck above the fleet: what needs you comes first.
- Keep one primary button on the page (New sandbox) and the yellow only there, on focus and on the decision's primary.

## Don't

- Don't add a second colored word to the headline; "stopped" stays `fg`.
- Don't show a badge when the count is zero.
