# Roadmap

What the suite builds next, in four phases and a backlog, across hangar, flightdeck, ai-dlc, Tower (the governed workspace), Spaceport and this repo. Phases are GitHub milestones of the same name in every repo; themes group the issues that deliver one outcome.

The counts and lists below are rebuilt from GitHub issue state every day and on every publish, so they match GitHub at build time. To move an issue between themes, or to place a new one, edit [`roadmap.toml`](https://github.com/Sean-Koval/agent-factory/blob/main/roadmap.toml); open issues it does not place appear under [Unsorted](#unsorted). Private repositories are named but their issues are not listed here.

| Phase | Weeks | Done when |
| --- | --- | --- |
| P1 · Safe release | 1-2 | Security fixes, credential policy and grader isolation are in; CI is green; two engineers use hangar on one repo. |
| P2 · Adopt and capture | 3-4 | All six engineers on three repos through the Jira door and the Slack inbox; every run lands in the outbox and Parquet; weekly metrics; a team harness frozen from a good run. |
| P3 · flightdeck v0 | 5-6 | flightdeck's stats and reports run over real runs and change one real decision. |
| P4 · Frontier | 7 on | Record-mode gateway, replay-as-fork, pin-set trials, shadows, governed tool calls. |

## Decisions that shape the plan

- **No big harness spec.** A harness is native files plus a small lock; no new format or compiler in the next six weeks.
- **flightdeck waits for evidence.** No flightdeck code before week 5 and twenty labelled failures; v0 must change one real decision before it gets a UI.
- **Shadows wait for reviewers.** Shadow runs stay off until review wait p50 is under four hours.
- **Spaceport is frozen.** Cleanup only, until its MCP tools ask the workspace's decision point.

Choices that bind more than one repo are recorded on [Decisions](decisions.md).

--8<-- "roadmap.md"
