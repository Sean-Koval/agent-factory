# Airframe

**Agent infrastructure, quiet until a human is needed.**

Airframe is the shared design system for Sean's agent-infrastructure consoles. It works like a dark cockpit: black, white and grey while agents work, one signal yellow for what is yours to act on, and color only when something needs a person. Build every console, docs page and marketing page for these five products from it.

| Product | What it is | Tail numbers |
|---|---|---|
| **hangar** | Control plane for cloud coding-agent sandboxes: fleet, environments, sandboxes, sessions, jobs, approvals, traces. | `HGR-7Q2K` |
| **flightdeck** | Harness evals: experiments, behavior checks over traces, promotion (the approver is never the author). | `FDK-EXP-0142` |
| **Tower** (governed workspace) | One policy decision point for people and agents: decisions, approvals, receipts, audit trail. | `TWR-APR-0391`, `TWR-RCPT-88A1` |
| **ai-dlc** | Portable dev-environment kit: roles mapped to providers, a CLI and docs. | none |
| **Spaceport** | Catalog of data products: cards, schemas, lineage. | none |

Three further sections carry the detailed rules: **Status** (the six statuses), **Data** (tables, inline data, readouts, traces, lanes, charts) and **Products** (marks, hues, nav marker).

## Principles

1. **Dark cockpit: quiet until a human is needed.** Normal is grey. Running is a quiet `status-running` circle; nothing turns green, glows or blinks. Color appears only for needs approval (`status-approval`), failed (`status-failed`) and denied (`status-denied`). A screen with no color on it means nobody is needed.
2. **One hot color.** Signal yellow (`brand`) marks what is yours: the primary action, the focus ring, the trace critical path, the now line, the selected mark. Use one primary button per view. Yellow never means a state.
3. **Tonal, not boxed.** Separate by tone and space, not lines. Cards are `raised` on `canvas` with no border; dividers inside them are `line-subtle`.
4. **Data first.** Show the real ID, the real number, the real policy name. Set data in DM Mono with tabular figures and let chrome recede.
5. **Sharp, never glossy.** 2px controls, 4px cards, 1px lines. No gloss, glow, blur, gradients or card shadows.

## Content fundamentals

### Voice

- Write short, plain, specific sentences: what happened, to what, and what is needed. "HGR-3MX9 is holding at PR. Push to main needs your approval."
- Let numbers be the proof: "38 of 41 passed", not "most tests passed".
- Speak as the system, in statements. Address the reader as "you" only when they must act ("Waiting on you"). Never "we" or "I".
- Use aviation terms only where they clarify: hold, cleared, spun down, on approach. Never cute.
- Write real content only: no lorem ipsum, no invented praise, no filler stats. No emoji, no exclamation marks.

### Casing

- Sentence case for headlines, titles, body, menu items and status words: "Forty agents. One needs you.", "Needs approval".
- Mono capitals for labels, buttons, keys, tabs and table headers. Write the source text in sentence case and let `af-lbl`, `af-btn`, `af-meta__key` and the `label` / `label-s` styles uppercase it (tracking .06–.09em), so screen readers read words, not letters.
- Product names keep their case everywhere, even at the start of a sentence: hangar, flightdeck, Tower (the governed workspace), ai-dlc, Spaceport, Airframe.
- Policy, branch, model and command names stay exactly as typed: `require-approval-main-push`, `gpt-5.1`, `claude-code@2.1`.

### Tail-number IDs

- Give every object a person can point at a tail number: product prefix, optional type, short code; uppercase, hyphenated. `HGR-7Q2K` sandbox, `FDK-EXP-0142` experiment, `TWR-APR-0391` approval, `TWR-RCPT-88A1` receipt.
- Set IDs in `af-id` (DM Mono 500). Never lowercase, wrap or truncate an ID; truncate the description beside it. The fleet board may show the code alone (`7Q2K`) because the pool header carries the prefix.
- Lead with the ID: "HGR-0PZ4 failed at test", not "Test failed for sandbox HGR-0PZ4".

### Numbers and units

- Use tabular figures wherever numbers stack (`data` style, `af-num`, `af-mono`). Right-align numeric columns.
- Put a space between number and unit: `14.0 s`, `41 min`, `2 vCPU`, `48.6k tokens`. No space before `%` or after a currency sign: `61%`, `$1.18`.
- Elapsed clocks as `00:41:07`. Span durations in seconds with one decimal. Relative time axes run `-60 min` to `now`.
- Money: two decimals in tables (`$0.42`), whole units in headlines (`$142`). Group thousands: `2,481`.
- Ratios in words: `22 of 24 slots`, `38 of 41`. Never `38/41`.
- Show zero as a number (`0`, `$0.00`). Use an em dash only for "not applicable".

