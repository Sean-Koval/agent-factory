# Contracts

Which file or API two tools meet at, where it is defined, and whether it is on main. The tools meet only at these versioned seams. Each entry points to the defining repo and never copies its schema.

Tower and Spaceport are private repositories, so their files and issues are named without links. [How it fits](../how-it-fits.md) shows the same seams along a ticket's journey.

## Define to Run: the harness

### Workflow plugin {#workflow-plugin}

**ai-dlc → team harness repo → hangar.** The plugin with `plugin.lock.json`, pinned in a harness lock as the component `plugin:ai-dlc-workflow@team-harness`. Its digest is the component's own `digest` field.

- **Defined in:** [ai-dlc#191](https://github.com/Sean-Koval/ai-dlc/issues/191), [#193](https://github.com/Sean-Koval/ai-dlc/issues/193), [hangar#221](https://github.com/Sean-Koval/hangar/issues/221)
- **Status:** Plugin and lock support on main; the team's harness turning it on: [hangar#139](https://github.com/Sean-Koval/hangar/issues/139)

### Harness lock: `hangar.harness-lock/v1` {#harness-lock}

**Team harness repo → hangar.** `harness.lock` plus native files and `channels.yaml`. The lock's `harness_digest` is computed the same way as the manifest's.

- **Defined in:** hangar spec 0014 §2, [`docs/harness-lock.md`](https://sean-koval.github.io/hangar/harness-lock/), `docs/api/harness-lock.schema.json`
- **Status:** On main: freeze and check ([hangar#133](https://github.com/Sean-Koval/hangar/issues/133)), thaw with turn-1 drift ([#134](https://github.com/Sean-Koval/hangar/issues/134)), plugin mounts ([#221](https://github.com/Sean-Koval/hangar/issues/221)), a registry by git URL; the team's own repo: [#138](https://github.com/Sean-Koval/hangar/issues/138)

### Plugin seed {#plugin-seed}

**hangar → Claude Code sandboxes.** A read-only plugin seed, `enabledPlugins`, auto-update off, and plugins listed in the manifest.

- **Defined in:** [hangar#136](https://github.com/Sean-Koval/hangar/issues/136)
- **Status:** On main

### CLI lock: `harnesses.lock.yaml` {#cli-lock}

**hangar canary → hangar, ai-dlc.** The CLI version and checksum per harness.

- **Defined in:** hangar `src/hangar/harnesses.lock.yaml`
- **Status:** On main

## Run to Judge: what a run leaves behind

### Manifest: `hangar.manifest/v1` {#manifest}

**hangar → flightdeck, Tower.** What ran, with `config_digest`, `harness_digest` and `environment_digest`.

- **Defined in:** hangar [`docs/api/manifest.schema.json`](https://github.com/Sean-Koval/hangar/tree/main/docs/api)
- **Status:** On main

### Trace: `hangar.trace/v1` {#trace}

**hangar → flightdeck, Tower.** OTLP spans with `hangar.tool.kind`, `hangar.shell.ops`, taint and outcome class.

- **Defined in:** hangar [`docs/api/traces.md`](https://github.com/Sean-Koval/hangar/tree/main/docs/api)
- **Status:** On main; export to Tower's `/v1/traces`: [hangar#176](https://github.com/Sean-Koval/hangar/issues/176)

### Run outbox: `hangar.run/v1` {#run-outbox}

**hangar outbox → flightdeck.** `hangar.run/v1`, `hangar.tests/v1` and `hangar.job_event/v1` objects under `v1/runs/{date}/{session}.{run}/` and `v1/jobs/`. `run.json` is written last and marks the run complete.

- **Defined in:** hangar [`docs/api/outbox.md`](https://sean-koval.github.io/hangar/api/outbox/)
- **Status:** On main ([hangar#163](https://github.com/Sean-Koval/hangar/issues/163)); on in the GKE deploy: [hangar#273](https://github.com/Sean-Koval/hangar/issues/273)

### Parquet store: `flightdeck.parquet/v1` {#parquet-store}

**flightdeck internal.** Runs, spans, events, manifests, grades, test cases and spec results, built nightly by the compactor.

- **Defined in:** flightdeck [`docs/data-plane.md`](https://github.com/Sean-Koval/flightdeck/tree/main/docs)
- **Status:** On main ([flightdeck#4](https://github.com/Sean-Koval/flightdeck/issues/4), [#5](https://github.com/Sean-Koval/flightdeck/issues/5))

### Behavior specs: `flightdeck.spec/v1` {#behavior-specs}

**Team repos → flightdeck.** Behavior specs and ADR `checks:`, judged nightly.

- **Defined in:** flightdeck `docs/behavior-specs.md`, [ai-dlc#207](https://github.com/Sean-Koval/ai-dlc/issues/207)
- **Status:** Spec language on main ([flightdeck#14](https://github.com/Sean-Koval/flightdeck/issues/14)) and the ADR convention ([ai-dlc#207](https://github.com/Sean-Koval/ai-dlc/issues/207)); nightly runner: [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15)

## Judge to Run: experiments

### Experiment: `hangar.experiment/v1` {#experiment}

**flightdeck → hangar.** Tasks × variants × trials, pinned, with sealed graders. hangar records a pin set per variant.

- **Defined in:** hangar `docs/api/experiment.schema.json`
- **Status:** On main ([flightdeck#11](https://github.com/Sean-Koval/flightdeck/issues/11)); lock variants on hangar's side ([hangar#135](https://github.com/Sean-Koval/hangar/issues/135)), not yet sent by flightdeck

### Pin set and trials: `hangar.pinset/v1` {#pin-set-and-trials}

**flightdeck → hangar.** `POST /api/trials {pin_set, task, n, budget}` runs trials against a content-addressed, immutable pin set. flightdeck owns sampling. A trial whose turn 1 drifted ends as `infra_error` / `drift` and is not retried.

The pin set holds `harness_lock` and `harness_digest`, `environment_spec_digest`, `model_id`, each task's `base_sha`, `grader_digest` and `egress_digest`. `environment_digest` and `knowledge_snapshot` are optional.

- **Defined in:** hangar [`docs/api/trials.md`](https://sean-koval.github.io/hangar/api/trials/), `src/hangar/pinsets.py`
- **Status:** hangar on main ([hangar#178](https://github.com/Sean-Koval/hangar/issues/178), trial cache [#180](https://github.com/Sean-Koval/hangar/issues/180)); flightdeck client: [flightdeck#25](https://github.com/Sean-Koval/flightdeck/issues/25)

## Run and Govern: decisions

### Decision: `hangar.decision/v1` {#decision}

**hangar ↔ Tower.** Sent to `POST /v1/decisions`, in five kinds: `job.release`, `tool.call`, `landing.approve`, `egress.request`, `secret.request`. Tower answers allow, deny or wait, plus a receipt. It fails closed and rolls out off → shadow → enforce.

- **Defined in:** hangar [spec 0015](https://github.com/Sean-Koval/hangar/blob/main/docs/specs/0015-governance-decision-point.md), Tower `docs/api/decisions.md`
- **Status:** Both sides built: Tower's API (Tower#13), hangar's client and contract tests ([hangar#171](https://github.com/Sean-Koval/hangar/issues/171)); wiring: [hangar#172](https://github.com/Sean-Koval/hangar/issues/172), [#173](https://github.com/Sean-Koval/hangar/issues/173)

### Approval events {#approval-events}

**Tower → hangar.** HMAC-signed `approval.created` and `approval.decided` events to one route, `/api/governance/events`. hangar re-reads the decision.

- **Defined in:** spec 0015 §12, Tower `docs/api/webhooks.md`
- **Status:** Tower's side on main (Tower#17); hangar's receiver: [hangar#190](https://github.com/Sean-Koval/hangar/issues/190)

### Passport {#passport}

**hangar sandbox → Tower.** A workload token exchanged under RFC 8693 for a 15-minute passport with the requester as subject.

- **Defined in:** Tower `aw/workload.py`, [hangar#174](https://github.com/Sean-Koval/hangar/issues/174)
- **Status:** Exchange on main for `/mcp`; for `/hooks`: Tower#14; hangar's side: [hangar#174](https://github.com/Sean-Koval/hangar/issues/174)

### Receipts: `aw.attest/v1` {#receipts}

**Tower → auditors and PRs.** Hash-chained receipts, and an attestation envelope with digests, model, requester and approver.

- **Defined in:** Tower `aw/audit.py`, `docs/api/receipts.md`
- **Status:** On main (Tower#18)

## To people: review and inbox

### Review packet and trailers {#review-packet}

**hangar → reviewers.** A review packet on each PR. `Harness-Digest:` trailers go on the PR body and the landed commit, with `Harness-Lock:` for a thawed job.

- **Defined in:** hangar `landing.py`, `trailers.py`, [hangar#137](https://github.com/Sean-Koval/hangar/issues/137)
- **Status:** On main

### Inbox {#inbox}

**hangar → engineers.** Inbox items: review, question, approval, failed. Questions and approvals also go by Slack DM, with a digest at 10:15 and 16:00.

- **Defined in:** hangar `inbox.py`, [#157](https://github.com/Sean-Koval/hangar/issues/157), [#158](https://github.com/Sean-Koval/hangar/issues/158)
- **Status:** On main; Tower's approvals in the digest: Tower#21, [hangar#277](https://github.com/Sean-Koval/hangar/issues/277)

## Capability: data tools

### Spaceport MCP tools {#spaceport-mcp-tools}

**Spaceport → agents.** Four MCP tools with typed results.

- **Defined in:** spaceport `gateway/mcp/server.py`
- **Status:** On main, frozen; asking Tower: spaceport#14
