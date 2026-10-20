---
hide:
  - navigation
  - toc
---

# Architecture

The suite follows the [C4 model](https://c4model.com/): this page is the system context, who uses the suite and what it depends on; [Containers](containers.md) is what runs where. [How it fits](../how-it-fits.md) follows one ticket through them. Both diagrams follow the page's light or dark theme; PNGs for slides are in [`docs/assets/diagrams`](https://github.com/Sean-Koval/agent-factory/tree/main/docs/assets/diagrams).

## System context

<figure class="af-figure">
--8<-- "c4-context.svg"
<figcaption>C4 level 1 · people, the suite and the systems around it · <a href="../assets/diagrams/c4-context.svg">full size</a></figcaption>
</figure>

Four kinds of people use the suite. **Engineers** hand off work and answer questions. **Reviewers** approve the exact commit that lands. The **harness owner** runs experiments and promotes the team harness. **Approvers** decide risky actions. The suite depends on GitHub for code and review, Jira and Slack as doors, model providers through API keys only, Google Cloud to run on, and MCP servers for the tools agents call.

## The planes

| Plane | Tool | Decides | Never does |
| --- | --- | --- | --- |
| Define | The team harness repo; ai-dlc contributes the optional workflow plugin and machine setup | What a harness is: native files and `harness.lock`, frozen from a good hangar run; one digest | Run anything |
| Run | hangar | Where work runs and how it reaches a branch | Analyse runs or set approval policy |
| Judge | flightdeck | Whether a change made agents better, with intervals | Run sandboxes or hold credentials |
| Govern | Tower | Whether a risky action may happen | Enforce inside a sandbox |
| Capability | MCP servers, Spaceport | What data and tools agents can reach | Decide policy for agents |
