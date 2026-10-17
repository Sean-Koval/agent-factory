---
hide:
  - navigation
  - toc
---

<div class="af-hero" markdown>
<span class="af-eyebrow">Agent factory · team tooling</span>

# Hand work to cloud coding agents and keep every change reviewable

<p class="af-lede">Five open-source tools that let a team of six engineers run about sixty agent sessions at once. One defines the harness, one runs it, one judges the runs, one governs risky decisions, and every change still leaves through a reviewed pull request.</p>

[See the architecture](architecture/index.md){ .md-button .md-button--primary } [Open the deck](deck.md){ .md-button }
</div>

<div class="af-tools">
  <a class="af-tool" href="tools/hangar/" style="--af-tool: var(--af-p-hangar)"><small>Run</small><b>hangar</b><span>Cloud sandboxes, sessions, jobs and experiment trials, from a Jira ticket to a landed PR.</span></a>
  <a class="af-tool" href="tools/flightdeck/" style="--af-tool: var(--af-p-flightdeck)"><small>Judge</small><b>flightdeck</b><span>Reads every run from Parquet and answers whether a harness change made agents better.</span></a>
  <a class="af-tool" href="tools/ai-dlc/" style="--af-tool: var(--af-p-aidlc)"><small>Define</small><b>ai-dlc</b><span>Authors the team workflow plugin, provisions machines, gates local work on CI.</span></a>
  <a class="af-tool" href="tools/workspace/" style="--af-tool: var(--af-p-workspace)"><small>Govern</small><b>Tower</b><span>One decision point for risky actions: rules, human approvals, signed receipts.</span></a>
  <a class="af-tool" href="tools/spaceport/" style="--af-tool: var(--af-p-spaceport)"><small>Capability</small><b>Spaceport</b><span>Reviewed data products that agents query through four MCP tools. Frozen.</span></a>
</div>

## How it fits together

<figure class="af-figure">
--8<-- "planes.svg"
<figcaption>The four planes, the doors and the gate</figcaption>
</figure>

hangar sits in the middle. Work arrives through the doors, the harness arrives as a lock file, risky decisions go out to the workspace, every run goes out to flightdeck, and flightdeck's verdict comes back as the next promoted harness. One number, `harness_digest`, identifies a harness from the lock file to the manifest, the PR and the report.

## Three rules the suite is built around

**Many doors, one inbox, one gate.** People start work wherever they already are: a Jira status, a GitHub label, Slack, an MCP client. Questions and approvals come back to one inbox, and nothing reaches a branch except through a pull request a human approves.

**Each tool owns one plane.** hangar never analyses runs, flightdeck never runs sandboxes, the workspace decides but never enforces, and ai-dlc stays off the agent's hot path. They meet only at versioned [contracts](architecture/contracts.md).

**Fail closed, measure everything.** Untrusted input taints a run and raises the bar to land it. Every run is written once to an outbox, so a harness change is judged on paired evidence rather than impressions.

## Where to go next

- [Architecture](architecture/index.md): the system context, the containers and where they run.
- [Flows](architecture/flows.md): a ticket to a merged PR, improving the harness, a risky action, the nightly pipeline, onboarding a repo.
- [Roadmap](roadmap.md): the four phases and their themes, with progress rebuilt daily from GitHub issues.
- [Decisions](decisions.md): choices that span more than one repo.
