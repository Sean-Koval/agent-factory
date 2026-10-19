<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-aidlc); }</style>

<span class="af-eyebrow">Agent factory · Setup</span>

# ai-dlc

Sets up engineers' machines, authors the optional workflow plugin, gates local work on CI.

ai-dlc is the suite's setup, off the agent's hot path. The [team harness repo](../team-harness.md) defines the harness; ai-dlc contributes one optional component to it, its workflow plugin, and prepares engineers' machines ([ADR 0001](https://github.com/Sean-Koval/ai-dlc/blob/main/docs/decisions/0001-refocus-ai-dlc.md)).

| | |
| --- | --- |
| Owns | The `ai-dlc-workflow` Claude Code plugin with its content digest and its Codex form, publishing it into a team harness repo, machine enrollment and bootstrap, the CI-gated work lifecycle, team skills. |
| Does not own | The harness itself (the team harness repo), running agents (hangar), evaluation (moved to flightdeck) or tracker intake (hangar's doors). Linear is not supported. |
| Entry points | The `ai-dlc` CLI, a local MCP server, the plugin. |
| Used by | Each engineer on their own machine, CI, and the team harness repo, which pins the plugin. |
| Status | **Shipped:** the workflow plugin and its Codex form ([#191](https://github.com/Sean-Koval/ai-dlc/issues/191), [#193](https://github.com/Sean-Koval/ai-dlc/issues/193)), hooks that work without the CLI ([#192](https://github.com/Sean-Koval/ai-dlc/issues/192)), the ADR `checks:` convention ([#207](https://github.com/Sean-Koval/ai-dlc/issues/207)), `ai-dlc eval` moved to flightdeck ([#195](https://github.com/Sean-Koval/ai-dlc/issues/195)). **In progress:** the refocus epic ([#189](https://github.com/Sean-Koval/ai-dlc/issues/189)) and its docs sweep ([#208](https://github.com/Sean-Koval/ai-dlc/issues/208)). Features outside ADR 0001's list are frozen. |
| Docs site | Live: [sean-koval.github.io/ai-dlc](https://sean-koval.github.io/ai-dlc/) |

[Docs site](https://sean-koval.github.io/ai-dlc/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/ai-dlc){ .md-button }
