---
hide:
  - navigation
  - toc
---

# Containers

C4 level 2: what runs on an engineer's machine, in the Google Cloud project and outside it, and which seams are on main. [Architecture](index.md) has the system context above this view; [Contracts](contracts.md) indexes the files and APIs the containers meet at.

<figure class="af-figure">
--8<-- "c4-containers.svg"
<figcaption>C4 level 2 · solid: on main · dashed: planned or not yet wired · <a href="../../assets/diagrams/c4-containers.svg">full size</a></figcaption>
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
