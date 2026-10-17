# Contracts

The tools meet only at versioned files and APIs. Each row links to the repo that defines the contract; this page indexes them and never copies their schemas.

| Producer → consumer | Contract | Defined in | Status |
| --- | --- | --- | --- |
| ai-dlc → team harness repo → hangar | Workflow plugin with `plugin.lock.json`, pinned in a harness lock as `plugin:ai-dlc-workflow@sha256:…` | [ai-dlc #191](https://github.com/Sean-Koval/ai-dlc/issues/191), [hangar #139](https://github.com/Sean-Koval/hangar/issues/139) | Plugin in review |
| Team harness repo → hangar | `harness.lock` plus native files; its digest equals the manifest's `harness_digest` | hangar spec 0014 §2, `docs/api/harness-lock.schema.json` | Freeze and thaw in review |
| hangar → Claude Code sandboxes | Read-only plugin seed, `enabledPlugins`, auto-update off, plugins listed in the manifest | [hangar #136](https://github.com/Sean-Koval/hangar/issues/136) | In review |
| hangar canary → hangar, ai-dlc | `harnesses.lock.yaml`: CLI version and checksum per harness | hangar `src/hangar/harnesses.lock.yaml` | On main |
| hangar → flightdeck, workspace | `hangar.manifest/v1`: what ran, with `config_digest`, `harness_digest`, `environment_digest` | hangar [`docs/api/manifest.schema.json`](https://github.com/Sean-Koval/hangar/tree/main/docs/api) | On main |
| hangar → flightdeck, workspace | `hangar.trace/v1`: OTLP spans with `hangar.tool.kind`, `hangar.shell.ops`, taint and outcome class | hangar [`docs/api/traces.md`](https://github.com/Sean-Koval/hangar/tree/main/docs/api) | On main |
| flightdeck → hangar | `hangar.experiment/v1`: tasks × variants × trials, pinned, with sealed graders | hangar `docs/api/experiment.schema.json` | On main; client in review |
| hangar outbox → flightdeck | `hangar.run/v1` objects under `v1/runs/{date}/{session}.{run}/`; `run.json` is written last and marks the run complete | hangar `docs/api/outbox.md` | In review |
| flightdeck internal | `flightdeck.parquet/v1`: runs, spans, events, manifests, grades, test cases, spec results | flightdeck [`docs/data-plane.md`](https://github.com/Sean-Koval/flightdeck/tree/main/docs) | On main |
| Team repos → flightdeck | Behavior specs `flightdeck.spec/v1` and ADR `checks:`, judged nightly | flightdeck `docs/behavior-specs.md`, [ai-dlc #207](https://github.com/Sean-Koval/ai-dlc/issues/207) | In review |
| hangar ↔ workspace | `hangar.decision/v1`: five kinds (`job.release`, `tool.call`, `landing.approve`, `egress.request`, `secret.request`); allow, deny or wait plus a receipt; fails closed; off → shadow → enforce | hangar spec 0015 | Spec in review |
| workspace → hangar | HMAC-signed events to one route, `/api/governance/events`; hangar re-reads the decision | spec 0015, [workspace #17](https://github.com/Sean-Koval/governed-agent-workspace/issues/17) | Planned |
| hangar sandbox → workspace | Passport: workload token exchanged under RFC 8693 for a 15-minute passport with the requester as subject | workspace `aw/workload.py`, [hangar #174](https://github.com/Sean-Koval/hangar/issues/174) | Exchange on main; hangar side planned |
| workspace → auditors and PRs | Hash-chained receipts; an attestation envelope with digests, model and approver | workspace `aw/audit.py`, [workspace #18](https://github.com/Sean-Koval/governed-agent-workspace/issues/18) | Chain on main; envelope planned |
| hangar → reviewers | Review packet on each PR; `Harness-Digest:` trailer | hangar `landing.py`, [hangar #137](https://github.com/Sean-Koval/hangar/issues/137) | Packet on main; trailer planned |
| hangar → engineers | Inbox items (review, question, approval, failed), delivered to Slack | hangar `inbox.py`, [#157](https://github.com/Sean-Koval/hangar/issues/157), [#158](https://github.com/Sean-Koval/hangar/issues/158) | List on main; delivery planned |
| Spaceport → agents | Four MCP tools with typed results | spaceport `gateway/mcp/server.py` | On main, frozen |
