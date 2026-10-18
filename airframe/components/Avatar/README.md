Avatars are a triad of silhouettes used across the suite: people are round, agents are hexagonal, firms are square; each is initials in DM Mono on a 1px `line-strong` edge with no fill and no hue, in 22, 28 or 44 px, alone, beside a name, or stacked.

## You provide
- The kind: `af-avatar--person`, `af-avatar--agent` or `af-avatar--firm`. The plain `af-avatar` (30 px, round) is the nav's account button and stays as it was.
- Two initials, or for an agent without a name the `agent` icon (the hexagon is that icon's unit); `?` with `af-avatar--pending` for a person or firm still expected, and `af-avatar--pending` with the icon for an agent slot not yet filled.
- A size: `af-avatar--22` in meta and quorum strips, `af-avatar--28` in rows and beside names, `af-avatar--44` in page headers and profiles.
- A `title` and, when the avatar stands alone, `aria-label` with the full name; `aria-hidden="true"` when the name is written next to it.
- For a stack, `af-avatars` around them (optionally `af-avatars__more` for `+2`); set `--af-avatar-ground` to the ground the stack sits on when it is not `raised`, and `--af-avatar-fill` for the hexagon's fill when the avatar sits on the canvas.
- `af-who` for avatar, name and a sub line in one row.

## Markup
```html
<span class="af-avatar af-avatar--person af-avatar--28" title="Priya Natarajan" aria-label="Priya Natarajan" role="img">PN</span>
<span class="af-avatar af-avatar--agent af-avatar--28" title="codex" aria-hidden="true">CX</span>
<span class="af-avatar af-avatar--agent af-avatar--44" title="Breaks" aria-hidden="true"><svg class="af-ic" …>agent</svg></span>
<span class="af-avatar af-avatar--firm af-avatar--22" title="Globex" aria-hidden="true">GX</span>
<span class="af-avatar af-avatar--person af-avatar--22 af-avatar--pending" title="Not signed yet">?</span>

<span class="af-avatars" aria-label="Signers: Priya, Sean, Marcus and 2 more">
  <span class="af-avatar af-avatar--person af-avatar--28" title="Priya Natarajan">PN</span>
  <span class="af-avatar af-avatar--person af-avatar--28" title="Sean Koval">SK</span>
  <span class="af-avatar af-avatar--agent af-avatar--28" title="codex">CX</span>
  <span class="af-avatars__more">+2</span>
</span>

<span class="af-who"><span class="af-avatar af-avatar--agent af-avatar--28" aria-hidden="true">CX</span><span class="af-who__name">codex</span><span class="af-who__sub">gpt-5.1, sponsored by Sean</span></span>

<button type="button" class="af-avatar" aria-label="Account: Sean">SK</button>   <!-- the nav, unchanged -->
```

| Kind | Shape | Class | Who |
|---|---|---|---|
| person | round (`radius-round`) | `af-avatar--person` | people: approvers, requesters, owners |
| agent | hexagon (`clip-path`) | `af-avatar--agent` | agents: harnesses, chat agents, copilots |
| firm | square (`radius-control`) | `af-avatar--firm` | firms: clients, counterparties, custodians |

The hexagon is three clipped layers (a ground ring, a 1px edge, the fill) in a box 4 px larger than its siblings with a −2 px margin, so the visible shape matches the circle beside it and the stack ring has room. In forced colors the edge paints `CanvasText` and the fill `Canvas`, so the shape survives; where `clip-path` is unsupported the agent falls back to a square with a 0 radius (the firm keeps its 2 px), still distinct.

## When to use
- Anywhere a person, agent or firm appears as an actor: approval signers, "requested by", session owners, Tower's spaces and object pages, comment threads.
- The nav keeps the plain `af-avatar` for the account button.

## Do
- Use one silhouette per kind everywhere, so a hexagon always means an agent before anyone reads the name.
- Pair the avatar with a name the first time an actor appears on a page; alone, give it a label.
- Mark an expected-but-missing actor as pending (dashed edge, `?`), never with a status color.

## Don't
- Don't fill an avatar with a product hue, the brand yellow or a status color, and don't put a status dot on it; status belongs to the work, not the actor.
- Don't use photos or logos; initials or the agent glyph only.
- Don't give agents round avatars or people hexagons to save space; use a smaller size instead.
