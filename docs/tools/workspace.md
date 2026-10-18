<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-tower); }</style>

<span class="af-eyebrow">Govern plane</span>

# Tower

The team's governance plane: one decision point for risky actions, with human approvals and signed receipts.

| | |
| --- | --- |
| Owns | Cedar rules, approvals where the approver is never the requester, RFC 8693 passports, hash-chained receipts, reconciliation of tool calls against receipts, an approvals inbox. |
| Does not own | Enforcement inside sandboxes or landing mechanics. Tower decides; hangar enforces. |
| Entry points | A REST decision API (planned, spec 0015), an MCP gateway, a Claude Code hook, a web inbox. |
| Used by | Approvers and leads, hangar's decision client, auditors. |

[Repository](https://github.com/Sean-Koval/tower){ .md-button }
