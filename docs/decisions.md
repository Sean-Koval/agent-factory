# Decisions

Choices that affect more than one repo. Each tool keeps its own ADRs; this page records the ones that bind them together.

| Decision | Status | Where it is recorded |
| --- | --- | --- |
| Each tool owns one plane: hangar runs, flightdeck judges, the workspace decides, ai-dlc defines. hangar does no analysis. | Accepted | hangar spec 0014 §1, flightdeck ADR 0001 |
| A harness is native files plus a small lock; its identity is `harness_digest`, computed the same way by the lock and the manifest. | Accepted | hangar spec 0014 §2 |
| flightdeck reads exports and the outbox, never hangar's database or live API during analysis. | Accepted | flightdeck ADR 0001 |
| Code is public, run data is private. | Accepted | flightdeck ADR 0002 |
| The workspace decides and hangar enforces. Decisions fail closed and roll out off → shadow → enforce. | Proposed | hangar spec 0015 |
| Workspace events reach hangar on one HMAC-signed route; hangar re-reads the decision before acting. | Proposed | hangar spec 0015 |
| The outbox layout is `v1/runs/{date}/{session}.{run}/` with `run.json` written last as the completion marker. | Proposed | hangar outbox PR, flightdeck #5 |
| The GCS → Parquet compactor belongs to flightdeck. | Open | flightdeck #5 |
| ADR `checks:` use flightdeck's behavior-spec grammar. | Open | ai-dlc #207, flightdeck #15 |
| Trackers are GitHub Issues, Jira and GitHub Projects. Linear is not supported. | Accepted | ai-dlc tracker boundary |
| One design system, Airframe, across every site and tool; this repo hosts its tokens. | Accepted | [`theme/`](https://github.com/Sean-Koval/agent-factory/tree/main/theme) |
