<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-tower); }</style>

<span class="af-eyebrow">Agent factory · Govern</span>

# Tower

One decision point for risky actions: rules, human approvals, signed receipts.

<figure class="af-figure af-figure--lead">
<a href="../assets/captures/tower-desk.png"><img src="../assets/captures/tower-desk-approval.png#only-dark" alt="Tower's Desk for an approver: approval TWR-APR-0102 to create a ticket for Globex, what will run, the risk, what approving does, Deny and Approve" width="656" height="588"></a>
<a href="../assets/captures/tower-desk-day.png"><img src="../assets/captures/tower-desk-day-approval.png#only-light" alt="Tower's Desk for an approver: approval TWR-APR-0102 to create a ticket for Globex, what will run, the risk, what approving does, Deny and Approve" width="656" height="588"></a>
<figcaption>Needs you on the Desk: an agent wants to create a client ticket, and what approving does is explained before the button.</figcaption>
</figure>

Tower is the team's governance plane for the coding agents hangar runs and the vendor agents the team uses. hangar runs the agents; Tower clears risky actions. It was the governed workspace until its owner named it Tower (Tower ADR 0017).

| | |
| --- | --- |
| Owns | Cedar rules, approvals (approver never the requester), passports, hash-chained receipts, reconciliation, an inbox. |
| Does not own | Enforcement inside sandboxes or landing mechanics. Tower decides; hangar enforces. |
| Entry points | The REST decision API `POST /v1/decisions`, an MCP gateway, a Claude Code hook (`/hooks/claude-code`), a web inbox. |
| Used by | Approvers and leads, hangar's decision client, auditors. |
| Status | The decision API, signed events, attestation receipts and passports for `/mcp` are shipped; hangar's wiring and a deployment beside it are next. See the [roadmap](../roadmap.md). |
| Docs site | Private repository (Sean-Koval/tower); docs site once public. |

<figure class="af-figure af-figure--lead">
<a href="../assets/clips/tower.mp4"><img src="../assets/clips/tower.png#only-dark" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="816"></a>
<a href="../assets/clips/tower-day.mp4"><img src="../assets/clips/tower-day.png#only-light" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="816"></a>
<figcaption>Play the clip (18 s): a push to main waits on Marcus's Desk, he denies it with a reason, and the receipt in the record carries the reason.</figcaption>
</figure>

## How hangar uses Tower

Hangar enforces; Tower decides. Each of hangar's enforcement points asks Tower one question and keeps doing the rest itself. An allow lets hangar go on with its own checks, never skip them. Anything that fails on the way is a wait or a deny.

| Hangar enforcement point | What it asks Tower | What stays in hangar |
| --- | --- | --- |
| Job intake | May this untrusted job run? (`hangar.job.release`) | The queue, budgets, fairness, the power schedule |
| Driver `ask` turns and the sandbox hook | May this risky tool call run? (`hangar.tool.call`; the sandbox's Claude Code hook asks `/hooks/claude-code`, with a passport once Tower#14 lands) | Taint tracking, and which calls count as risky |
| Egress proxy and secret broker | May this blocked host or missing secret be granted? (`hangar.egress.request`, `hangar.secret.request`) | The proxy, NetworkPolicy, the git gateway, intake posture |
| Landing | Does this approval of this head land it? (`hangar.landing.approve`) | Auto-merge, SHA pinning, the stale-gate, branch protection |

Each kind rolls out on its own: `off` (hangar's own rules, the default), then `shadow` (Tower answers dry runs and disagreements are counted), then `enforce`. The contract is `hangar.decision/v1`, in hangar's [spec 0015](https://github.com/Sean-Koval/hangar/blob/main/docs/specs/0015-governance-decision-point.md).
