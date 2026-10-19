# Architecture

The suite follows the [C4 model](https://c4model.com/): a system context view for who uses it and what it depends on, then a container view for what runs where. [How it fits](../how-it-fits.md) follows one ticket through them. Both diagrams follow the page's light or dark theme; PNGs for slides are in [`docs/assets/diagrams`](https://github.com/Sean-Koval/agent-factory/tree/main/docs/assets/diagrams).

## System context

<figure class="af-figure">
--8<-- "c4-context.svg"
<figcaption>C4 level 1 · people, the suite and the systems around it · <a href="../assets/diagrams/c4-context.svg">full size</a></figcaption>
</figure>

Four kinds of people use the suite. **Engineers** hand off work and answer questions. **Reviewers** approve the exact commit that lands. The **harness owner** runs experiments and promotes the team harness. **Approvers** decide risky actions. The suite depends on GitHub for code and review, Jira and Slack as doors, model providers through API keys only, Google Cloud to run on, and MCP servers for the tools agents call.

## Containers

<figure class="af-figure">
--8<-- "c4-containers.svg"
<figcaption>C4 level 2 · solid: on main · dashed: planned or not yet wired · <a href="../assets/diagrams/c4-containers.svg">full size</a></figcaption>
</figure>

| Container | Runs on | Owns | Status |
| --- | --- | --- | --- |
| hangar control plane | GKE, always on | REST, MCP and web UI; jobs, sessions, intake, landing, inbox; SQLite on a persistent disk | On main |
| Git gateway and egress proxy | The control-plane pod | Pushes one ref as the GitHub App; the only route from a sandbox to the internet | On main |
| Agent sandboxes | GKE gVisor pool on Spot nodes, 0 to N; optional Kata heavy tier | Claude Code, Codex, pi and Antigravity sessions; off 01:00–10:00 ET | On main |
| Tower | Beside the control plane, one instance | Decision point, approvals, receipts, passports | On main: the decision API, events and receipts (Tower#13, #17, #18). Not deployed yet (Tower#28, #52); hangar's wiring is [hangar#172](https://github.com/Sean-Koval/hangar/issues/172) |
| Run outbox | Cloud Storage | Every finished run written once as `hangar.run/v1` | On main ([hangar#163](https://github.com/Sean-Koval/hangar/issues/163), [PR #214](https://github.com/Sean-Koval/hangar/pull/214)); off in the GKE deploy until [hangar#273](https://github.com/Sean-Koval/hangar/issues/273) |
| Compactor | Cloud Run job, nightly | Flattens new runs into `flightdeck.parquet/v1` | On main ([flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5), `deploy/compactor/`); deployed with [hangar#273](https://github.com/Sean-Koval/hangar/issues/273) |
| flightdeck | An engineer's machine or CI | Ingest, statistics, behavior specs, reports, experiment submission | On main (v0); the nightly spec runner is [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15) |
| ai-dlc | An engineer's machine | Machine setup, local work lifecycle, workflow plugin | On main |

## The planes

| Plane | Tool | Decides | Never does |
| --- | --- | --- | --- |
| Define | The team harness repo; ai-dlc contributes the optional workflow plugin and machine setup | What a harness is: native files and `harness.lock`, frozen from a good hangar run; one digest | Run anything |
| Run | hangar | Where work runs and how it reaches a branch | Analyse runs or set approval policy |
| Judge | flightdeck | Whether a change made agents better, with intervals | Run sandboxes or hold credentials |
| Govern | Tower | Whether a risky action may happen | Enforce inside a sandbox |
| Capability | MCP servers, Spaceport | What data and tools agents can reach | Decide policy for agents |
