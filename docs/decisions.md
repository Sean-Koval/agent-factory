# Decisions

What the suite has decided across repos, how firm each choice is, and where it is written down. Each tool keeps its own ADRs; this page records only the choices that bind more than one repo.

Every record reads the same way: the decision, its status, and the place it is recorded.

- **Accepted**: the owner decided it.
- **Built**: it is on main in every repo it touches.
- **Proposed**: it is written and waits for the owner.

Tower and Spaceport are private repositories, so their ADRs and issues are named without links.

## The planes and the harness

### One plane per tool {#one-plane-per-tool}

Each tool owns one plane: the team harness repo defines, hangar runs, flightdeck judges and Tower decides. ai-dlc authors the optional workflow plugin. hangar does no analysis.

- **Status:** Accepted
- **Recorded in:** hangar spec 0014 §1, flightdeck ADR 0001, [ai-dlc ADR 0001](https://github.com/Sean-Koval/ai-dlc/blob/main/docs/decisions/0001-refocus-ai-dlc.md)

### No big harness spec {#no-big-harness-spec}

A harness is native files plus a small lock, with no new format or compiler. Its identity is `harness_digest`, computed the same way by the lock and the manifest.

- **Status:** Accepted
- **Recorded in:** hangar spec 0014 §2, [hangar `docs/harness-lock.md`](https://sean-koval.github.io/hangar/harness-lock/)

### A public example harness {#a-public-example-harness}

The example is separate from the team's real harness, which is internal to the owner's employer. It lives at [Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness).

- **Status:** Accepted (owner, 2026-10-17)
- **Recorded in:** [agent-factory#4](https://github.com/Sean-Koval/agent-factory/issues/4), [hangar#138](https://github.com/Sean-Koval/hangar/issues/138)

### ai-dlc refocuses {#ai-dlc-refocuses}

ai-dlc keeps the workflow plugin, machine provisioning and the CI-gated work lifecycle. It neither defines nor evaluates harnesses; `ai-dlc eval` moved to flightdeck.

- **Status:** Accepted
- **Recorded in:** [ai-dlc ADR 0001](https://github.com/Sean-Koval/ai-dlc/blob/main/docs/decisions/0001-refocus-ai-dlc.md), [ai-dlc#189](https://github.com/Sean-Koval/ai-dlc/issues/189)

### Three trackers, no Linear {#three-trackers-no-linear}

Trackers are GitHub Issues, Jira and GitHub Projects. Linear is not supported.

- **Status:** Accepted
- **Recorded in:** ai-dlc tracker boundary

## Running and judging

### flightdeck reads exports only {#flightdeck-reads-exports-only}

flightdeck reads exports and the outbox, never hangar's database or live API during analysis.

- **Status:** Accepted
- **Recorded in:** flightdeck ADR 0001

### Public code, private run data {#public-code-private-run-data}

Code is public, run data is private.

- **Status:** Accepted
- **Recorded in:** flightdeck ADR 0002

### The outbox layout {#the-outbox-layout}

The layout is `v1/runs/{date}/{session}.{run}/`, with `run.json` written last as the completion marker.

- **Status:** Built
- **Recorded in:** hangar `docs/api/outbox.md`, [hangar#163](https://github.com/Sean-Koval/hangar/issues/163) ([PR #214](https://github.com/Sean-Koval/hangar/pull/214))

### flightdeck owns the compactor {#flightdeck-owns-the-compactor}

The GCS → Parquet compactor belongs to flightdeck.

- **Status:** Built
- **Recorded in:** [flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5), flightdeck `deploy/compactor/`

### flightdeck owns sampling {#flightdeck-owns-sampling}

The hangar ↔ flightdeck seam is a trial against an immutable pin set. hangar runs each trial exactly as pinned.

- **Status:** Built on hangar's side; flightdeck's client is [flightdeck#25](https://github.com/Sean-Koval/flightdeck/issues/25)
- **Recorded in:** [hangar#178](https://github.com/Sean-Koval/hangar/issues/178), hangar [`docs/api/trials.md`](https://sean-koval.github.io/hangar/api/trials/)

### ADR checks use the spec grammar {#adr-checks-use-the-spec-grammar}

ADR `checks:` use flightdeck's behavior-spec grammar. The convention for ADRs is ai-dlc's.

- **Status:** Built; the nightly runner is [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15)
- **Recorded in:** [ai-dlc#207](https://github.com/Sean-Koval/ai-dlc/issues/207), [flightdeck#14](https://github.com/Sean-Koval/flightdeck/issues/14)

### Reviewer attention is the scarce resource {#reviewer-attention-is-the-scarce-resource}

Admission holds a person's new jobs while five of their agent PRs wait on review (`HANGAR_PERSON_MAX_OPEN_AGENT_PRS`).

- **Status:** Built
- **Recorded in:** [hangar#159](https://github.com/Sean-Koval/hangar/issues/159); attention per merged PR as a metric: [hangar#278](https://github.com/Sean-Koval/hangar/issues/278)

### flightdeck's line budget {#flightdecks-line-budget}

The budget is 3,785 counted lines, up from the plan's 1,500 through flightdeck ADRs 0003–0005. ADR 0005 is agent-proposed and asks for owner review.

- **Status:** Awaiting owner review
- **Recorded in:** flightdeck ADRs [0003](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0003-line-budget.md), [0004](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0004-local-runner-budget.md), [0005](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0005-post-v0-budget.md)

## Governing

### The Govern plane is named Tower {#the-govern-plane-is-named-tower}

Tower replaces "Agent workspace", "governed agent workspace" and "governed workspace" in user-facing text. The repository is Sean-Koval/tower.

- **Status:** Accepted
- **Recorded in:** Tower ADR 0017 (Tower#36)

### Tower decides, hangar enforces {#tower-decides-hangar-enforces}

Decisions fail closed and roll out per kind: off → shadow → enforce.

- **Status:** Proposed; Tower's side is built (Tower#13)
- **Recorded in:** hangar spec 0015, Tower ADR 0015

### One signed route for Tower's events {#one-signed-route-for-towers-events}

Tower's events reach hangar on one HMAC-signed route. hangar re-reads the decision before acting.

- **Status:** Proposed; Tower's side is built (Tower#17), hangar's is [hangar#190](https://github.com/Sean-Koval/hangar/issues/190)
- **Recorded in:** hangar spec 0015 §12

### Team knowledge lives in git {#team-knowledge-lives-in-git}

Git is the source of truth for team knowledge. The pull request is the only write gate, and agents only propose.

- **Status:** Proposed
- **Recorded in:** Tower ADR 0016

### OpenSpaces is inspiration only {#openspaces-is-inspiration-only}

OpenSpaces informs Tower's UI and is not a base to build on. It lacks consistent authorization and agent execution.

- **Status:** Plan; not yet in an ADR
- **Recorded in:** The suite architecture plan

### Spaceport is frozen {#spaceport-is-frozen}

Security fixes and cleanup only, until its MCP tools ask Tower's decision point.

- **Status:** Accepted (2026-10-16)
- **Recorded in:** spaceport#10; asking Tower: spaceport#14

## Design

### One design system {#one-design-system}

Airframe is the one design system across every site and tool. This repo is its source of truth.

- **Status:** Accepted
- **Recorded in:** [`airframe/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe), with its values in `airframe/tokens.json`
