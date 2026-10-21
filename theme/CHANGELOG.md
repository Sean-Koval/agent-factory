# Airframe theme changelog

Every change to a published theme file (the files generated from `airframe/`, including the docs-site mapping and the suite strip) gets an entry here, newest first, under a
new `## theme-vN` heading. Merging it to `main` tags `theme-vN` and opens a sync pull request in
each tool repo (hangar, flightdeck, ai-dlc, Tower), or prints the one-command sync when the
workflow has no cross-repo token. Keep token names stable; list each token whose value changed.

## theme-v14 · 2026-10-21

Product hues leave the status band, the decision words are one set, the last mono capitals go from the guides, and
every docs site gets the same footer (KAN-154). No token is added, renamed or removed.

Changed token values:

- `product-hangar`: Night `#EE8F63` → `#24C1C9`, Day `#A44C1D` → `#00787D` (clay → teal, OKLCH hue 200°). The clay sat
  beside `status-approval` (`#FF8A3D` / `#B04E00`).
- `product-tower`: Night `#C5A93B` → `#67B0F9`, Day `#816600` → `#1F6CB0` (brass → azure, OKLCH hue 250°). The brass
  read as the brand yellow.
- Both keep the family's lightness (OKLCH 0.74 Night, 0.52 Day) and meet 3:1 on `raised` and `canvas`. No product hue
  now sits between 0° and 100°, where failed, denied, needs approval and the brand live. `Products.md` states the rule.

Docs-site mapping (`airframe-docs.css`, `airframe-suite.html`, new `airframe-footer.html`):

- New `airframe-footer.html`: one footer for every site (the site's name, "part of the Agent factory suite", source,
  roadmap, Airframe). Vendor it and add `{% block footer %}{% include "partials/airframe-footer.html" %}{% endblock %}`
  to `overrides/main.html`; `copyright` and `extra.social` are no longer shown. The repository widget drops its star and
  fork counts.
- The 48px product marker at the far left of the header is gone; the marker under the active tab says where you are.
  The default `--af-product` is `fg` (neutral), not the brand yellow.
- The suite strip on phones scrolls the current item into view and fades whichever edge has more; the home link is
  a snap point, so the strip no longer opens scrolled past it.
- Below 960px the theme's floating "On this page" button (it covered text) is hidden, and the page's contents return
  to the menu drawer.
- Inline code in the nav and the table of contents is a quiet `raised` chip in both themes, not a black terminal chip
  in Day.
- `code.af-id` keeps a tail number on one line.

Words and guides:

- `Status.md` gains "Decision words": Needs approval, Needs input, Approve / Deny, Denied. Sign, Decline, Reject and
  Blocked are retired as UI words. ApprovalCard's quorum says "1 of 2 approved"; Button, Avatar, AgentRow, AgentCard
  and FleetConsole previews follow.
- Label and InlineData previews, the InlineData README, the Status, Data, PageHeader and Diff examples and the
  Airframe skill teach sentence-case keys (`Policy require-approval-main-push`), not mono capitals.
- Banners (`brand/`): sentence-case sans eyebrows ("Agent factory · Govern") and strip; the strip is the sites' strip
  (Define, Run, Judge, Govern, Setup, Design); Spaceport's place is Capability, off the strip.

## theme-v13 · 2026-10-20

The docs-site mapping catches up with theme-v12's type rule: labels are sentence-case sans, not mono capitals
(KAN-150 found them still in mono on the flightdeck site). `airframe-docs.css` and the DecisionDeck rules change; no token changes value,
none is added, renamed or removed.

- Tabs, nav titles, table headers, admonition and details titles, buttons, the eyebrow, figure captions, the tool-card
  kicker and the suite strip's home link and plane words are Red Hat Text 500, sentence case, no tracking.
  The strip's plane words go from .5rem to .55rem and its home link from .56rem to .6rem.
- `h4`–`h6` are sans 600 at .75rem in `fg-muted` instead of small mono capitals in `fg-subtle`.
- Code, IDs and numbers stay in DM Mono.
- The deprecated `brand-wash` is gone from the docs mapping: the accent wash, `<mark>` and highlighted code lines
  use `selected` (neutral), so Day no longer shows a yellow tint.
