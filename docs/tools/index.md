# Tools

Five tools and the team harness repo. hangar, flightdeck and Tower each own a plane; the team harness repo is the Define plane; ai-dlc contributes the optional workflow plugin to it; Spaceport is a frozen capability. hangar, flightdeck and ai-dlc are public and have docs sites in the same theme. Tower and Spaceport are private repositories for now.

| Tool | Plane | In one line | Status | Docs site |
| --- | --- | --- | --- | --- |
| [hangar](hangar.md) | Run | Runs coding agents in isolated cloud sandboxes, from a ticket to a landed PR. | Shipped; asking Tower in progress | [Live](https://sean-koval.github.io/hangar/) |
| [flightdeck](flightdeck.md) | Judge | Judges harness changes with paired statistics and behavior specs over every run. | v0 shipped; one real decision next | [Live](https://sean-koval.github.io/flightdeck/) |
| [Tower](workspace.md) | Govern | One decision point for risky actions: rules, human approvals, signed receipts. | Decision API shipped; passports and inbox next | Private |
| [Team harness](../team-harness.md) | Define | The harness as native files and a lock, frozen from a good run and promoted on evidence. | Example shipped; the team's repo next | [README](https://github.com/Sean-Koval/team-harness) |
| [ai-dlc](ai-dlc.md) | Supports Define | Authors the optional workflow plugin, provisions machines, gates local work on CI. | Plugin shipped; refocus docs in progress | [Live](https://sean-koval.github.io/ai-dlc/) |
| [Spaceport](spaceport.md) | Capability | Reviewed data products that agents query through four MCP tools. Frozen. | Frozen | None (README only) |

Each tool page lists what it owns, what it doesn't, and the issues behind its status.
