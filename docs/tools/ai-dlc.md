<style>:root, [data-md-color-scheme] { --af-product: var(--af-product-aidlc); }</style>

<span class="af-eyebrow">Define plane</span>

# ai-dlc

Authors the team's workflow plugin, provisions developer machines and gates local work on CI.

| | |
| --- | --- |
| Owns | The `ai-dlc-workflow` Claude Code plugin with its content digest, machine enrollment and bootstrap, the CI-gated work lifecycle, team skills. |
| Does not own | Running agents (hangar), evaluation (moved to flightdeck) or tracker intake (hangar's doors). Linear is not supported. |
| Entry points | The `ai-dlc` CLI, a local MCP server, the plugin. |
| Used by | Each engineer on their own machine, and CI. |

[Docs site](https://sean-koval.github.io/ai-dlc/){ .md-button .md-button--primary } [Repository](https://github.com/Sean-Koval/ai-dlc){ .md-button }