- DecisionDeck (`airframe-components.css`): the cards peeking behind the top one no longer show the 3px status edge (only
  the top card carries it). New `af-deck__subtitle` and `af-deck__stopped`: what stopped (failed, denied) is listed
  under up-next as "Stopped", visible at every width, and is no longer stacked with the decisions, so "1 of N" counts
  decisions only and agrees with the nav badge (found in hangar #343). The README and preview follow.
- New `af-gauge--mini` (`airframe-components.css`): a gauge in a list keeps a neutral `fg-muted` limit bug; a lone gauge
  keeps the `brand-text` bug. `Data.md` states the rule (found in Tower #86).

## theme-v12 · 2026-10-19

The new Fleet look and the decision deck (KAN-140, KAN-139): soft geometry, one step of lift, sentence-case sans labels,
motion tokens, and attention as **edge, mark, word** instead of a status-tinted box with an orange ring. From the hangar
Fleet direction "6, Decision deck". No token is renamed or removed; every class from theme-v11 still resolves.

Changed token values:

- `radius-control` 2px → 8px; `radius-card` 4px → 12px. Buttons, inputs, chips, tags, segments and tiles soften; cards,
  rows and panels take 12px. The denied placard keeps a 4px corner.

New tokens:

- Surface: `lifted` (Night `#1C1C1C`, Day `#FFFFFF`), the one step above `raised` for what is open or on top; `edge-hi`
  (Night `rgba(255,255,255,0.045)`, Day `#FFFFFF`), its 1px top highlight.
- Shadow: `shadow-1` (resting lift; Night `0 1px 2px rgba(0,0,0,0.5)`, Day `0 1px 2px rgba(0,0,0,0.06)`) and `shadow-2`
  (an open sheet or the top card of a deck; Night `0 20px 60px rgba(0,0,0,0.6)`, Day `0 16px 48px rgba(0,0,0,0.14)`).
  `shadow-overlay` is unchanged and now also covers toasts.
- Radius: `radius-sheet` 18px.
- Rail: `rail` (Night `#2A2A2A`, Day `#E3E3E0`), `rail-done` (Night `#D6D6D6`, Day `#2A2A2A`), `rail-glow` (Night
  `rgba(255,255,255,0.25)`, Day `rgba(0,0,0,0.12)`), `rail-h` 2px.
- Motion (new family; DTCG `duration` and `cubicBezier`): `dur-fast` 120ms, `dur` 200ms (was a 160ms constant in base.css),
  `dur-open` 300ms, `ease` `cubic-bezier(.2,0,0,1)`, `ease-open` `cubic-bezier(.32,.72,0,1)`. Under
  `prefers-reduced-motion` the three durations read as 0ms and every transition and animation is off. Tailwind gains
  `ease-airframe` and `ease-open`.
- `brand-wash` is **deprecated**: no Airframe rule uses it any more. It still resolves, unchanged, for older product CSS.

Type: `label` and `label-s` are sentence-case Red Hat Text (12/1.2 and 11/1.2, 500, no tracking); the mono capitals are
retired. `af-lbl`, `af-btn`, tabs, keys, table headers, stage words and the trace/iconset headings follow. Mono stays for
IDs, numbers, commands, the denied placard, the lamp legend and the terminal bar. `af-btn--text` is now a no-op.

Attention (`airframe-components.css`): every status `color-mix()` wash and inset outline is gone. `af-card--lit`,
`--failed`, `--denied`, `af-stand`, `af-bay`, `af-mini`, table and list rows (`is-attention`) keep a neutral ground and
take a 3px status edge on the leading side; selection is neutral (`selected`, a 1px `fg` ring on tiles, a 2px `fg` edge
on rows and trace and lane rows) where it was `brand-wash` and a yellow ring. The failed trace span loses its tint.
Danger buttons are red words with no red border (`af-btn--danger af-btn--secondary` for a hairline). Forced colors: the
edge is a 3px `CanvasText` border.

New components and classes (`runway.css`, a new stylesheet with its own forced-colors block):

- **DecisionDeck** (`af-deck`, `af-decision`, `af-reason`, `af-verdict-line`): one decision at a time, ordered by expiry.
- **AgentRow** and **AgentCard** (`af-runway`, `af-board`, `af-agent`, `af-console`): the List and Board views, opening in
  place. **ActivityTimeline** (`af-timeline`), **StageRail** (`af-rail`, `af-ring`, `af-capsule`, with `--est` for an
  estimate), **Heartbeat** (`af-hb`), and **FleetConsole**, the composed Fleet page.
- `af-nav__badge`: the orange Needs-you count. FleetView, FleetBays, FleetColumns and FleetOwners keep their classes and
  fold onto the neutral tile and the edge; hangar's default pair is List + Board.

`airframe.js`: `duration(name)`, `expand.open/close` (open in place, Escape, focus return), `deck.next/prev/go/leave`
(the deck, firing `af:deck`) and `roving(root)` (arrow keys by visual row).

Accepted bends, documented in `guide/Status.md`: the orange count badge, the heartbeat pulse (recency, not status; still
under reduced motion) and the rail-head glow.

## theme-v11 · 2026-10-19

Docs-site admonitions in the greyscale, and two icons for theme toggles (KAN-135). No token value changes; no class is
added or renamed.

- `airframe-docs.css`: every Material / Zensical admonition type (note, abstract, info, tip, success, question, warning,
  failure, danger, bug, example, quote and their aliases) maps onto the tokens through one custom property, `--af-adm`
  (`fg-subtle`): the 2px start mark, the title icon and the details chevron take it, the block is `surface` and the title
  has no tint. Only two families carry color, because a person must act: warning (caution, attention) is
  `status-approval`, danger (error) and failure (fail, missing) are `status-failed`. The modern Zensical theme paints
  each type's hue over the whole block (`.admonition.note { background: #448aff1a }`) and tints the chevron and the focus
  halo; those are overridden, and `:focus-within` is `focus` (2px) over the mark. Forced colors: the mark is a
  `CanvasText` border and focus an outline in `Highlight`.
- `airframe-icons.svg`: `sun` and `moon`, for a theme toggle (show the one the reader can switch to). 57 icons; the
  contact sheet gains a row.
- `tests/test_admonitions.py` renders every type in both themes in Chromium and fails when any mark, icon, block,
  title, chevron or focus ring computes to a hue that is not the type's one allowed token.

## theme-v10 · 2026-10-19

The suite strip and the stage track read at every size, in both themes, from the suite audit (KAN-48, KAN-113, KAN-73,
KAN-34). One token value changes: `brand-wash` (Night). No class is added or renamed.

- `brand-wash` (Night): `rgba(255,196,0,0.12)` → `rgba(255,196,0,0.10)`. The selected trace row sits on `raised`, and
  `status-failed` on the old tint measured 4.42:1 at 11.5 px; on the new one it is 4.67:1, so the duration a person reads on
  the critical path is AA. Day is unchanged (5.14:1). Selection in lanes and traces is a touch quieter in Night.
- `airframe-suite.html` (the strip's list): it now tells the suite story the deck tells. The four planes in order, Define =
  **Team harness** (links the team-harness repository), Run = hangar, Judge = flightdeck, Govern = Tower, then ai-dlc as
  **Setup** (it was labelled Define) and Airframe as Design. `extra.airframe.product` gains the value `team-harness`.
- `airframe-docs.css`:
  - `.af-suite__list small` and `.af-tool small`: `opacity: 1`. Material sets `.md-typeset small { opacity: .75 }`, which
    pulled the role words from `fg-subtle` (6.1:1 Night, 5.2:1 Day) down to 3.7:1 and 3.2:1; they are `fg-subtle` again.
  - Under 960 px the strip scrolls with `scroll-snap-type: x proximity` (each item snaps to the start), a right-edge fade
    on `.md-banner__inner::after` says there is more, and a spacer after the last item lets it scroll clear of the fade.
    Nothing is cut mid-word any more. Under 480 px the role words go and the strip shows product names only.
  - Forced colors: the fade is off.
- `airframe-components.css`:
  - `af-track__seg`: every stage word is `label-s` (10 px) in `fg-subtle`; a reached stage is `fg-muted`, the current one
    `fg`. The words not yet reached were 9.5 px `fg-dim` (3.1:1 Night, 2.5:1 Day); the brand book keeps `fg-dim` for
    separators and disabled marks. The pips are unchanged: `rule`, then `fg-subtle`, then `fg`.
- Gallery (`scripts/airframe.py gallery`): rows wrap their one-line description instead of ellipsizing it, and the five
  longest descriptions (ApprovalCard, Diff, Drawer, EmptyState, ObjectChip) are at most twelve words.
- Brand (`scripts/banners.py`, `brand/`): the eyebrows say `Agent factory · Run | Judge | Govern | Setup | Capability`,
  without the word "plane", which collided with flightdeck's data plane; the banner strip is the four planes with the team
  harness under Define, then Setup (ai-dlc) and Capability (Spaceport); the role words in the strip are `fg-subtle`, not
  `fg-dim`.
- Registry docs: the pinned install commands are generated from the newest `theme-vN`, like the header badge; the Airframe
  skill lists Cover and the test no longer exempts it.

## theme-v9 · 2026-10-19

Card heads and decisions that fit a narrow place, from hangar's quality pass (hangar #312): in the docked Fleet panel the
ApprovalCard head "Approval · APR-8E7F50C8 / Needs approval" ran past the card's edge, as "Needs input" had on the Question
card, and the decision buttons stacked into a ragged row. No token values change; no class is added or renamed, and at
full width nothing moves.

- `airframe-components.css`:
  - `af-card__top` wraps (`flex-wrap: wrap`): in a narrow place the status drops under the label, whole and visible, before
    anything is cut. Its `af-lbl` child gets `min-width: 0; max-width: 100%` and its `af-status` child `flex: none`.
  - `af-lbl__sub` ellipsizes (`min-width: 0; overflow: hidden; text-overflow: ellipsis`) only when the label alone is wider
    than its place; a later sub (`turn 7`, `editing`) gives way before the first (`flex-shrink: 1e5`), so a tail number
    outlasts its qualifier. The full text stays in the DOM. Section labels whose sub ran into the next column now ellipsize.
  - `af-approval__btns`: `max-width: 100%`; each `af-btn` in it is `flex: 1 1 auto` with centered content and the ghost
    (inspect) stays `flex: none`, so once the row has wrapped the buttons share each line and the primary never sits alone
    at the end of a ragged row. The row is still as wide as its buttons, so nothing stretches until it wraps. In
    `af-approval__reason` the row is `align-self: flex-start` for the same reason. This replaces the container query hangar
    carried in `app.css` (`.needs, .job-detail, .fd { container-type }` and `@container (max-width: 420px)`), which it can
    drop on sync.
  - `af-question__act > .af-btn`: `max-width: 100%`.
  - Long mono values wrap inside their cell instead of past the card's edge: `af-meta__item` gets `max-width: 100%` and
    `af-meta__val` `min-width: 0; white-space: normal; overflow-wrap: anywhere` (a policy name or receipt in the policy
    line of a verdict row or an approval card at 320 px); `af-verdict__why` and `af-question__ctx code` get
    `overflow-wrap: anywhere`. A receipt ID in `af-receipt b` never breaks at its hyphens (`white-space: nowrap`); the
    words beside it wrap.
  - `af-verdict` is its own query container (`container-type: inline-size`): under 420 px the time
    (`af-verdict__time`) drops under the words, right-aligned, so the third column collapses and the body keeps its width.
- `airframe-docs.css` (the docs sites):
  - `af-hero--visual`: the dot field is off below 960 px, where the hero is one column and the field sat behind the
    lower right of the lede on phones; it shows only beside the visual, from 960 px (`display: none` / `block` on the
    `::after`, same inset as before on wide screens).
  - The hero figure's caption is a sentence, so it is set as one: `body-s` in the body face (`.65rem`, Red Hat Text),
    sentence case, left-aligned, `fg-subtle`, instead of tracked mono capitals that wrapped to two centred lines at
    1440 px. `af-figure` captions are unchanged.
- ApprovalCard, Question: the previews end with the card at 320 px; the READMEs say what wraps and what gives way. Card and
  Label READMEs note the wrapping head and the ellipsizing sub.

## theme-v8 · 2026-10-18

The docs look, shared: every product's docs site reads as one family and links to the others. No token values
change; no `af-` component class changes.

- New published file `airframe-suite.html`: the suite strip, one quiet row above the docs header that names the
  suite and links each product's public docs site (agent factory, hangar, flightdeck, Tower once public, ai-dlc,
  Airframe), with the 2px product marker under the current one. It is a Material / Zensical partial, rendered
  server side, so it works without JavaScript on Material for MkDocs and on Zensical. A site adds it with config
  only: `theme.custom_dir: overrides`, a two-line `overrides/main.html` that extends `base.html` and includes
  `partials/airframe-suite.html` in the `announce` block, and `extra.airframe.product: <name>` for the current
  item. Tool repos vendor it with `sync-airframe.sh` (`airframe-suite.html overrides/partials/airframe-suite.html`).
  The list lives in the partial, not in each site's config, so the family stays identical everywhere.
- `airframe-docs.css`:
  - `.md-banner` and `.af-suite*`: the strip's layout and type (mono capital plane, product name in the display
    face, `fg-muted` at rest, `fg` and the `--af-product` marker when current, `fg-subtle` for an unlinked item).
    Below 600px the plane words drop and the row scrolls sideways.
  - Page anatomy: the first paragraph after the page title is the lede on every page (`h1 + p`, `fg-muted`, `.9rem`,
    62ch), so a page written as "title, one sentence, sections" reads the same on every site without markup.
  - `af-hero--visual`: a variant of the home hero with a slot for a real product capture, `figure.af-hero__visual`
    (image or video, `radius-card`, a 1px `line` edge, a mono caption). Words left, the product on the right from
    960px; the visual follows the actions below that.
  - The hero's dot field no longer sits behind the words on phones: below 960px it is a small field at the top
    right, as on the README banners; the headline drops to 2em. On wide screens it starts at 64% so it stays off
    the lede.
  - Tables take the full column width (`display: table; width: 100%`) instead of shrinking to their content and
    wrapping every cell; wide tables still scroll inside `.md-typeset__scrollwrap`.
  - Code blocks scroll sideways (long commands are not wrapped): `pre > code` gets `padding-right: 3em` so the end
    of the longest line clears the copy button, and `.md-clipboard` sits on the terminal ground (`terminal-bg`,
    `terminal-dim`, `terminal-fg` on hover) instead of over the glyphs.
  - The plain `af-hero` no longer draws an empty dot-field stage; the field appears only behind a visual
    (`af-hero--visual`), as the brand book places it behind hero data.
  - A `@media (forced-colors: active)` block, the first in the docs mapping: the tab, nav, strip and admonition
    markers become borders in system colors, the dot field and header marker go, swatches and hero visuals keep an
    outline.
- `airframe-docs.css` and `airframe-suite.html` are now built from `airframe/docs-site/` by `scripts/airframe.py
  build` (the CSS gets the release stamp), so `check` catches drift and the forced-colors test covers them like
  the other stylesheets.

## theme-v7 · 2026-10-18

Docs fix: the secondary docs button now matches Airframe's Button. No token values change.

- `airframe-docs.css`: `.md-typeset .md-button` gets `background: transparent`. The docs theme's default filled it
  with `--md-default-fg-color--lightest`, a grey in both Night and Day, but Airframe's secondary button is a
  `line-strong` hairline with no fill. Hover and the primary button (`.md-button--primary`) are unchanged.

## theme-v6 · 2026-10-18

Airframe for agents: the parts a person needs to work with an agent, from the design team's research, audit and Tower
streams and Sean's decisions of October 17. No token values change; no existing class changes its look except where noted.

- New published file `airframe.js` (copied from `airframe/js/airframe.js` by the build): one ES module, no dependencies,
  no build step, no Web Components. Markup helpers that match the contracts with every value escaped: `status`, `icon`,
  `meta`, `btn`, `avatar`, `obj`, `tag`, `el`. Behaviours: `toast(msg, {tone, action, timeout, critical})`,
  `confirm({title, body, ok, cancel, danger, inspect})` returning `Promise<boolean>` on an `af-dialog`, and
  `drawer.open/close/toggle` with Escape, focus return and an inert page. Alert inhibition: while an `af-dialog` or
  `af-drawer` is open, or a text field has focus, non-critical toasts are held and shown afterwards (`inhibited()`, `flush()`).
- `airframe-components.css` gains two stylesheets, `agents.css` and `patterns.css`, and these classes:
  - ApprovalCard v2: `af-approval__reason` (deny with a required reason: an `af-field` with `af-input--area` and an
    `af-field__error` carrying the failed mark and words), `af-approval__edit` and `af-approval--editing` (the arguments
    become editable; the primary reads "Approve edited"), `af-approval__hint` (what "Approve for this session" grants and for
    how long), `af-approval__quorum` and `af-approval__signed` (signer avatars, "1 of 2 signed"), `af-approval--waiting`
    (waiting on others: the queued ring and words, no lit ring, no primary), `af-verdict__ok` (approved is a quiet check and
    a word) and `af-verdict__why` (a denial carries its reason). The action row wraps.
  - Question: `af-question`, `af-question__q`, `__ctx`, `__opts`, `__free`, `__act`; the approval role with the word
    "Needs input"; free text dismisses the option chips through `:has()`.
  - Composer: `af-composer`, `af-composer__queued` ("Queued · applies after this tool call" with a take-back),
    `__qmsg`, `__box`, `__input`, `__row`, `__chips`, `__send`, `__why`; `is-disabled` says why.
  - Diff: `af-diff`, `af-diff__file`, `__path`, `__stat`, `__add`, `__del`, `__tools`, `__hunk`, `__hunk--failed`, `__hh`,
    `__line`, `__line--ctx|add|del`, `__n`, `__s`, `__code`, `__cmt`, `__more`, `__thread`, `__note`; `af-comment`,
    `af-comment__who`, `__name`, `__time`, `__text`. Greyscale: additions in `fg` with a 2px `fg` gutter bar, deletions in
    `fg-muted` with a 2px `line-strong` bar, context in `fg-subtle`; the only color is the failed triangle on the hunk a
    failing test points at.
  - Avatar: `af-avatar--person|agent|firm`, `af-avatar--22|28|44`, `af-avatar--pending`, `af-avatars`, `af-avatars__more`,
    `af-who`, `af-who__name`, `__sub`. People round, agents hexagonal (clip-path, with a forced-colors edge and a
    no-clip-path square fallback), firms square. The plain `af-avatar` (the nav's account button) is unchanged except that
    its pointer cursor and hover now apply only to a `button` or `a`.
  - ObjectChip: `af-obj`, `af-obj--link`, `af-obj--restricted`, `af-obj__key`, `__title`, `__state` (with
    `af-status--approval` for the one color a chip may carry), `af-obj__trust`, `af-objs`.
  - Button: `af-btn--text`, sentence-case Red Hat Text 13.5 px (13 small); the rule "friendlier where people read, mono
    where data is" is in the Button README.
  - Controls: `af-input--area` (a textarea in the input well), `af-input--sans`, `af-field__error`, `af-chip`,
    `af-chip--mono`, `af-chip--sm`, `af-chips`; `af-id` no longer wraps.
  - Patterns (new dsCard group): PageHeader `af-page-head`, `af-page-head--s`, `--rule`, `__text`, `__title`, `__lede`,
    `__sum`, `__actions`; EmptyState `af-empty[data-kind]`, `af-empty--clear`, `--compact`, `__title`, `__text`,
    `__counts`, `__act`, `__body`; Toast `af-toasts`, `af-toasts--inline`, `af-toast`, `af-toast--bad`, `__msg`, `__act`,
    `is-leaving`; Dialog `af-dialog`, `af-dialog--wide`, `--danger`, `__form`, `__head`, `__title`, `__body`, `__foot`;
    Drawer `af-scrim`, `af-drawer`, `af-drawer--right|bottom`, `__head`, `__title`, `__body`, `__foot`, `__grip`, and the
    `is-open` state; layer variables `--af-z-scrim` 100, `--af-z-drawer` 110, `--af-z-toast` 120, sizes `--af-drawer-w`
    480px, `--af-drawer-h` 40vh, `--af-drawer-inset` (set through `html.af-drawer-open--bottom`).
  - Forced colors: every new part keeps its edges and marks in system colors (gutter bars and the hexagon edge in
    `CanvasText`, pressed chips in `Highlight`, the diff and chips as outlines).
- `registry.json`: new items `helpers` (airframe.js), `approval-card`, `question`, `composer`, `diff`, `avatar`,
  `object-chip`, `page-header`, `empty-state`, `toast`, `dialog`, `drawer`; the skill lists every component.
- Brand book: `guide/Status.md` adds "A question is not an approval, but it is the same role", "Waiting on others stays
  grey", "Alert inhibition" and the Carbon and Airbus ECAM sources; `guide/brand.md` adds "Who has the controls" (Agent has
  control, grey; You have control, brand) and the avatar triad; `guide/Data.md` adds the greyscale diff rule and objects by
  reference. The command palette is deferred to theme-v7.

## theme-v5 · 2026-10-17

Distribution, from the design team's registry stream: Airframe can now be installed with the shadcn CLI and
consumed from Tailwind and token tools. No token values change and no existing file changes.

- New published files, generated by `scripts/airframe.py build`:
  - `airframe-tailwind.css`: a Tailwind CSS v4 `@theme inline` that maps every color token (`bg-canvas`, `text-fg-muted`,
    `bg-brand text-on-brand`), the faces (`font-sans`, `font-mono`, and `font-display` as a utility that also sets the
    width axis), the type styles (`text-body`, `text-label`, with line-height, weight and tracking), radii
    (`rounded-card`), the overlay shadow and the layout heights (`h-row`, `max-w-page`) onto `var(--af-*)`. Tailwind's
    default color, font, radius and shadow scales are reset, so an Airframe project has no `bg-blue-500`.
  - `airframe.tokens.json` (Night) and `airframe-day.tokens.json` (Day): the tokens in the W3C Design Tokens Format
    Module 2025.10, one complete file per theme, each token carrying its CSS name under
    `$extensions["io.github.sean-koval.airframe"]`.
- `registry.json` at the repository root: a shadcn-compatible registry of universal items (`airframe`,
  `airframe-tailwind`, `airframe-tokens`, `skill`, `button`, `status`, `card`, `fleet-bay`, `react`). The docs site
  serves the built items under `/r/`; the repo itself is a GitHub source registry pinned by tag.
- `.claude/skills/airframe/SKILL.md`: the Airframe skill for coding agents, also installed by the `skill` item.

## theme-v4 · 2026-10-17

Accessibility patch from the design team's research stream: statuses now survive forced colors (Windows Contrast
Themes), and the guide states one attention order. No token values change.

