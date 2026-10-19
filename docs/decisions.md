# Decisions

Choices that affect more than one repo. Each tool keeps its own ADRs; this page records the ones that bind them together.

**Accepted** means the owner decided it. **Built** means it is on main in every repo it touches. **Proposed** means it is written and waits for the owner. Tower and Spaceport are private repositories, so their ADRs and issues are named without links.

## The planes and the harness

| Decision | Status | Where it is recorded |
| --- | --- | --- |
| Each tool owns one plane: the team harness repo defines, hangar runs, flightdeck judges, Tower decides. ai-dlc authors the optional workflow plugin. hangar does no analysis. | Accepted | hangar spec 0014 §1, flightdeck ADR 0001, [ai-dlc ADR 0001](https://github.com/Sean-Koval/ai-dlc/blob/main/docs/decisions/0001-refocus-ai-dlc.md) |
| No big harness spec. A harness is native files plus a small lock, with no new format or compiler; its identity is `harness_digest`, computed the same way by the lock and the manifest. | Accepted | hangar spec 0014 §2, [hangar `docs/harness-lock.md`](https://sean-koval.github.io/hangar/harness-lock/) |
| A public example harness, separate from the team's real one, which is internal to the owner's employer. The example is [Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness). | Accepted (owner, 2026-10-17) | [agent-factory#4](https://github.com/Sean-Koval/agent-factory/issues/4), [hangar#138](https://github.com/Sean-Koval/hangar/issues/138) |
| ai-dlc refocuses on the workflow plugin, machine provisioning and the CI-gated work lifecycle. It neither defines nor evaluates harnesses; `ai-dlc eval` moved to flightdeck. | Accepted | [ai-dlc ADR 0001](https://github.com/Sean-Koval/ai-dlc/blob/main/docs/decisions/0001-refocus-ai-dlc.md), [ai-dlc#189](https://github.com/Sean-Koval/ai-dlc/issues/189) |
| Trackers are GitHub Issues, Jira and GitHub Projects. Linear is not supported. | Accepted | ai-dlc tracker boundary |

## Running and judging

| Decision | Status | Where it is recorded |
| --- | --- | --- |
| flightdeck reads exports and the outbox, never hangar's database or live API during analysis. | Accepted | flightdeck ADR 0001 |
| Code is public, run data is private. | Accepted | flightdeck ADR 0002 |
| The outbox layout is `v1/runs/{date}/{session}.{run}/` with `run.json` written last as the completion marker. | Built | hangar `docs/api/outbox.md`, [hangar#163](https://github.com/Sean-Koval/hangar/issues/163) ([PR #214](https://github.com/Sean-Koval/hangar/pull/214)) |
| The GCS → Parquet compactor belongs to flightdeck. | Built | [flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5), flightdeck `deploy/compactor/` |
| flightdeck owns sampling. The hangar ↔ flightdeck seam is a trial against an immutable pin set; hangar runs each trial exactly as pinned. | Built on hangar's side; flightdeck's client is [flightdeck#25](https://github.com/Sean-Koval/flightdeck/issues/25) | [hangar#178](https://github.com/Sean-Koval/hangar/issues/178), hangar [`docs/api/trials.md`](https://sean-koval.github.io/hangar/api/trials/) |
| ADR `checks:` use flightdeck's behavior-spec grammar; the convention for ADRs is ai-dlc's. | Built; the nightly runner is [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15) | [ai-dlc#207](https://github.com/Sean-Koval/ai-dlc/issues/207), [flightdeck#14](https://github.com/Sean-Koval/flightdeck/issues/14) |
| Reviewer attention is the scarce resource. Admission holds a person's new jobs while five of their agent PRs wait on review (`HANGAR_PERSON_MAX_OPEN_AGENT_PRS`). | Built | [hangar#159](https://github.com/Sean-Koval/hangar/issues/159); attention per merged PR as a metric: [hangar#278](https://github.com/Sean-Koval/hangar/issues/278) |
| flightdeck's line budget is 3,785 counted lines, up from the plan's 1,500 through flightdeck ADRs 0003–0005. ADR 0005 is agent-proposed and asks for owner review. | Awaiting owner review | flightdeck ADRs [0003](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0003-line-budget.md), [0004](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0004-local-runner-budget.md), [0005](https://github.com/Sean-Koval/flightdeck/blob/main/docs/decisions/0005-post-v0-budget.md) |

## Governing

| Decision | Status | Where it is recorded |
| --- | --- | --- |
| The Govern plane's product is named Tower. It replaces "Agent workspace", "governed agent workspace" and "governed workspace" in user-facing text; the repository is Sean-Koval/tower. | Accepted | Tower ADR 0017 (Tower#36) |
| Tower decides and hangar enforces. Decisions fail closed and roll out per kind: off → shadow → enforce. | Proposed; Tower's side is built (Tower#13) | hangar spec 0015, Tower ADR 0015 |
| Tower's events reach hangar on one HMAC-signed route; hangar re-reads the decision before acting. | Proposed; Tower's side is built (Tower#17), hangar's is [hangar#190](https://github.com/Sean-Koval/hangar/issues/190) | hangar spec 0015 §12 |
| Team knowledge lives in git, which is the source of truth; the pull request is the only write gate; agents only propose. | Proposed | Tower ADR 0016 |
| OpenSpaces is inspiration for Tower's UI only, not a base to build on: it lacks consistent authorization and agent execution. | Plan; not yet in an ADR | The suite architecture plan |
| Spaceport is frozen: security fixes and cleanup only, until its MCP tools ask Tower's decision point. | Accepted (2026-10-16) | spaceport#10; asking Tower: spaceport#14 |

## Design

| Decision | Status | Where it is recorded |
| --- | --- | --- |
| One design system, Airframe, across every site and tool; this repo is its source of truth. | Accepted | [`airframe/`](https://github.com/Sean-Koval/agent-factory/tree/main/airframe), with its values in `airframe/tokens.json` |
