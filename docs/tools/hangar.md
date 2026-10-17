<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-hangar); }</style>

<span class="af-eyebrow">Run plane</span>

# hangar

The team's runtime and control plane for cloud coding agents, from intake to a landed pull request.

| | |
| --- | --- |
| Owns | Sandboxes and environments, harness packs and CLI pins, jobs, sessions and experiment trials, the doors (Jira, GitHub, Slack, schedules, webhooks), admission, egress, the git gateway, verify and landing, the inbox, and emitting manifests, traces and outbox records. |
| Does not own | Analysis or statistics (flightdeck), harness authoring (ai-dlc and the team harness repo), or final approval policy, which moves to Tower. |
| Entry points | MCP server, REST API, the `hangar` CLI, webhooks from GitHub, Jira and Slack. |
| Used by | Engineers who submit and steer work, reviewers, the lead who sets policy and power schedules, agents through MCP, and CI. |

[Docs site](https://sean-koval.github.io/hangar/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/hangar){ .md-button }