- `airframe-components.css`: each stylesheet gains an `@media (forced-colors: active)` block in system colors only.
  Before, the browser's forced palette erased the running, approval, failed and off marks, the denied placard's fill,
  the lit card ring, tile edges, fleet pips, lane stages and trace spans, leaving only the words.
  - Status marks, stand marks and lane marks paint in `CanvasText`, so the circle, diamond, triangle and dot still
    say the status; the queued ring and the denied placard become outlines.
  - Cards, stands, bays and minis get a 1px outline; lit and attention variants (`af-card--lit`, attention rows and
    tiles, failed spans) a 2px one; human waits a 2px outline; queues stay dashed.
  - Selection (`aria-pressed` stands, selected bays, minis, table rows, lanes, trace rows, pressed segments) uses
    `Highlight`; the lanes' now line too.
  - The primary button keeps a 2px `ButtonText` border so it still reads as the primary action.
- Brand book: `guide/Status.md` states the attention order once, for group marks, columns and counts alike:
  approval, failed, denied, then running, queued, off (it said denied first, which contradicted FleetView and the
  hangar console); `FleetBays` now matches. Adds the forced-colors rule.

## theme-v3 · 2026-10-17

Fleet views: the same sandboxes four ways, chosen by Sean from the fleet layout study. No token
values change.

