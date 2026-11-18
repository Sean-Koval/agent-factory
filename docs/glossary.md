# Glossary

What a suite term means, defined once and in alphabetical order. Each entry has its own link, and where a tool's docs go deeper the entry points there.

Jump to [A to D](#a-to-d), [E to H](#e-to-h), [I to P](#i-to-p), [R to S](#r-to-s), [T to W](#t-to-w).

## A to D

### Admission {#admission}

hangar's decision to start a queued job: budgets, fairness, the power schedule and review capacity. A person whose five agent PRs wait on review has new jobs held as `awaiting_capacity` ([hangar#159](https://github.com/Sean-Koval/hangar/issues/159)).

### Airframe {#airframe}

The suite's design system. Its source is this repo's `airframe/` (values in `airframe/tokens.json`); `theme/` holds the files generated from it, which each tool vendors.

### Behavior spec {#behavior-spec}

`flightdeck.spec/v1`: a predicate over a [trace](#trace), such as "tests run before a PR opens", judged per run.

### Channel {#channel}

A name in the [team harness repo](#team-harness-repo)'s `channels.yaml` (`stable`, `candidate`) that holds one [`harness_digest`](#harness-digest). `team-default@stable` resolves through it; only a [promotion](#promotion) moves `stable`.

### Compactor {#compactor}

flightdeck's nightly Cloud Run job that flattens new [outbox](#outbox) objects into `flightdeck.parquet/v1`, while the [sandbox](#sandbox) pools are off ([flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5)).

### Decision point {#decision-point}

Tower's API, `POST /v1/decisions`, that hangar asks before releasing a job, landing, or running a risky tool call, host or secret. It answers allow, deny or wait.

### Door {#door}

A place where work starts: a Jira status, a GitHub label, Slack, an MCP client, a schedule.

### Drift {#drift}

A difference between what a sandbox ran on turn 1 and its [harness lock](#harness-lock), or a trial's [pin set](#pin-set). hangar records it on the turn (`harness.drift`); under `HANGAR_HARNESS_DRIFT=fail` the turn stops, and a drifted trial ends as [`infra_error`](#infra-error) / `drift` without a retry.

## E to H

### Environment {#environment}

hangar's reusable recipe for a [sandbox](#sandbox): base image, packages, skills and instructions, MCP servers, credentials, resources and optionally the repo. Its spec has a digest (`environment_spec_digest`); a [turn](#turn)'s [manifest](#manifest) also records `environment_digest`, what the sandbox actually was.

### Experiment {#experiment}

A set of tasks × variants × [trials](#trial) that flightdeck plans and hangar runs (`hangar.experiment/v1`); hangar records a [pin set](#pin-set) per variant.

### Freeze, thaw {#freeze-thaw}

`hangar harness freeze` writes native files and a [`harness.lock`](#harness-lock) from a [turn](#turn) that went well. `hangar harness thaw NAME@ref` runs a [session](#session) or job from a lock, with its files mounted read-only.

### Gate {#gate}

The one way a change reaches a branch: a pull request that a second human approves at its exact commit.

### Harness {#harness}

Everything that shapes how a coding agent works. The agent CLI at a pinned version, the concrete model, instructions, skills, plugins, hooks, MCP bindings and the approval mode. A team keeps each one as a harness directory (native files plus [`harness.lock`](#harness-lock)) in its [team harness repo](#team-harness-repo). hangar's [concepts](https://sean-koval.github.io/hangar/concepts/#harness) page also calls the agent CLI itself a harness.

### `harness_digest` {#harness-digest}

The one hash that identifies a harness: a SHA-256 over the lock's identity fields. Name, revision and paths are not part of it. The lock, the [manifest](#manifest), the PR trailer and every report carry the same value.

### `harness.lock` {#harness-lock}

`hangar.harness-lock/v1`: pins each native file by digest, plus the CLI version, the concrete model and the binding layer (MCP servers, hooks, approvals: names, never values).

## I to P

### Inbox {#inbox}

One list per person of reviews, questions, approvals and failures, delivered as a Slack DM and a digest at 10:15 and 16:00.

### `infra_error` {#infra-error}

An outcome caused by infrastructure (preemption, power-down, rate limits, [drift](#drift)); excluded from statistics, and retried except for drift.

### Intake posture {#intake-posture}

hangar's rule that intake jobs need the git gateway and an egress allowlist.

### Job {#job}

A piece of work hangar runs to a result. An agent [turn](#turn) in a [session](#session), the repo's own check (`verify`), then a branch and a draft pull request.

### Manifest {#manifest}

`hangar.manifest/v1`: the effective configuration captured when a [turn](#turn) starts.

### Outbox {#outbox}

Cloud Storage objects written once per finished run, the input to flightdeck's Parquet store (its data plane).

### Passport {#passport}

A 15-minute token Tower issues under RFC 8693 in exchange for a workload token, with the requester as subject.

### Pin set {#pin-set}

`hangar.pinset/v1`: what a [trial](#trial) runs with, recorded once and never changed. The [harness lock](#harness-lock) and its digest, the [environment](#environment)'s digests, the concrete model, each task's base commit, the grader's and egress policy's digests. Its id is a hash of its content ([hangar: trials and pin sets](https://sean-koval.github.io/hangar/api/trials/)).

### Plane {#plane}

One of the four responsibilities the suite is split into, each owned by one tool. Define (the [team harness repo](#team-harness-repo)), Run (hangar), Judge (flightdeck) and Govern (Tower). ai-dlc is setup, not a plane, and Spaceport is a capability under the suite. The sense is control plane / data plane, not aircraft; flightdeck's own "data plane" is its Parquet store.

### Promotion {#promotion}

Moving `stable` in `channels.yaml` to a candidate's digest, by a PR whose approver is not its author, after flightdeck's report against the pre-registered `decision.yaml`.

## R to S

### Receipt {#receipt}

A hash-chained record of a Tower decision, attached to the action it allowed; its attestation envelope is `aw.attest/v1`.

### Review packet {#review-packet}

The comment hangar adds to each agent PR: the verification, cost, harness and model, files touched, risk and links.

### Sandbox {#sandbox}

A running, isolated copy of an [environment](#environment) where an agent works. Job sandboxes can fetch but never push; hangar pushes the commit it verified.

### Sealed grader {#sealed-grader}

A grading [sandbox](#sandbox) with no network, no credentials and hidden tests from a pristine copy.

### Sealed holdout {#sealed-holdout}

Tasks nobody tuning a harness has seen, kept in the private data repo with hashes and canaries, and scored once on explicit go-ahead ([flightdeck: holdouts](https://sean-koval.github.io/flightdeck/holdouts/)).

### Session {#session}

A resumable stream of work: an agent's conversation plus the repo's state, checkpointed after every [turn](#turn).

### Shadow (governance) {#shadow-governance}

A rollout mode for one decision kind: hangar's own rules still decide, Tower answers the same question as a dry run, and disagreements are counted. The order is `off`, `shadow`, `enforce`.

### Shadow (run) {#shadow-run}

A [trial](#trial) of a candidate harness on a sampled real ticket (`source: shadow`) that delivers nothing: no PR, no tracker write-back, no Slack post ([hangar#183](https://github.com/Sean-Koval/hangar/issues/183)). Shadows stay off while the review wait p50 is four hours or more.

## T to W

### Taint {#taint}

A mark on a [turn](#turn) or [session](#session) that has read untrusted content; it raises the bar to push and land.

### Team harness repo {#team-harness-repo}

The git repository where a team keeps its harnesses (`harnesses/<name>/`), `channels.yaml` and the CI that checks them; `HANGAR_HARNESS_REPO` points hangar at it. The public example is [Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness); see [Team harness](team-harness.md).

### Tower {#tower}

The Govern plane: one [decision point](#decision-point) (Cedar), approvals where the approver is never the requester, [passports](#passport) and signed [receipts](#receipt). Formerly the governed workspace (Tower ADR 0017).

### Trace {#trace}

`hangar.trace/v1`: OTLP spans for every step of a run, with tool kinds and shell operations.

### Trial {#trial}

One attempt at one task against one [pin set](#pin-set) (one variant of an [experiment](#experiment)). `POST /api/trials` starts n of them.

### Turn {#turn}

One round of agent work in a [session](#session), from a message to its result; each turn records its own [manifest](#manifest).

### Workflow plugin {#workflow-plugin}

ai-dlc's workflow guidance, team skills and safety hooks packaged as one Claude Code plugin (`ai-dlc-workflow`, with a Codex form), off by default. A team harness pins it as `plugin:ai-dlc-workflow@team-harness`.
