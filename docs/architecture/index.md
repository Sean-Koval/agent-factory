# Architecture

The suite follows the [C4 model](https://c4model.com/): a system context view for who uses it and what it depends on, then a container view for what runs where. Both diagrams follow the page's light or dark theme; PNGs for slides are in [`docs/assets/diagrams`](https://github.com/Sean-Koval/agent-factory/tree/main/docs/assets/diagrams).

## System context

<figure class="af-figure">
--8<-- "c4-context.svg"
<figcaption>C4 level 1 · people, the suite and the systems around it · <a href="../assets/diagrams/c4-context.svg">full size</a></figcaption>
</figure>

Four kinds of people use the suite. **Engineers** hand off work and answer questions. **Reviewers** approve the exact commit that lands. The **harness owner** runs experiments and promotes the team harness. **Approvers** decide risky actions. The suite depends on GitHub for code and review, Jira and Slack as doors, model providers through API keys only, Google Cloud to run on, and MCP servers for the tools agents call.

## Containers

<figure class="af-figure">
--8<-- "c4-containers.svg"
<figcaption>C4 level 2 · solid: on main · dashed: in review or planned · <a href="../assets/diagrams/c4-containers.svg">full size</a></figcaption>
</figure>

| Container | Runs on | Owns | Status |
| --- | --- | --- | --- |
| hangar control plane | GKE, always on | REST, MCP and web UI; jobs, sessions, intake, landing, inbox; SQLite on a persistent disk | On main |
| Git gateway and egress proxy | The control-plane pod | Pushes one ref as the GitHub App; the only route from a sandbox to the internet | On main |
| Agent sandboxes | GKE gVisor pool on Spot nodes, 0 to N; optional Kata heavy tier | Claude Code, Codex, pi and Antigravity sessions; off 01:00–10:00 ET | On main |
| Governed workspace | Beside the control plane, one instance | Decision point, approvals, receipts, passports | Planned ([spec 0015](https://github.com/Sean-Koval/hangar/pull/208)) |
| Run outbox | Cloud Storage | Every finished run written once as `hangar.run/v1` | In review ([hangar #214](https://github.com/Sean-Koval/hangar/pull/214)) |
| Compactor | Cloud Run job, nightly | Flattens new runs into `flightdeck.parquet/v1` | Planned ([flightdeck #5](https://github.com/Sean-Koval/flightdeck/issues/5)) |
| flightdeck | An engineer's machine or CI | Ingest, statistics, behavior specs, reports, experiment submission | On main, slice in review |
| ai-dlc | An engineer's machine | Machine setup, local work lifecycle, workflow plugin | On main |

## The planes

| Plane | Tool | Decides | Never does |
| --- | --- | --- | --- |
| Define | ai-dlc and the team harness repo | What a harness is: native files, a lock, a digest | Run anything |
| Run | hangar | Where work runs and how it reaches a branch | Analyse runs or set approval policy |
| Judge | flightdeck | Whether a change made agents better, with intervals | Run sandboxes or hold credentials |
| Govern | Governed workspace | Whether a risky action may happen | Enforce inside a sandbox |
| Capability | MCP servers, Spaceport | What data and tools agents can reach | Decide policy for agents |