### Example copy

- **hangar.** Headline: "Forty agents. One needs you." Lede: "hangar runs coding agents in isolated cloud sandboxes, holds risky steps for a human, and files a receipt for every decision." Alert: "HGR-3MX9 is holding at PR. Push to main needs your approval." Empty: "No sandboxes running. Start one from an environment." Buttons: Start a sandbox, Snapshot, Fork.
- **flightdeck.** Headline: "Planner prompt v4". Result: "v4 beats v3 on 7 of 9 behavior checks. Tool-call budget regressed 12%." Gate: "Promotion needs an approver who is not the author." Buttons: Promote, Hold.
- **Tower.** Request: "codex wants to push to main. Policy require-approval-main-push holds it for you." Outcome: "Approved by Sean at 14:02. Receipt TWR-RCPT-88A1." Denial: "Denied by policy deny-secrets-egress. No receipt issued." Buttons: Approve, Deny.
- **ai-dlc.** CLI: "Environment base-codex ready in 41 s." Docs: "Map each role to a provider once. Every repo picks it up."
- **Spaceport.** Card: "orders_daily refreshed at 06:00." Gate: "Schema change on orders_daily needs the owner's approval."

### Words to avoid

| Avoid | Write instead |
|---|---|
| simply, just, easy, seamless, effortless | what actually happens |
| powerful, blazing, magic, revolutionary, AI-powered | a number |
| Oops, Uh-oh, Something went wrong | what failed and what to do next |
| Submit, OK, Click here, Please (on buttons) | the verb: Approve, Start a sandbox |
| Error, Warning (alone) | Failed, Needs approval, Denied, plus the reason |
| `a · b · c` metadata strings | keyed inline data (see Data) |
| pilot, captain, takeoff, mayday | hold, cleared, spun down, and only where they clarify |

## Visual foundations

### Color roles

- **Ground.** `canvas` for the page; `surface` for recessed wells (inputs, the terminal bar, display windows); `raised` for cards and panels; `overlay` for menus, popovers and hover rows; `selected` for the selected row or tab.
- **Lines.** `line-subtle` between rows inside cards and tables; `line` for hairlines (table header rule, chips, keys); `line-strong` for control borders (3:1 or better on `surface` and `raised`); `rule` for section rules and chart axes where there is no card.
- **Text.** `fg` for primary text and values; `fg-muted` for secondary text and inline values; `fg-subtle` for labels, keys and timestamps (the lowest text tone, 4.9:1 or better); `fg-dim` for separators and disabled marks, never text.
- **Brand.** `brand` fill with `on-brand` text; `brand-hover`; `brand-text` for brand as text or a 1px line; `brand-wash` behind a brand-marked selection; `focus` for the ring.
- **Status.** `status-running`, `status-queued`, `status-approval`, `status-failed`, `status-denied` with `on-status-denied`, `status-off`. Lamps `lamp-caution` and `lamp-warning` with `on-lamp` text are the only large color fields in the UI, and only in MasterCaution.
- **Terminal and code.** `terminal-*` and `code-*` stay dark in both themes. Code is greyscale; only `terminal-err` carries color.
- **Data.** `span-model`, `span-tool`, `span-sandbox`; `stage-plan`, `stage-edit`, `stage-test`; `chart-1` to `chart-6`; `readout-cell`, `display-window`; `dot-field`.
- **Product.** `product-hangar`, `product-flightdeck`, `product-tower`, `product-aidlc`, `product-spaceport`: marks, docs headers and the 2px nav marker only.

### The brand is never a status

Use `brand` for the primary action, focus, the active route (trace critical path, now line) and selected marks, and nothing else. Never color a status, alert, badge or chart series yellow. Caution is orange for exactly this reason: cockpits paint caution amber, and an amber "needs approval" beside a yellow primary button would read as one signal. So `status-approval` is orange (`#FF8A3D` Night, `#B04E00` Day) and always a diamond, and a yellow fill always means "your action". Product hues never carry state either.

### Night and Day

