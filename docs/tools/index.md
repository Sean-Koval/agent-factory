# Tools

Four planes, five tools and the team harness repo. The team harness is Define, hangar is Run, flightdeck is Judge and Tower is Govern. ai-dlc is Setup, off the agent's hot path, and Spaceport sits under the suite as a frozen data capability.

hangar, flightdeck and ai-dlc are public and have docs sites in the same theme. Tower and Spaceport are private repositories for now.

<div class="af-cards-table" markdown>

| Tool | Plane | In one line | Status | Docs site |
| --- | --- | --- | --- | --- |
| [Team harness](../team-harness.md) | Define | The harness as native files and a lock, frozen from a good run and promoted on evidence. | Example shipped; the team's repo next | [README](https://github.com/Sean-Koval/team-harness) |
| [hangar](hangar.md) | Run | Runs coding agents in isolated cloud sandboxes, from a ticket to a landed PR. | Shipped; asking Tower in progress | [Live](https://sean-koval.github.io/hangar/) |
| [flightdeck](flightdeck.md) | Judge | Judges harness changes with paired statistics and behavior specs over every run. | v0 shipped; one real decision next | [Live](https://sean-koval.github.io/flightdeck/) |
| [Tower](workspace.md) | Govern | One decision point for risky actions: rules, human approvals, signed receipts. | Decision API shipped; passports and inbox next | Private |
| [ai-dlc](ai-dlc.md) | Setup | Sets up engineers' machines, authors the optional workflow plugin, gates local work on CI. | Plugin shipped; refocus docs in progress | [Live](https://sean-koval.github.io/ai-dlc/) |
| [Spaceport](spaceport.md) | Capability | Reviewed data products that agents query through four MCP tools. | Frozen | None (README only) |

</div>

Each tool page shows the product, then what it owns, what it doesn't, and where its status lives on the [roadmap](../roadmap.md).
