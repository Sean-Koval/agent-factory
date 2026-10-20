# Glossary

The suite's terms, defined once. Where a tool's own docs go deeper, the entry links there.

| Term | Meaning |
| --- | --- |
| Admission | hangar's decision to start a queued job: budgets, fairness, the power schedule and review capacity. A person whose five agent PRs wait on review has new jobs held as `awaiting_capacity` ([hangar#159](https://github.com/Sean-Koval/hangar/issues/159)). |
| Airframe | The suite's design system. Its source is this repo's `airframe/` (values in `airframe/tokens.json`); `theme/` holds the files generated from it, which each tool vendors. |
| Behavior spec | `flightdeck.spec/v1`: a predicate over a trace, such as "tests run before a PR opens", judged per run. |
| Channel | A name in the team harness repo's `channels.yaml` (`stable`, `candidate`) that holds one `harness_digest`. `team-default@stable` resolves through it; only a promotion moves `stable`. |
| Compactor | flightdeck's nightly Cloud Run job that flattens new outbox objects into `flightdeck.parquet/v1`, while the sandbox pools are off ([flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5)). |
| Decision point | Tower's API, `POST /v1/decisions`, that hangar asks before releasing a job, landing, or running a risky tool call, host or secret. It answers allow, deny or wait. |
| Door | A place where work starts: a Jira status, a GitHub label, Slack, an MCP client, a schedule. |
| Drift | A difference between what a sandbox ran on turn 1 and its harness lock, or a trial's pin set. hangar records it on the turn (`harness.drift`); under `HANGAR_HARNESS_DRIFT=fail` the turn stops, and a drifted trial ends as `infra_error` / `drift` without a retry. |
| Environment | hangar's reusable recipe for a sandbox: base image, packages, skills and instructions, MCP servers, credentials, resources and optionally the repo. Its spec has a digest (`environment_spec_digest`); a turn's manifest also records `environment_digest`, what the sandbox actually was. |
| Experiment | A set of tasks × variants × trials that flightdeck plans and hangar runs (`hangar.experiment/v1`); hangar records a pin set per variant. |
| Freeze, thaw | `hangar harness freeze` writes native files and a `harness.lock` from a turn that went well. `hangar harness thaw NAME@ref` runs a session or job from a lock, with its files mounted read-only. |
| Gate | The one way a change reaches a branch: a pull request that a second human approves at its exact commit. |
| Harness | Everything that shapes how a coding agent works. The agent CLI at a pinned version, the concrete model, instructions, skills, plugins, hooks, MCP bindings and the approval mode. A team keeps each one as a harness directory (native files plus `harness.lock`) in its team harness repo. hangar's [concepts](https://sean-koval.github.io/hangar/concepts/#harness) page also calls the agent CLI itself a harness. |
| `harness.lock` | `hangar.harness-lock/v1`: pins each native file by digest, plus the CLI version, the concrete model and the binding layer (MCP servers, hooks, approvals: names, never values). |
| `harness_digest` | The one hash that identifies a harness: a SHA-256 over the lock's identity fields. Name, revision and paths are not part of it. The lock, the manifest, the PR trailer and every report carry the same value. |
| Inbox | One list per person of reviews, questions, approvals and failures, delivered as a Slack DM and a digest at 10:15 and 16:00. |
| `infra_error` | An outcome caused by infrastructure (preemption, power-down, rate limits, drift); excluded from statistics, and retried except for drift. |
| Intake posture | hangar's rule that intake jobs need the git gateway and an egress allowlist. |
| Job | A piece of work hangar runs to a result. An agent turn in a session, the repo's own check (`verify`), then a branch and a draft pull request. |
| Manifest | `hangar.manifest/v1`: the effective configuration captured when a turn starts. |
| Outbox | Cloud Storage objects written once per finished run, the input to flightdeck's Parquet store (its data plane). |
| Passport | A 15-minute token Tower issues under RFC 8693 in exchange for a workload token, with the requester as subject. |
| Plane | One of the four responsibilities the suite is split into, each owned by one tool. Define (the team harness repo), Run (hangar), Judge (flightdeck) and Govern (Tower). ai-dlc is setup, not a plane, and Spaceport is a capability under the suite. The sense is control plane / data plane, not aircraft; flightdeck's own "data plane" is its Parquet store. |
| Pin set | `hangar.pinset/v1`: what a trial runs with, recorded once and never changed. The harness lock and its digest, the environment's digests, the concrete model, each task's base commit, the grader's and egress policy's digests. Its id is a hash of its content ([hangar: trials and pin sets](https://sean-koval.github.io/hangar/api/trials/)). |
| Promotion | Moving `stable` in `channels.yaml` to a candidate's digest, by a PR whose approver is not its author, after flightdeck's report against the pre-registered `decision.yaml`. |
| Receipt | A hash-chained record of a Tower decision, attached to the action it allowed; its attestation envelope is `aw.attest/v1`. |
| Review packet | The comment hangar adds to each agent PR: the verification, cost, harness and model, files touched, risk and links. |
| Sandbox | A running, isolated copy of an environment where an agent works. Job sandboxes can fetch but never push; hangar pushes the commit it verified. |
| Sealed grader | A grading sandbox with no network, no credentials and hidden tests from a pristine copy. |
| Sealed holdout | Tasks nobody tuning a harness has seen, kept in the private data repo with hashes and canaries, and scored once on explicit go-ahead ([flightdeck: holdouts](https://sean-koval.github.io/flightdeck/holdouts/)). |
| Session | A resumable stream of work: an agent's conversation plus the repo's state, checkpointed after every turn. |
| Shadow (governance) | A rollout mode for one decision kind: hangar's own rules still decide, Tower answers the same question as a dry run, and disagreements are counted. The order is `off`, `shadow`, `enforce`. |
| Shadow (run) | A trial of a candidate harness on a sampled real ticket (`source: shadow`) that delivers nothing: no PR, no tracker write-back, no Slack post ([hangar#183](https://github.com/Sean-Koval/hangar/issues/183)). Shadows stay off while the review wait p50 is four hours or more. |
| Taint | A mark on a turn or session that has read untrusted content; it raises the bar to push and land. |
| Team harness repo | The git repository where a team keeps its harnesses (`harnesses/<name>/`), `channels.yaml` and the CI that checks them; `HANGAR_HARNESS_REPO` points hangar at it. The public example is [Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness); see [Team harness](team-harness.md). |
| Tower | The Govern plane: one decision point (Cedar), approvals where the approver is never the requester, passports and signed receipts. Formerly the governed workspace (Tower ADR 0017). |
| Trace | `hangar.trace/v1`: OTLP spans for every step of a run, with tool kinds and shell operations. |
| Trial | One attempt at one task against one pin set (one variant of an experiment). `POST /api/trials` starts n of them. |
| Turn | One round of agent work in a session, from a message to its result; each turn records its own manifest. |
| Workflow plugin | ai-dlc's workflow guidance, team skills and safety hooks packaged as one Claude Code plugin (`ai-dlc-workflow`, with a Codex form), off by default. A team harness pins it as `plugin:ai-dlc-workflow@team-harness`. |
