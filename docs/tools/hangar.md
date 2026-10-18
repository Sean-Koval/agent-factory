<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-hangar); }</style>

<span class="af-eyebrow">Run plane</span>

# hangar

Runs coding agents in isolated cloud sandboxes, from a ticket to a landed PR.

| | |
| --- | --- |
| Owns | Sandboxes and environments, harness packs and CLI pins, jobs, sessions and experiment trials, pin sets, the doors (Jira, GitHub, Slack, schedules, webhooks), admission, egress, the git gateway, verify and landing, the inbox, and emitting manifests, traces and outbox records. |
| Does not own | Analysis or statistics (flightdeck), harness content (the [team harness repo](../team-harness.md)), or final approval policy, which moves to Tower. |
| Entry points | MCP server, REST API, the `hangar` CLI, webhooks from GitHub, Jira and Slack. |
| Used by | Engineers who submit and steer work, reviewers, the lead who sets policy and power schedules, agents through MCP, and CI. |
| Status | **Shipped:** the safe release ([#121](https://github.com/Sean-Koval/hangar/issues/121)–[#130](https://github.com/Sean-Koval/hangar/issues/130)), the Jira door and the Slack inbox ([#156](https://github.com/Sean-Koval/hangar/issues/156)–[#158](https://github.com/Sean-Koval/hangar/issues/158)), review-aware admission ([#159](https://github.com/Sean-Koval/hangar/issues/159)), harness lock freeze, check and thaw ([#133](https://github.com/Sean-Koval/hangar/issues/133), [#134](https://github.com/Sean-Koval/hangar/issues/134), [#221](https://github.com/Sean-Koval/hangar/issues/221)), the outbox ([#163](https://github.com/Sean-Koval/hangar/issues/163)), trials and pin sets ([#178](https://github.com/Sean-Koval/hangar/issues/178), [#180](https://github.com/Sean-Koval/hangar/issues/180)), shadows ([#183](https://github.com/Sean-Koval/hangar/issues/183)), the record-mode gateway ([#177](https://github.com/Sean-Koval/hangar/issues/177)). **In progress:** asking Tower ([#172](https://github.com/Sean-Koval/hangar/issues/172), [#173](https://github.com/Sean-Koval/hangar/issues/173), [#190](https://github.com/Sean-Koval/hangar/issues/190)), workload identity ([#174](https://github.com/Sean-Koval/hangar/issues/174)), the team's harness repo ([#138](https://github.com/Sean-Koval/hangar/issues/138), [#139](https://github.com/Sean-Koval/hangar/issues/139)), the outbox and compactor in the GKE deploy ([#273](https://github.com/Sean-Koval/hangar/issues/273)). |
| Docs site | Live: [sean-koval.github.io/hangar](https://sean-koval.github.io/hangar/) |

[Docs site](https://sean-koval.github.io/hangar/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/hangar){ .md-button }