- `airframe-components.css` gains three components and their shared parts:
  - FleetBays (`af-bays`, `af-bay`): a box per sandbox with its task, owner, harness, a labeled
    stage track, lease left and one action; dashed "Start in …" bay per environment.
  - FleetColumns (`af-statecols`, `af-statecol`, `af-mini`): one column per state, attention
    first, Running two wide, sticky heads.
  - FleetOwners (`af-owners`): people down, environments across, stand tiles in the cells, with
    each person's share of the per-person cap.
  - Shared: `af-cap` (capacity bar), `af-track` (labeled plan / edit / test / PR track),
    `af-person` (initials and name).
- `af-seg__btn` also styles links: `aria-current="page"` reads as pressed, so a segmented switch
  can move between pages or views.
- Brand book: Tower's tail-number prefix is `TWR-` (`TWR-APR-0391`, `TWR-RCPT-88A1`), replacing
  `WS-` from the governed-workspace name.

## theme-v2 · 2026-10-17

Airframe's full system moves here and becomes the source of truth. Values now live in
`airframe/tokens.json` and the component CSS in `airframe/styles/`; `scripts/airframe.py build`
generates `theme/airframe.css` from them (no longer hand-written) and three new published files.
This is the system on the claude.ai Design System page, which is now a viewer of this repo.

