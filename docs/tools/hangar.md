<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-hangar); }</style>

<span class="af-eyebrow">Agent factory · Run</span>

# hangar

Runs coding agents in isolated cloud sandboxes, from a ticket to a landed PR.

<figure class="af-figure af-figure--lead">
<a href="../assets/captures/hangar-needs-you.png"><img src="../assets/captures/hangar-needs-you-narrow-decision.png#only-dark" alt="hangar's Needs you: the decision deck with a held git push to main on top, its changes, branch and expiry, Deny, Allow for this turn and Approve push" width="720" height="586"></a>
<a href="../assets/captures/hangar-needs-you-day.png"><img src="../assets/captures/hangar-needs-you-narrow-day-decision.png#only-light" alt="hangar's Needs you: the decision deck with a held git push to main on top, its changes, branch and expiry, Deny, Allow for this turn and Approve push" width="720" height="586"></a>
<figcaption>Needs you: one decision at a time, soonest to expire on top. Everything else keeps running.</figcaption>
</figure>

| | |
| --- | --- |
| Owns | Sandboxes, jobs and sessions, the doors, the git gateway and landing, the inbox, the manifest and trace. |
| Does not own | Statistics (flightdeck), harness content (the [team harness repo](../team-harness.md)) or approval policy (Tower). |
| Entry points | MCP server, REST API, the `hangar` CLI, webhooks from GitHub, Jira and Slack. |
| Used by | Engineers who submit and steer work, reviewers, the lead who sets policy, agents through MCP, CI. |
| Status | The safe release, the doors, the inbox, the harness lock and the outbox are shipped; asking Tower is in progress. See [P2 on the roadmap](../roadmap.md#p2-adopt-and-capture). |

[Docs site](https://sean-koval.github.io/hangar/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/hangar){ .md-button }
