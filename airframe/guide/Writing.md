# Writing

How to write for the five products: the voice, the casing, example copy and the words to avoid.

## Voice

- Write short, plain, specific sentences: what happened, to what, and what is needed. "HGR-3MX9 is holding at PR. Push to main needs your approval."
- Let numbers be the proof: "38 of 41 passed", not "most tests passed".
- Speak as the system, in statements. Address the reader as "you" only when they must act ("Waiting on you"). Never "we" or "I".
- Use aviation terms only where they clarify: hold, cleared, spun down, on approach. Never cute.
- Write real content only: no lorem ipsum, no invented praise, no filler stats. No emoji, no exclamation marks.

## Casing

- Sentence case for headlines, titles, body, menu items and status words: "Forty agents. One needs you.", "Needs approval".
- Sentence-case sans for labels, buttons, keys, tabs, table headers and stage words too (`af-lbl`, `af-btn`, `af-meta__key`, `label`, `label-s`). Mono capitals were retired in theme-v12: they made every screen read as a terminal printout. Mono stays for what *is* a code: IDs (`af-id`), numbers, commands, model and policy names, the denied placard, the lamp legend and the terminal bar.
- Product names keep their case everywhere, even at the start of a sentence: hangar, flightdeck, Tower (the governed workspace), ai-dlc, Spaceport, Airframe.
- Policy, branch, model and command names stay exactly as typed: `require-approval-main-push`, `gpt-5.1`, `claude-code@2.1`.

## Example copy

- **hangar.** Headline: "Forty agents. One needs you." Lede: "hangar runs coding agents in isolated cloud sandboxes, holds risky steps for a human, and files a receipt for every decision." Alert: "HGR-3MX9 is holding at PR. Push to main needs your approval." Empty: "No sandboxes running. Start one from an environment." Buttons: Start a sandbox, Snapshot, Fork.
- **flightdeck.** Headline: "Planner prompt v4". Result: "v4 beats v3 on 7 of 9 behavior checks. Tool-call budget regressed 12%." Gate: "Promotion needs an approver who is not the author." Buttons: Promote, Hold.
- **Tower.** Request: "codex wants to push to main. Policy require-approval-main-push holds it for you." Outcome: "Approved by Sean at 14:02. Receipt TWR-RCPT-88A1." Denial: "Denied by policy deny-secrets-egress. No receipt issued." Buttons: Approve, Deny.
- **ai-dlc.** CLI: "Environment base-codex ready in 41 s." Docs: "Map each role to a provider once. Every repo picks it up."
- **Spaceport.** Card: "orders_daily refreshed at 06:00." Gate: "Schema change on orders_daily needs the owner's approval."

## Words to avoid

| Avoid | Write instead |
|---|---|
| simply, just, easy, seamless, effortless | what actually happens |
| powerful, blazing, magic, revolutionary, AI-powered | a number |
| Oops, Uh-oh, Something went wrong | what failed and what to do next |
| Submit, OK, Click here, Please (on buttons) | the verb: Approve, Start a sandbox |
| Error, Warning (alone) | Failed, Needs approval, Denied, plus the reason |
| `a · b · c` metadata strings | keyed inline data (see Data) |
| pilot, captain, takeoff, mayday | hold, cleared, spun down, and only where they clarify |

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