New published files (tool repos vendor the ones they need):

- `airframe-components.css`: the `af-` component classes (buttons, statuses, cards, tables,
  navigation, master caution, approval card, terminal, fleet board and table, session lanes,
  trace spans, readouts, product marks, icons) and the `.af-type-<style>` type classes.
- `airframe-icons.svg`: the 55-icon sprite (`#af-<name>`); `agent` is a hex unit, not a plane.
- `airframe-tokens.json`: tokens resolved per theme, for diagrams, decks and charts.

Renamed tokens (the theme-v1 names stay as aliases in every theme scope; new code uses the new names):

- `--af-st-run|queue|appr|fail|deny|off` → `--af-status-running|queued|approval|failed|denied|off`
- `--af-p-hangar|flightdeck|aidlc|spaceport` → `--af-product-…`; `--af-p-workspace` → `--af-product-tower`
- `--af-term-bg|fg` → `--af-terminal-bg|fg`; `--af-code-k|f|s|n|c` → `--af-code-keyword|function|string|number|comment`
- `--af-dot` → `--af-dot-field`; `--af-f-display|sans|mono` → `--af-font-display|sans|mono`
- `--af-r-ctl`, `--af-r-chip` → `--af-radius-control`; `--af-r-card` → `--af-radius-card`; `--af-pad` → `--af-space-16`; `--af-gap` → `--af-space-12`

