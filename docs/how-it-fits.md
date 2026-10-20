---
hide:
  - navigation
  - toc
---

# How it fits

<style>
  /* The journey has a wide drawing and a stacked one; phones and narrow tablets get the stacked one. */
  .af-journey--stacked { display: none !important; }
  @media (max-width: 959px) {
    .af-journey--wide { display: none !important; }
    .af-journey--stacked { display: block !important; max-width: 26rem; }
  }
</style>

One ticket, four planes, one gate. The team harness defines what the agents run, hangar runs them, flightdeck judges the runs and Tower governs the risky decisions. Every change leaves through a reviewed pull request.

<figure class="af-figure af-journey--wide">
--8<-- "slide-planes.svg"
<figcaption>Four planes, one loop, one gate · <a href="assets/diagrams/journey.svg">the seven steps, numbered, full size</a></figcaption>
</figure>

<figure class="af-figure af-journey--stacked">
--8<-- "journey-stacked.svg"
<figcaption>The seven steps, numbered as below</figcaption>
</figure>

## A ticket's journey

1. An engineer moves ABC-123 to **Ready for agent** in Jira, the default door.
2. hangar receives the signed webhook, marks the job tainted (ticket text is untrusted) and admits it within budget.
3. hangar claims a sandbox pinned to `team-default@stable` and records a manifest carrying its `harness_digest`.
4. For anything risky the agent asks Tower: allow, deny or wait. A wait goes to a second person.
5. hangar runs the repo's checks, pushes one commit and opens a draft PR. A second human approves that commit.
6. The finished run lands once in the outbox, and flightdeck compacts it to Parquet overnight.
7. A harness change runs stable against candidate on pinned trials; flightdeck's verdict decides what `stable` becomes.

Each step's progress lives on the [roadmap](roadmap.md); the flows that start elsewhere (a harness change, a risky action, the nightly pipeline, onboarding a repo) are on [Flows](architecture/flows.md).

## Three rules

**Many doors, one inbox, one gate.** Work starts wherever people already are: a Jira status, a GitHub label, Slack, an MCP client. Questions and approvals come back to one inbox, and nothing reaches a branch except through a pull request a human approves.

**Each tool owns one plane.** hangar never analyses runs, flightdeck never runs sandboxes, Tower decides but never enforces, and ai-dlc stays off the agent's hot path. They meet only at versioned [contracts](architecture/contracts.md).

**Fail closed, measure everything.** Untrusted input taints a run and raises the bar to land it. Every run is written once to an outbox, so a harness change is judged on paired evidence rather than impressions.

## Who owns what

- **Team harness** (Define): the harness as native files and `harness.lock`; its channels name which digest is `stable`.
- **hangar** (Run): doors, admission, sandboxes, the manifest and trace, the outbox, trials, and the PR gate.
- **flightdeck** (Judge): the Parquet data plane, paired statistics, behavior specs, pin sets and the report on the PR.
- **Tower** (Govern): the decision point, passports, approvals and hash-chained receipts.
- **ai-dlc** (Setup): engineers' machines and the optional workflow plugin a harness may pin.
- **Spaceport** (also in the suite, frozen): governed data over four MCP tools.
- **agent-factory**: Airframe, these docs, the deck and the roadmap.

The seams between them are versioned files and APIs. [Contracts](architecture/contracts.md) lists each one, who produces and consumes it, where it is defined and its status.

## Where to go next

- [Team harness](team-harness.md): the Define plane, with the example you can copy.
- [Architecture](architecture/index.md): the C4 views and where each container runs.
- [Flows](architecture/flows.md): improving the harness, a risky action, the nightly pipeline and onboarding a repo.
- [Glossary](glossary.md): every term on this page.
