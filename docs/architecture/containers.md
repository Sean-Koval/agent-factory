---
hide:
  - navigation
  - toc
---

# Containers

What runs where: on an engineer's machine, in the Google Cloud project, and outside it. This is C4 level 2. [Architecture](index.md) is the system context above it, and [Contracts](contracts.md) lists the files and APIs these containers meet at.

<figure class="af-figure">
--8<-- "c4-containers.svg"
<figcaption>C4 level 2: the engineer's machine on the left, the Google Cloud project in the middle, outside systems on the right. Solid is on main; dashed is planned or not yet wired. <a href="../assets/diagrams/c4-containers.svg">Full size</a></figcaption>
</figure>

## In the Google Cloud project

### hangar control plane {#hangar-control-plane}

- **Runs on:** GKE, always on
- **Owns:** REST, MCP and web UI; jobs, sessions, intake, landing, inbox; SQLite on a persistent disk
- **Status:** On main

### Git gateway and egress proxy {#git-gateway-and-egress-proxy}

- **Runs on:** The control-plane pod
- **Owns:** Pushes one ref as the GitHub App; the only route from a sandbox to the internet
- **Status:** On main

### Agent sandboxes {#agent-sandboxes}

- **Runs on:** GKE gVisor pool on Spot nodes, 0 to N; optional Kata heavy tier
- **Owns:** Claude Code, Codex, pi and Antigravity sessions; off 01:00–10:00 ET
- **Status:** On main

### Tower {#tower}

- **Runs on:** Beside the control plane, one instance
- **Owns:** Decision point, approvals, receipts, passports
- **Status:** On main: the decision API, events and receipts (Tower#13, #17, #18). Not deployed yet (Tower#28, #52); hangar's wiring is [hangar#172](https://github.com/Sean-Koval/hangar/issues/172)

### Run outbox {#run-outbox}

- **Runs on:** Cloud Storage
- **Owns:** Every finished run written once as `hangar.run/v1`
- **Status:** On main ([hangar#163](https://github.com/Sean-Koval/hangar/issues/163), [PR #214](https://github.com/Sean-Koval/hangar/pull/214)); off in the GKE deploy until [hangar#273](https://github.com/Sean-Koval/hangar/issues/273)

### Compactor {#compactor}

- **Runs on:** Cloud Run job, nightly
- **Owns:** Flattens new runs into `flightdeck.parquet/v1`
- **Status:** On main ([flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5), `deploy/compactor/`); deployed with [hangar#273](https://github.com/Sean-Koval/hangar/issues/273)

## On an engineer's machine

### flightdeck {#flightdeck}

- **Runs on:** An engineer's machine or CI
- **Owns:** Ingest, statistics, behavior specs, reports, experiment submission
- **Status:** On main (v0); the nightly spec runner is [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15)

### ai-dlc {#ai-dlc}

- **Runs on:** An engineer's machine
- **Owns:** Machine setup, local work lifecycle, workflow plugin
- **Status:** On main

Phase by phase progress is on the [Roadmap](../roadmap.md).