Changed values, Night (`dark`):

- `--af-line-subtle` `#161616` → `#1F1F1F` and `--af-line` `#1F1F1F` → `#2A2A2A` (dividers were invisible on raised cards)
- `--af-rule` `#3A3A3A` → `#424242`
- `--af-status-approval` (was `--af-st-appr`) `#FFB224` → `#FF8A3D`: caution is orange so it can never read as the brand yellow

Changed values, Day (`light`): paper-grey page with white cards (theme-v1 had a white page with grey cards):

- `--af-canvas` `#FFFFFF` → `#F4F4F2`; `--af-surface` `#F8F8F7` → `#EDEDEB`; `--af-raised` `#F1F1F0` → `#FFFFFF`; `--af-selected` `#E8E8E7` → `#E6E6E3`
- `--af-line-subtle` `#EDEDED` → `#E6E6E3`; `--af-line` `#E0E0E0` → `#DCDCD9`; `--af-line-strong` `#858585` → `#858583`; `--af-rule` `#C9C9C9` → `#BDBDBA`
- `--af-fg` `#000000` → `#0A0A0A`; `--af-fg-muted` `#4D4D4D` → `#474746`; `--af-fg-subtle` `#6B6B6B` → `#666664`; `--af-fg-dim` `#A3A3A3` → `#9C9C99`
- `--af-brand-wash` `.16` → `.18` alpha; `--af-status-queued` `#6B6B6B` → `#666664`; `--af-status-approval` `#9A5B00` → `#B04E00`; `--af-status-off` `#858585` → `#858583`; `--af-dot-field` `#E0E0E0` → `#DCDCD9`

