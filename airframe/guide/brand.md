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

## Where each rule lives

Each page answers one question.

- <span id="content-fundamentals"></span><span id="voice"></span><span id="casing"></span><span id="example-copy"></span><span id="words-to-avoid"></span>**[Writing](Writing.md)**: how do I write for these products? Voice, casing, example copy and words to avoid.
- <span id="tail-number-ids"></span><span id="numbers-and-units"></span>**[IDs and numbers](IDs.md)**: how do I show an ID, a number or a unit? Tail numbers, units, ratios and money.
- <span id="visual-foundations"></span><span id="color-roles"></span><span id="the-brand-is-never-a-status"></span><span id="night-and-day"></span>**[Color](Color.md)**: which color goes where? Color roles, the brand that is never a status, Night and Day.
- <span id="who-has-the-controls"></span><span id="actors-the-avatar-triad"></span>**[People and agents](People.md)**: how do people and agents appear? Who has the controls, and the avatar triad.
- <span id="type"></span>**[Type](Type.md)**: which face, size and weight? Three families and one scale.
- <span id="spacing-and-layout"></span><span id="radius"></span><span id="borders-and-dividers"></span><span id="cards-are-tonal"></span><span id="texture"></span>**[Layout](Layout.md)**: how is a screen spaced and shaped? Spacing, radius, borders, tonal cards and texture.
- <span id="motion"></span><span id="focus"></span>**[Motion and focus](Motion.md)**: how do things move, and how does focus show?
- <span id="iconography"></span>**[Iconography](Iconography.md)**: which icons, at what size and in what color?
- <span id="how-to-consume"></span>**[How to consume](Consume.md)**: how does a tool load Airframe?
- **[Status](Status.md)**: the six statuses, their marks and the decision words.
- **[Data](Data.md)**: tables, inline data, readouts, traces, lanes and charts.
- **[Products](Products.md)**: each product's mark, hue and nav marker.

## Principles

1. **Dark cockpit: quiet until a human is needed.** Normal is grey. Running is a quiet `status-running` circle; nothing turns green, glows or blinks. Color appears only for needs approval (`status-approval`), failed (`status-failed`) and denied (`status-denied`). A screen with no color on it means nobody is needed.
2. **One hot color.** Signal yellow (`brand`) marks what is yours: the primary action, the focus ring, the trace critical path, the now line, the selected mark. Use one primary button per view. Yellow never means a state.
3. **Tonal, not boxed.** Separate by tone and space, not lines. Cards are `raised` on `canvas` with no border; dividers inside them are `line-subtle`.
4. **Data first.** Show the real ID, the real number, the real policy name. Set data in DM Mono with tabular figures and let chrome recede.
5. **Soft, never glossy.** 8px controls, 12px cards, an 18px sheet, 1px lines. One step of lift (`lifted`) for what is open or on top, with a shadow; resting cards cast none. No gloss, blur, gradients or noise. The one glow is the rail head and the latest timeline dot, and it means "moving".
6. **Attention is edge, mark, word.** A thing that needs a person keeps a neutral ground and shows a 3px status edge on its leading side, the status mark and the word. No status color is ever mixed into a surface; selection is neutral, so yellow never sits around orange.
