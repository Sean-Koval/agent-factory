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
<figcaption>Work comes in through the doors and the harness as a lock. hangar runs it, Tower decides, flightdeck judges, and the pull request is the one way out · <a href="assets/diagrams/journey.svg">the seven steps as a drawing</a></figcaption>
</figure>

<figure class="af-figure af-journey--stacked">
--8<-- "journey-stacked.svg"
<figcaption>The seven steps, numbered as in the list below</figcaption>
</figure>

## One ticket in seven steps

1. **Door.** An engineer moves ABC-123 to **Ready for agent** in Jira, the default door.
2. **Admit.** hangar receives the signed webhook, marks the job tainted (ticket text is untrusted) and admits it within budget.
3. **Claim.** hangar claims a sandbox pinned to `team-default@stable` and records a manifest carrying its `harness_digest`.
4. **Decide.** For anything risky the agent asks Tower: allow, deny or wait. A wait goes to a second person.
5. **Deliver.** hangar runs the repo's checks, pushes one commit and opens a draft PR. A second human approves that commit.
6. **Record.** The finished run lands once in the outbox, and flightdeck compacts it to Parquet overnight.
7. **Judge.** A harness change runs stable against candidate on pinned trials; flightdeck's verdict decides what `stable` becomes.

Each step's progress lives on the [roadmap](roadmap.md). Other starting points are on [Flows](architecture/flows.md): a harness change, a risky action, the nightly pipeline and onboarding a repo.

## Where a person steps in

Agents do the work between the steps. People see two things: a decision that waits for them, and the evidence behind a harness change.

<div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr))" markdown>
<figure class="af-figure af-figure--lead">
<a href="assets/captures/hangar-needs-you.png"><img src="assets/captures/hangar-needs-you-narrow-decision.png#only-dark" alt="hangar's Needs you with five items waiting. On top, approval HGR-JOB-VDTR: codex wants to push the refunds migration to main after reading untrusted content, with the command git push origin main, Deny, Allow for this turn and Approve push" width="720" height="512"></a>
<a href="assets/captures/hangar-needs-you-day.png"><img src="assets/captures/hangar-needs-you-narrow-day-decision.png#only-light" alt="hangar's Needs you with five items waiting. On top, approval HGR-JOB-VDTR: codex wants to push the refunds migration to main after reading untrusted content, with the command git push origin main, Deny, Allow for this turn and Approve push" width="720" height="512"></a>
<figcaption><b>Steps 4 and 5.</b> A push to main, held after the agent read untrusted content. The card shows the command, the branch and the expiry, with Deny, Allow for this turn and Approve push.</figcaption>
</figure>
<figure class="af-figure af-figure--lead">
<a href="assets/captures/flightdeck-verdict.png"><img src="assets/captures/flightdeck-verdict-verdict.png#only-dark" alt="flightdeck's report as a comment on the harness pull request. The verdict reads candidate is better than control on resolved, plus 21.2 points, above the pre-registered rule and an outcome table: control resolved 10 of 32, candidate 16 of 31" width="800" height="484"></a>
<a href="assets/captures/flightdeck-verdict-day.png"><img src="assets/captures/flightdeck-verdict-day-verdict.png#only-light" alt="flightdeck's report as a comment on the harness pull request. The verdict reads candidate is better than control on resolved, plus 21.2 points, above the pre-registered rule and an outcome table: control resolved 10 of 32, candidate 16 of 31" width="800" height="484"></a>
<figcaption><b>Step 7.</b> The verdict as a comment on the harness pull request: the pre-registered rule, each arm's resolved count and the paired difference.</figcaption>
</figure>
</div>

## Three rules hold it together

**Many doors, one inbox, one gate.** Work starts wherever people already are: a Jira status, a GitHub label, Slack, an MCP client. Questions and approvals come back to one inbox. Nothing reaches a branch except through a pull request a human approves.

**Each tool owns one plane.** hangar never analyses runs, flightdeck never runs sandboxes, Tower decides but never enforces, and ai-dlc stays off the agent's hot path. They meet only at versioned [contracts](architecture/contracts.md).

**Fail closed, measure everything.** Untrusted input taints a run and raises the bar to land it. Every run is written once to an outbox, so a harness change is judged on paired evidence rather than impressions.

## Who owns what

| Part | Plane | Owns |
| --- | --- | --- |
| [Team harness](team-harness.md) | Define | The harness as native files and `harness.lock`; its channels name which digest is `stable`. |
| [hangar](tools/hangar.md) | Run | Doors, admission, sandboxes, the manifest and trace, the outbox, trials and the PR gate. |
| [flightdeck](tools/flightdeck.md) | Judge | The Parquet data plane, paired statistics, behavior specs, pin sets and the report on the PR. |
| [Tower](tools/workspace.md) | Govern | The decision point, passports, approvals and hash-chained receipts. |
| [ai-dlc](tools/ai-dlc.md) | Setup | Engineers' machines and the optional workflow plugin a harness may pin. |
| [Spaceport](tools/spaceport.md) | Capability (frozen) | Governed data over four MCP tools. |
| agent-factory | Suite home | [Airframe](airframe/index.md), these docs, the [deck](deck.md) and the [roadmap](roadmap.md). |

The seams between them are versioned files and APIs. [Contracts](architecture/contracts.md) lists each one, who produces and consumes it, where it is defined and its status.

## Go deeper

- [Team harness](team-harness.md): the Define plane, with the example you can copy.
- [Architecture](architecture/index.md): the C4 views and where each container runs.
- [Flows](architecture/flows.md): improving the harness, a risky action, the nightly pipeline and onboarding a repo.
- [Glossary](glossary.md): every term on this page.
