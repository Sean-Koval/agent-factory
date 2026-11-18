<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-tower); }</style>

<span class="af-eyebrow">Agent factory · Govern</span>

# Tower

One decision point for risky actions: rules, human approvals, signed receipts.

<figure class="af-figure af-figure--lead">
<a href="../assets/captures/tower-desk.png"><img src="../assets/captures/tower-desk-approval.png#only-dark" alt="Tower's Desk for an approver: approval TWR-APR-A5T2 to create a ticket for Globex, what will run, the risk, what approving does, Deny and Approve" width="656" height="588"></a>
<a href="../assets/captures/tower-desk-day.png"><img src="../assets/captures/tower-desk-day-approval.png#only-light" alt="Tower's Desk for an approver: approval TWR-APR-A5T2 to create a ticket for Globex, what will run, the risk, what approving does, Deny and Approve" width="656" height="588"></a>
<figcaption>Needs you on the Desk: an agent wants to create a client ticket, and what approving does is explained before the button.</figcaption>
</figure>

!!! note "Status"
    The decision API, signed events, attestation receipts and passports for `/mcp` are shipped; hangar's wiring and a deployment beside it are next. See the [roadmap](../roadmap.md).

## What Tower owns

Tower is the team's governance plane for the coding agents hangar runs and the vendor agents the team uses. hangar runs the agents; Tower clears risky actions. It was the governed workspace until its owner named it Tower (Tower ADR 0017).

| | |
| --- | --- |
| Owns | Cedar rules, approvals (approver never the requester), passports, hash-chained receipts, reconciliation, an inbox. |
| Does not own | Enforcement inside sandboxes or landing mechanics. Tower decides; hangar enforces. |
| Entry points | The REST decision API `POST /v1/decisions`, an MCP gateway, a Claude Code hook (`/hooks/claude-code`), a web inbox. |
| Used by | Approvers and leads, hangar's decision client, auditors. |
| Docs site | Private repository (Sean-Koval/tower); docs site once public. |

## Watch a push to main get denied

<figure class="af-figure af-figure--lead">
<a href="../assets/clips/tower.mp4"><img src="../assets/clips/tower.png#only-dark" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="816"></a>
<a href="../assets/clips/tower-day.mp4"><img src="../assets/clips/tower-day.png#only-light" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="816"></a>
<figcaption>Play the clip (18 s): a push to main waits on Marcus's Desk, he denies it with a reason, and the receipt in the record carries the reason.</figcaption>
</figure>

## How hangar uses Tower

Hangar enforces; Tower decides. Each of hangar's enforcement points asks Tower one question and keeps doing the rest itself. An allow lets hangar go on with its own checks, never skip them. Anything that fails on the way is a wait or a deny.

### Job intake

- **Asks Tower:** may this untrusted job run? (`hangar.job.release`)
- **Stays in hangar:** the queue, budgets, fairness and the power schedule.

### Driver `ask` turns and the sandbox hook

- **Asks Tower:** may this risky tool call run? (`hangar.tool.call`) The sandbox's Claude Code hook asks `/hooks/claude-code`; a passport for that route is next.
- **Stays in hangar:** taint tracking, and which calls count as risky.

### Egress proxy and secret broker

- **Asks Tower:** may this blocked host or missing secret be granted? (`hangar.egress.request`, `hangar.secret.request`)
- **Stays in hangar:** the proxy, NetworkPolicy, the git gateway and intake posture.

### Landing

- **Asks Tower:** does this approval of this head land it? (`hangar.landing.approve`)
- **Stays in hangar:** auto-merge, SHA pinning, the stale-gate and branch protection.

### Rolling it out

Each kind rolls out on its own, through three modes:

1. `off`: hangar's own rules decide. This is the default.
2. `shadow`: hangar's rules still decide, Tower answers dry runs, and disagreements are counted.
3. `enforce`: Tower's answer decides.

The contract is `hangar.decision/v1`, in hangar's [spec 0015](https://github.com/Sean-Koval/hangar/blob/main/docs/specs/0015-governance-decision-point.md).

## Works with

- **[hangar](hangar.md).** hangar's decision client asks at the four enforcement points above, and fails closed.
- **[Spaceport](spaceport.md).** Frozen; asking Tower's decision point waits in its backlog.
- **[Contracts](../architecture/contracts.md).** The decision, event, passport and receipt contracts, with who produces and consumes each.

[How it fits](../how-it-fits.md) follows one ticket through all four planes.