- Set the theme on the root: `<html data-theme="dark">` for Night (the default) or `data-theme="light"` for Day. Tokens re-declare per theme; never branch on theme in component CSS.
- Night is true black (`canvas` `#000000`) with `raised` `#141414` cards. Day is paper grey (`canvas` `#F4F4F2`) with white `raised` cards.
- The `brand` fill is the same yellow in both. For brand as text or a line use `brand-text`, which drops to dark gold `#7A5F00` in Day, since yellow on paper is 1.5:1.
- Terminals, code blocks and lamp fills keep their values in both themes.
- Check every component in both themes: text 4.5:1 on its ground; 3:1 for text 24px and up, meaningful borders, icons and the focus ring.

### Type

Three families: `--font-display` Archivo Expanded for headlines (700, sentence case, −0.01em); `--font-sans` Red Hat Text for body and UI; `--font-mono` DM Mono for IDs, data, labels, buttons and keys.

| Style | Family | Size / line | Weight | Tracking | Use |
|---|---|---|---|---|---|
| `display-xl` | display | 64 / 1 | 700 | −0.01em | Hero headline |
| `display-l` | display | 48 / 1.02 | 700 | −0.01em | Page headline |
| `display-m` | display | 36 / 1.05 | 700 | −0.005em | Section headline |
| `title-l` | display | 22 / 1.15 | 600 | 0 | Card and panel titles in the brand face |
| `title-m` | sans | 20 / 1.3 | 600 | −0.01em | Dialog and drawer titles |
| `title-s` | sans | 16 / 1.35 | 600 | −0.005em | Card titles in the body face |
| `body-l` | sans | 16 / 1.55 | 400 | 0 | Lead paragraphs |
| `body` | sans | 14 / 1.5 | 400 | 0 | Default UI text |
| `body-s` | sans | 13 / 1.45 | 400 | 0 | Dense UI, table cells, captions |
| `label` | mono | 11 / 1 | 500 | 0.08em | Labels and buttons, capitals |
| `label-s` | mono | 10 / 1 | 500 | 0.09em | Inline data keys and table headers, capitals |
| `mono` | mono | 13 / 1.5 | 400 | 0 | IDs, commands, digests |
| `mono-s` | mono | 12 / 1.45 | 400 | 0 | Inline data values, durations |
| `data` | mono | 13 / 1.3 | 500 | 0 | Numbers in tables and readouts, tabular |

- Use the display face for headlines (`title-l` and up) and for product names beside their marks. Never set body, data or labels in it.
- Set labels, buttons, keys and table headers in `label` or `label-s`, in capitals.
- Set every number with tabular figures (`font-variant-numeric: tabular-nums`; built into `af-num`, `af-mono`, `af-meta__val` and `af-readout`).
- Never set body copy in mono or labels in sans. Emphasize with `fg` against `fg-muted`, not italics.
- Each style compiles to a class of the same name in tokens.css (`.display-l`, `.body-s`, `.label`).

### Spacing and layout

- Space on a 4px base: `space-2`, `-4`, `-8`, `-12`, `-16`, `-20`, `-24`, `-28`, `-32`, `-40`, `-48`, `-64`, `-104`, `-160`.
- Pad cards with `space-16` (airy: `space-24`). Gap card grids by `space-12` and blocks by `space-28`. Gutter pages by `space-32` on desktop and `space-16` on phones. Pad sections with `space-64` (compact `space-48`, marketing `space-104`, hero top `space-160`).
- Cap content at `container-max` (1280px). The app header is `header-h` (56px).
- Rows are `row-h` (32px; dense tables `row-h-compact`, 28px). Session lanes are `lane-h` (30px), trace spans `span-h` (28px).
- Put `space-8` between an icon and its label and `space-4` between fleet tiles.

### Radius

- `radius-control` (2px): buttons, inputs, chips, tags, fleet tiles, the denied placard, product mark tiles.
- `radius-card` (4px): cards and panels.
- `radius-none`: tables, lanes, trace bars.
- `radius-round`: status dots and avatars. Nothing else is round; there are no pills.

### Borders and dividers

- Cards and panels have no border.
- Inside a card, divide rows and the footer (`af-card__foot`) with `line-subtle`. Rule under a table header with `line`.
- Border controls with 1px `line-strong`: inputs, secondary buttons, switches, product mark tiles.
- Rule sections that sit on the canvas with `rule`.
- Mark a card that needs a person with `af-card--lit` (a 1px inset `status-approval` ring and a faint tint). Never use a colored left border.
- Never box a table, list or chart inside a card, and never double a line.

### Cards are tonal

- Put content on `af-card` (padded, `raised`, `radius-card`) or `af-panel` (unpadded, for tables, lanes and traces).
- Separate cards by tone and `space-12`, not borders. Never nest `raised` in `raised`; for a well inside a card use `surface` or `display-window`.
- Cards cast no shadow. `shadow-overlay` is for menus and popovers only.

