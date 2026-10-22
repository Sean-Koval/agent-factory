---
hide:
  - navigation
  - toc
---

# Roadmap

What the suite builds next, in four phases and a backlog, across hangar, flightdeck, ai-dlc, Tower, Spaceport and this repo. Phases are GitHub milestones of the same name in every repo; themes in [`roadmap.toml`](https://github.com/Sean-Koval/agent-factory/blob/main/roadmap.toml) group the issues that deliver one outcome. Open a theme's row to see its issues.

Each day the site build reads those milestones and issues from GitHub and recounts them. Day-to-day work is tracked in Jira (KAN), which this page does not read. To move an issue to another theme, edit `roadmap.toml`.

<details class="af-rm-issues" markdown>
<summary>Four decisions that shape the plan</summary>

- **No big harness spec.** A harness is native files plus a small lock; no new format or compiler in the next six weeks.
- **flightdeck waits for evidence.** No flightdeck code before week 5 and twenty labelled failures; v0 must change one real decision before it gets a UI.
- **Shadows wait for reviewers.** Shadow runs stay off until review wait p50 is under four hours.
- **Spaceport is frozen.** Cleanup only, until its MCP tools ask Tower's decision point.
- Choices that bind more than one repo are recorded on [Decisions](decisions.md).

</details>


--8<-- "roadmap.md"
