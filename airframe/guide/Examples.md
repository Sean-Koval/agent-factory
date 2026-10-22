# What each product calls its statuses

## Examples by product

Keep the role; specialize the word only when it says more. The shape and color never change.

- **hangar.** `HGR-7Q2K` Running a turn. `HGR-5JD2` Queued for a slot in base-codex. `HGR-3MX9` Holding at PR (approval role): push to main held by `require-approval-main-push`. `HGR-0PZ4` Failed at test. `HGR-9KD4` Denied: egress blocked by policy. `HGR-1WQ8` Spun down (off role) when the pool went down at 01:00.
- **flightdeck.** `FDK-EXP-0142` Running, evaluating 9 behavior checks. Queued for a runner. Needs approval: promotion waits for an approver who is not the author. Failed: a behavior check failed or the run crashed. Denied: the author tried to approve their own promotion. Archived (off role).
- **Tower.** Active (running role): passport in force. Queued: request awaiting evaluation. `TWR-APR-0391` Needs approval. Failed: the decision point could not evaluate. Denied by `deny-secrets-egress`, no receipt issued. Expired (off role): passport lapsed. Every decided request links its receipt, `TWR-RCPT-88A1`.
- **ai-dlc.** The CLI prints the same shapes as glyphs: `●` running, `○` queued, `◆` needs approval, `▲` failed, `[DENIED]`, `·` off. The glyph carries the meaning without color; color only the lit three (`◆` orange, `▲` and `[DENIED]` red).
- **Spaceport.** Refreshing (running role). Queued. Needs approval: a schema change waits for the owner. Failed: the refresh failed. Denied: access request refused. Deprecated (off role).

Write the reason next to every lit status as keyed inline data: `Policy require-approval-main-push`, `Stage test`, `Held 41 min`.

Part of [Status](Status.md), a chapter of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
