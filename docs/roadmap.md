---
hide:
  - navigation
  - toc
---

# Roadmap

What the suite builds next, and how far each phase has come. There are four phases and a backlog, across hangar, flightdeck, ai-dlc, Tower, Spaceport and this repo.

- **A phase** is a GitHub milestone of the same name in every repo.
- **A theme** groups the issues that deliver one outcome. Open a theme's row to see its issues.
- **The counts** are recounted each day, when the site build reads milestones and issues from GitHub.

Themes live in [`roadmap.toml`](https://github.com/Sean-Koval/agent-factory/blob/main/roadmap.toml); edit it to move an issue to another theme. Day-to-day work is tracked in Jira (KAN), which this page does not read.

<details class="af-rm-issues" markdown>
<summary>Four decisions that shape the plan</summary>

- **No big harness spec.** A harness is native files plus a small lock; no new format or compiler in the next six weeks.
- **flightdeck waits for evidence.** No flightdeck code before week 5 and twenty labelled failures; v0 must change one real decision before it gets a UI.
- **Shadows wait for reviewers.** Shadow runs stay off until review wait p50 is under four hours.
- **Spaceport is frozen.** Cleanup only, until its MCP tools ask Tower's decision point.

Choices that bind more than one repo are recorded on [Decisions](decisions.md).

</details>


--8<-- "roadmap.md"
