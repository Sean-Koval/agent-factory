---
hide:
  - navigation
  - toc
---

<div class="af-hero af-hero--visual" markdown>
<div markdown>
<span class="af-eyebrow">Agent factory · Suite</span>

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

Two more parts round out the suite. [Spaceport](tools/spaceport.md) is the Capability: reviewed data products that agents query through four MCP tools (frozen). [Airframe](airframe/index.md) is Design: the system every tool uses.

## See each tool work

Each clip is under 20 seconds and starts on the product. Select one to play it.

<div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr))" markdown>
<figure class="af-figure af-figure--lead">
<a href="assets/clips/hangar.mp4"><img src="assets/clips/hangar.png#only-dark" alt="The first frame of hangar's clip: the Fleet, with issue #42's job starting in checkout-python and the caption Issue #42 gets the hangar label, and a job starts" width="680" height="640"></a>
<a href="assets/clips/hangar-day.mp4"><img src="assets/clips/hangar-day.png#only-light" alt="The first frame of hangar's clip: the Fleet, with issue #42's job starting in checkout-python and the caption Issue #42 gets the hangar label, and a job starts" width="680" height="640"></a>
<figcaption>hangar: a ticket lands</figcaption>
</figure>
<figure class="af-figure af-figure--lead">
<a href="assets/clips/tower.mp4"><img src="assets/clips/tower.png#only-dark" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="760"></a>
<a href="assets/clips/tower-day.mp4"><img src="assets/clips/tower-day.png#only-light" alt="The first frame of Tower's clip: Marcus's Desk with Claude Code's git push origin main waiting for approval, and the caption Claude Code wants to push to main. Tower holds it for a tech lead" width="640" height="760"></a>
<figcaption>Tower: a deny, with a reason</figcaption>
</figure>
<figure class="af-figure af-figure--lead">
<a href="assets/clips/flightdeck.mp4"><img src="assets/clips/flightdeck.png#only-dark" alt="The first frame of flightdeck's clip: flightdeck stats compare in a terminal, with the two arms' resolved rates and the paired difference" width="680" height="640"></a>
<a href="assets/clips/flightdeck-day.mp4"><img src="assets/clips/flightdeck-day.png#only-light" alt="The first frame of flightdeck's clip: flightdeck stats compare in a terminal, with the two arms' resolved rates and the paired difference" width="680" height="640"></a>
<figcaption>flightdeck: a verdict on the PR</figcaption>
</figure>
<figure class="af-figure af-figure--lead">
<a href="assets/clips/ai-dlc.mp4"><img src="assets/clips/ai-dlc.png" alt="The first frame of ai-dlc's clip: ai-dlc project init in a terminal, answering status applied and 37 files" width="680" height="460"></a>
<figcaption>ai-dlc: a project's checks pass</figcaption>
</figure>
</div>

## Start here

- **Engineer:** [hangar](tools/hangar.md). `hangar connect` adds hangar to your agent client ([connecting clients](https://sean-koval.github.io/hangar/clients/)).
- **Harness owner:** [Team harness](team-harness.md). Copy the example, freeze a good run, and promote on evidence.
- **Running it at work:** [Run the factory at your company](work/index.md). The four-repo convention, change sets from a ticket to a deploy, and what stays yours.
- **Building UI:** [Airframe](airframe/index.md). Tokens, components and the rules every tool's UI follows.

## The four planes

<figure class="af-figure af-planes--wide">
--8<-- "planes.svg"
<figcaption>The four planes, the doors and the gate · <a href="assets/diagrams/planes.svg">full size</a></figcaption>
</figure>

<figure class="af-figure af-planes--stacked">
--8<-- "planes-stacked.svg"
<figcaption>The four planes, one above the other · <a href="assets/diagrams/planes.svg">the wide drawing</a></figcaption>
</figure>

Define is the team harness repo, Run is hangar, Judge is flightdeck and Govern is Tower. hangar sits in the middle. Work arrives through the doors and the harness arrives as a lock file. Risky decisions go out to Tower, every run goes out to flightdeck, and the verdict comes back as the next promoted harness.

One number, `harness_digest`, identifies a harness from the lock file to the manifest, the PR and the report. ai-dlc is setup, off the agent's hot path. It prepares machines, authors the optional workflow plugin the harness may pin, and gates local work on CI.

## Where to go next

- [How it fits](how-it-fits.md): one ticket's journey through the four planes, the three rules, and who owns what.
- [Architecture](architecture/index.md): the system context, the containers and where they run.
- [Flows](architecture/flows.md): improving the harness, a risky action, the nightly pipeline, onboarding a repo.
- [Roadmap](roadmap.md): the four phases and their themes, with counts rebuilt daily from each repo's GitHub milestones.
- [Decisions](decisions.md): choices that span more than one repo.
- [Glossary](glossary.md): the suite's terms, defined once.

hangar, flightdeck and ai-dlc are open source. Tower and Spaceport are private repositories for now.