New tokens: `on-status-denied`, `lamp-caution`, `lamp-warning`, `on-lamp`, `terminal-dim|ok|err`,
`span-model|tool|sandbox`, `stage-plan|edit|test`, `readout-cell`, `display-window`, `chart-1…6`,
`shadow-overlay`, the `space-*` scale (2 to 160), `radius-none`, `radius-round`, `container-max`,
`header-h`, `row-h-compact`, `lane-h`, `span-h`, `icon-stroke`, `icon-size`.

Theme scopes: `data-theme` now works on any element (nested scopes), not only `<html>`.

`airframe-docs.css`:

- Token references use the new names.
- Table headers have no fill: mono capitals over a 1px `--af-line` rule.
- The product hue comment now declares `--af-product` on `[data-md-color-scheme]` too, so the Day hue follows a theme switch.

## theme-v1 · 2026-10-17

First tagged release: the "Night Panel" flavor (black canvas, signal-yellow accent, Archivo
Expanded display, Red Hat Text body, DM Mono labels, 2px radius, quiet status colors).
Changes since the copy the tool repos first vendored:

- `airframe.css`, light theme (both the `prefers-color-scheme` block and `[data-theme="light"]`):
  - `--af-surface` `#F7F7F7` → `#F8F8F7`
  - `--af-raised` `#FFFFFF` → `#F1F1F0` (tonal cards instead of white-on-white)
  - `--af-selected` `#EBEBEB` → `#E8E8E7`
- `airframe-docs.css`:
  - Footer sits on the canvas with a top rule (`.md-footer`, `.md-footer-meta`, `.md-copyright`).
  - `figure.af-figure` spans the full column; its SVG or image scales to width; captions upright.
