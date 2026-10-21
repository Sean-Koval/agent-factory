---
hide:
  - navigation
  - toc
---

<div class="af-hero af-hero--visual" markdown>
<div markdown>
<span class="af-eyebrow">Agent factory · team tooling</span>

# Hand work to cloud coding agents and keep every change reviewable

<p class="af-lede">Tools that let a team of six engineers run about sixty agent sessions at once. Four planes: the team harness defines what the agents run, hangar runs them, flightdeck judges the runs and Tower governs risky decisions. ai-dlc sets up the people and machines around them, and every change still leaves through a reviewed pull request.</p>

[See how it fits](how-it-fits.md){ .md-button .md-button--primary } [Open the deck](deck.md){ .md-button }
</div>
<figure class="af-hero__visual">
<a href="assets/captures/hangar-fleet.png"><img src="assets/captures/hangar-fleet-deck.png#only-dark" alt="hangar's Fleet: the decision deck with a held push on top. Needs approval, Push the refunds migration to main, git push origin main, Deny, Allow for this turn and Approve push" width="672" height="384"></a>
<a href="assets/captures/hangar-fleet-day.png"><img src="assets/captures/hangar-fleet-day-deck.png#only-light" alt="hangar's Fleet: the decision deck with a held push on top. Needs approval, Push the refunds migration to main, git push origin main, Deny, Allow for this turn and Approve push" width="672" height="384"></a>
<figcaption>hangar's Fleet: one decision at a time. A push to main waits for you; the agents keep working.</figcaption>
</figure>
</div>

<div class="af-tools">
  <a class="af-tool" href="team-harness/"><small>Define</small><b>Team harness</b><span>The harness as native files and a lock, frozen from a good run and promoted on evidence.</span></a>
  <a class="af-tool" href="tools/hangar/" style="--af-tool: var(--af-product-hangar)"><small>Run</small><b>hangar</b><span>Runs coding agents in isolated cloud sandboxes, from a ticket to a landed PR.</span></a>
  <a class="af-tool" href="tools/flightdeck/" style="--af-tool: var(--af-product-flightdeck)"><small>Judge</small><b>flightdeck</b><span>Judges harness changes with paired statistics and behavior specs over every run.</span></a>
  <a class="af-tool" href="tools/workspace/" style="--af-tool: var(--af-product-tower)"><small>Govern</small><b>Tower</b><span>One decision point for risky actions: rules, human approvals, signed receipts.</span></a>
  <a class="af-tool" href="tools/ai-dlc/" style="--af-tool: var(--af-product-aidlc)"><small>Setup</small><b>ai-dlc</b><span>Sets up engineers' machines, authors the optional workflow plugin, gates local work on CI.</span></a>
</div>

Also in the suite: [Spaceport](tools/spaceport.md), reviewed data products that agents query through four MCP tools (frozen), and [Airframe](airframe/index.md), the design system every tool uses.

## Start here

- **Engineer:** [hangar](tools/hangar.md). `hangar connect` adds hangar to your agent client ([connecting clients](https://sean-koval.github.io/hangar/clients/)).
- **Harness owner:** [Team harness](team-harness.md). Copy the example, freeze a good run, and promote on evidence.
- **Running it at work:** [Run the factory at your company](work/index.md). The four-repo convention, change sets from a ticket to a deploy, and what stays yours.
- **Building UI:** [Airframe](airframe/index.md). Tokens, components and the rules every tool's UI follows.

## The four planes

<figure class="af-figure">
--8<-- "planes.svg"
<figcaption>The four planes, the doors and the gate · <a href="assets/diagrams/planes.svg">full size</a></figcaption>
</figure>

Define is the team harness repo, Run is hangar, Judge is flightdeck and Govern is Tower. hangar sits in the middle. Work arrives through the doors and the harness arrives as a lock file. Risky decisions go out to Tower, every run goes out to flightdeck, and the verdict comes back as the next promoted harness.

One number, `harness_digest`, identifies a harness from the lock file to the manifest, the PR and the report. ai-dlc is setup, off the agent's hot path. It prepares machines, authors the optional workflow plugin the harness may pin, and gates local work on CI.

## Where to go next

- [How it fits](how-it-fits.md): one ticket's journey through the four planes, the three rules, and who owns what.
- [Architecture](architecture/index.md): the system context, the containers and where they run.
- [Flows](architecture/flows.md): improving the harness, a risky action, the nightly pipeline, onboarding a repo.
- [Roadmap](roadmap.md): the four phases and their themes, with progress rebuilt daily from GitHub issues.
- [Decisions](decisions.md): choices that span more than one repo.
- [Glossary](glossary.md): the suite's terms, defined once.

hangar, flightdeck and ai-dlc are open source. Tower and Spaceport are private repositories for now.