### Texture

- Use two textures and nothing else.
- **Dot field.** Small dots on an 8px pitch in `dot-field`, behind hero data only, once per page at most.
- **Hatching.** 135° stripes in `status-approval` for time spent waiting on a human, in lanes and trace spans.
- No gradients, noise, grain, glow, blur, gloss or background images.

### Motion

- Transition color, background, border and opacity over `--af-dur` (160 ms) with `--af-ease` (`cubic-bezier(.2,0,0,1)`). Buttons press to `scale(.98)` in 90 ms.
- No bounce, springs, overshoot, parallax, pulsing or blinking. A status never animates to get attention; its color and shape do that.
- `prefers-reduced-motion: reduce` switches all transitions and animations off (base.css). Never override it.

### Focus

- Show `:focus-visible` on every interactive element as a 2px solid `focus` outline, offset 2px; base.css sets it globally. `focus` is yellow in Night (13:1 on `canvas`) and dark gold in Day (5.5:1).
- Never remove the outline. Inset it (`outline-offset: -2px`) only where an offset ring would be clipped, as in dense rows.

## Iconography

- Use the Airframe icon set only: custom, drawn on a 20 px grid, stroke-only, `--icon-stroke` 1.5, square caps, miter joins, `fill: none`, `stroke: currentColor`. No icon fonts, no third-party sets, no emoji.
- Markup: `<svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg>`. Default size is 16px (`icon-size`); use `af-ic--14` in small buttons, `af-ic--20` in nav and headers, `af-ic--24` for empty states.
- Color icons with text tokens: `fg-subtle` beside a label, `fg` when active, `brand-text` when selected. An icon takes a status color only when it is that status's mark.
- Pair icons with a word wherever space allows. An icon-only button needs an `aria-label`.
- The `agent` glyph replaced the Lab's aircraft silhouette: agents are not airplanes. Aviation lives in the words and the logic (dark cockpit, tail numbers, master caution), never in pictures of aircraft.
- Files: one SVG per icon in `icons/<name>.svg`, the sprite `icons/airframe-icons.svg` and the index `icons/icons.json`. On this page, see the Icons component.

## How to consume

Airframe lives in [Sean-Koval/agent-factory](https://github.com/Sean-Koval/agent-factory): this folder is the source, `theme/` is what tools load. Tool repos vendor the `theme/` files at a `theme-vN` tag with their own `scripts/sync-airframe.sh` and never edit them.

1. Load `airframe.css`: every token as `--af-<name>`. It is generated from `tokens.json`; never edit it by hand. Night values sit under `:root, [data-theme="dark"]`, Day under `[data-theme="light"]` (and the OS light preference when no theme is pinned); spacing, radius, layout, icon, font tokens and `--af-font-display`, `--af-font-sans`, `--af-font-mono` sit on `:root`.
2. Load `airframe-components.css`: the font import, the `.af-type-<style>` classes, then `base.css`, `core.css` and `viz.css`.
3. Headlines use `font-family: var(--af-font-display); font-stretch: var(--af-display-stretch)`. Google serves Archivo as one variable family with a width axis; the stretch gives Archivo Expanded.
4. Set `data-theme="dark"` or `data-theme="light"` on `<html>` (or on any element, for a nested scope).
5. Build with the `af-` classes (BEM: `af-card__foot`, `af-btn--primary`). For anything new, use tokens as `var(--af-<name>)`; never hard-code a color, size or font.

```html
<html data-theme="dark">
<head>
  <link rel="stylesheet" href="airframe/airframe.css">
  <link rel="stylesheet" href="airframe/airframe-components.css">
</head>
<body>
  <article class="af-card">
    <div class="af-card__top">
      <span class="af-lbl">Sandbox<span class="af-lbl__sub">us-east4</span></span>
      <span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span>
    </div>
    <span class="af-id">HGR-3MX9</span>
    <span class="af-meta">
      <span class="af-meta__item af-meta__item--approval"><span class="af-meta__key">Policy</span><span class="af-meta__val">require-approval-main-push</span></span>
      <span class="af-meta__item"><span class="af-meta__key">Harness</span><span class="af-meta__val">codex</span></span>
    </span>
    <div class="af-card__foot"><span>Held <b>41 min</b></span><button class="af-btn af-btn--primary af-btn--sm">Review</button></div>
  </article>
</body>
</html>
```
