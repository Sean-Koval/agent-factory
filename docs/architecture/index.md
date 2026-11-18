---
hide:
  - navigation
  - toc
---

# Architecture

Who uses the suite, what it depends on, and which tool owns which decision. This page is the system context, level 1 of the [C4 model](https://c4model.com/). The other three pages go one level down.

- [Containers](containers.md): what runs where, and what is deployed.
- [Contracts](contracts.md): the file or API two tools meet at.
- [Flows](flows.md): a harness change, a risky action, the nightly run, a new repo.
- [How it fits](../how-it-fits.md): one ticket's path to a merged PR.

## System context

<figure class="af-figure">
--8<-- "c4-context.svg"
<figcaption>C4 level 1: the people who use the suite above it, the outside systems around it. The diagram follows the page's light or dark theme. <a href="../assets/diagrams/c4-context.svg">Full size</a></figcaption>
</figure>

### Who uses it

- **Engineers** hand off work and answer questions.
- **Reviewers** approve the exact commit that lands.
- The **harness owner** runs experiments and promotes the team harness.
- **Approvers** decide risky actions.

### What it depends on

- **GitHub** for code and review.
- **Jira and Slack** as [doors](../glossary.md#door): work comes in, questions and approvals go out.
- **Model providers** through API keys only.
- **Google Cloud** to run on.
- **MCP servers** for the tools agents call.

PNGs of both diagrams, for slides, are listed on the [Deck](../deck.md#diagrams-for-your-own-slides) page.

## The planes

Each [plane](../glossary.md#plane) is one responsibility with one owner. The limits matter as much as the duties: no tool does another's job.

<div class="af-rules">
<div class="af-rule">
<b>Define</b>
<span>The team harness repo. ai-dlc contributes the optional workflow plugin and machine setup.</span>
<span><strong>Decides</strong> what a harness is: native files and <code>harness.lock</code>, frozen from a good hangar run, with one digest.</span>
<span><strong>Never</strong> runs anything.</span>
</div>
<div class="af-rule">
<b>Run</b>
<span>hangar</span>
<span><strong>Decides</strong> where work runs and how it reaches a branch.</span>
<span><strong>Never</strong> analyses runs or sets approval policy.</span>
</div>
<div class="af-rule">
<b>Judge</b>
<span>flightdeck</span>
<span><strong>Decides</strong> whether a change made agents better, with intervals.</span>
<span><strong>Never</strong> runs sandboxes or holds credentials.</span>
</div>
<div class="af-rule">
<b>Govern</b>
<span>Tower</span>
<span><strong>Decides</strong> whether a risky action may happen.</span>
<span><strong>Never</strong> enforces inside a sandbox.</span>
</div>
<div class="af-rule">
<b>Capability</b>
<span>MCP servers, Spaceport</span>
<span><strong>Decides</strong> what data and tools agents can reach.</span>
<span><strong>Never</strong> decides policy for agents.</span>
</div>
</div>

The choices behind this split are recorded on [Decisions](../decisions.md#the-planes-and-the-harness).
