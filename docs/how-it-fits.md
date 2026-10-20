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

Agent factory is how a team of six runs about sixty coding-agent sessions without losing review or evidence. **hangar** (Run) takes work from many doors (Jira by default, GitHub, Slack, MCP, schedules) and runs each job in an isolated sandbox. The sandbox is pinned to a frozen **team harness**: a git directory of native files whose `harness.lock` yields one `harness_digest` (Define). Risky steps ask **Tower** (Govern), which answers allow, deny or wait. A wait goes to an approver who is not the requester, and every decision leaves a signed receipt. Every change leaves through one gate, a reviewed pull request, and every run is written once to a GCS outbox (on in the cluster with [hangar#273](https://github.com/Sean-Koval/hangar/issues/273)). **flightdeck** (Judge) compacts the outbox to Parquet and judges a harness change on paired, pinned trials, and a second person then promotes the candidate. **ai-dlc** supplies an optional workflow plugin and machine setup. **Spaceport** (frozen) serves governed data over MCP. **Airframe** gives every tool one look.

## A ticket's journey

1. An engineer moves ABC-123 to **Ready for agent** in Jira, the default door ([hangar#156](https://github.com/Sean-Koval/hangar/issues/156)).
2. hangar receives the signed webhook and marks the job tainted, because ticket text is untrusted. It admits the job within the budget and the reviewer's capacity: a person with five agent PRs waiting on review gets new jobs held ([hangar#159](https://github.com/Sean-Koval/hangar/issues/159)).
3. hangar claims a sandbox from `team-default@stable` (the intake default once `HANGAR_DEFAULT_HARNESS` is set) and records a manifest carrying its `harness_digest`. Every step streams into a trace.
4. When the agent needs something risky (a flagged tool call, a new host, a secret), hangar asks Tower. Tower answers allow, deny or wait, routes a wait to someone other than the requester, and signs a receipt. Tower's side is built; hangar's wiring is [hangar#172](https://github.com/Sean-Koval/hangar/issues/172) and [#173](https://github.com/Sean-Koval/hangar/issues/173), rolled out one kind at a time: off, then shadow, then enforce.
5. hangar runs the repo's own checks, pushes one commit through its gateway and opens a draft PR with a review packet and a `Harness-Digest:` trailer. A second human approves that exact commit, and hangar arms auto-merge for exactly that commit.
6. The finished run lands once in the outbox, and flightdeck's compactor turns it into Parquet overnight. Both are on main; switching them on in the GKE deploy is [hangar#273](https://github.com/Sean-Koval/hangar/issues/273).
7. When someone changes the harness, flightdeck runs stable against candidate on pinned trials and posts the verdict on the harness PR. A different person moves `stable`, and the next claim in step 3 uses it.

<figure class="af-figure af-journey--wide">
--8<-- "slide-planes.svg"
<figcaption>Four planes, one loop, one gate · <a href="assets/diagrams/journey.svg">the seven steps, numbered, full size</a></figcaption>
</figure>

<figure class="af-figure af-journey--stacked">
--8<-- "journey-stacked.svg"
<figcaption>The seven steps, numbered as above</figcaption>
</figure>

## Who does what

**Owns** means the tool defines and builds it; **uses** means it reads, calls or enforces it.

| Feature | hangar | Tower | flightdeck | Team harness repo | ai-dlc | Spaceport | agent-factory |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Doors, admission, inbox | owns | uses (approvals feed) | – | – | – | – | – |
| Sandboxes, sessions, jobs, turns | owns | – | – | – | – | – | – |
| Harness content and channels | uses (freeze, check, thaw) | – | uses (variants) | owns | uses (publishes the plugin) | – | – |
| Manifest, trace, outbox | owns | uses (reconciliation) | uses | – | – | – | – |
| Parquet data plane, statistics, specs, reports | – | – | owns | uses (specs, the decision file) | – | – | – |
| Trials and pin sets | owns (runs them) | – | owns (sampling) | – | – | – | – |
| Decision point, passports, receipts | uses (enforces) | owns | – | – | – | later | – |
| The PR gate and landing | owns | uses (landing approvals) | – | – | – | – | – |
| Workflow plugin, machine setup | – | – | – | uses | owns | – | – |
| Governed data over MCP | – | later | – | uses (binding) | – | owns (frozen) | – |
| Design system, suite docs, roadmap | uses | uses | uses | – | uses | – | owns |

## The seams

Each seam is a versioned file or API. [Contracts](architecture/contracts.md) links each one to the repository that defines it. Tower and Spaceport are private repositories, so their issues are written without links.

| Producer | Artifact or contract | Consumer | Status |
| --- | --- | --- | --- |
| Doors | Signed webhook, MCP `submit_job` | hangar intake | On main ([hangar#156](https://github.com/Sean-Koval/hangar/issues/156)) |
| hangar, from a good turn | `hangar harness freeze` writes native files and `harness.lock` (`hangar.harness-lock/v1`) | Team harness repo, by PR | On main ([hangar#133](https://github.com/Sean-Koval/hangar/issues/133)) |
| Team harness repo | Harness directory and `channels.yaml` (channel → `harness_digest`) | hangar `thaw`, a job's `harness_lock`, `HANGAR_DEFAULT_HARNESS` | On main ([hangar#134](https://github.com/Sean-Koval/hangar/issues/134), [#221](https://github.com/Sean-Koval/hangar/issues/221)); the team's own repo and first freeze: [hangar#138](https://github.com/Sean-Koval/hangar/issues/138) |
| ai-dlc | Workflow plugin and `plugin.lock.json`, pinned as `plugin:ai-dlc-workflow@team-harness` | Team harness repo | Plugin on main ([ai-dlc#191](https://github.com/Sean-Koval/ai-dlc/issues/191), [#193](https://github.com/Sean-Koval/ai-dlc/issues/193)); the team's harness consuming it: [hangar#139](https://github.com/Sean-Koval/hangar/issues/139) |
| hangar | `hangar.manifest/v1`, `hangar.trace/v1` | Outbox, flightdeck, Tower | On main; trace export to Tower: [hangar#176](https://github.com/Sean-Koval/hangar/issues/176) |
| hangar | Outbox `v1/runs/{date}/{session}.{run}/` (`hangar.run/v1`, `hangar.tests/v1`, `hangar.job_event/v1`; `run.json` last) | flightdeck compactor | On main ([hangar#163](https://github.com/Sean-Koval/hangar/issues/163)); on in the GKE deploy: [hangar#273](https://github.com/Sean-Koval/hangar/issues/273) |
| flightdeck compactor | `flightdeck.parquet/v1` | flightdeck statistics, specs, reports, weekly metrics | On main ([flightdeck#5](https://github.com/Sean-Koval/flightdeck/issues/5)) |
| flightdeck | `hangar.experiment/v1` | hangar | On main ([flightdeck#11](https://github.com/Sean-Koval/flightdeck/issues/11)); hangar records a pin set per variant |
| flightdeck | `hangar.pinset/v1` and `POST /api/trials` | hangar | hangar on main ([hangar#178](https://github.com/Sean-Koval/hangar/issues/178), cache [#180](https://github.com/Sean-Koval/hangar/issues/180)); flightdeck client: [flightdeck#25](https://github.com/Sean-Koval/flightdeck/issues/25) |
| flightdeck | Report against a pre-registered `decision.yaml`, posted on the PR | Harness PR, then a promotion PR (approver ≠ author) | On main ([flightdeck#9](https://github.com/Sean-Koval/flightdeck/issues/9)); the first real decision: [flightdeck#20](https://github.com/Sean-Koval/flightdeck/issues/20) |
| Team repos | `flightdeck.spec/v1`, ADR `checks:` | flightdeck `check run`, then issues | Language on main ([flightdeck#14](https://github.com/Sean-Koval/flightdeck/issues/14), [ai-dlc#207](https://github.com/Sean-Koval/ai-dlc/issues/207)); nightly runner: [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15) |
| hangar | `hangar.decision/v1` → `POST /v1/decisions` | Tower | Both sides built (Tower#13; hangar's client, [hangar#171](https://github.com/Sean-Koval/hangar/issues/171)); wiring: [hangar#172](https://github.com/Sean-Koval/hangar/issues/172), [#173](https://github.com/Sean-Koval/hangar/issues/173) |
| Tower | HMAC-signed `approval.*` events → `/api/governance/events` | hangar | Tower on main (Tower#17); hangar's receiver: [hangar#190](https://github.com/Sean-Koval/hangar/issues/190) |
| hangar sandbox | Workload token → RFC 8693 passport (15 minutes) | Tower | Exchange on main for `/mcp`; on `/hooks`: Tower#14; hangar's side: [hangar#174](https://github.com/Sean-Koval/hangar/issues/174) |
| Tower | Hash-chained receipts, `aw.attest/v1` attestation | Auditors, PRs | On main (Tower#18) |
| hangar | Review packet, `Harness-Digest:` trailer, inbox to Slack | Reviewers, engineers | On main ([hangar#137](https://github.com/Sean-Koval/hangar/issues/137), [#157](https://github.com/Sean-Koval/hangar/issues/157), [#158](https://github.com/Sean-Koval/hangar/issues/158)) |
| Spaceport | Four MCP tools | Agents, through an environment's binding | On main, frozen; asking Tower: spaceport#14 |
| agent-factory | Airframe `theme-vN` files, through `sync-airframe.sh` | Every tool repo | On main |

## Where to go next

- [Team harness](team-harness.md): the Define plane, with the example you can copy.
- [Architecture](architecture/index.md): the C4 views and where each container runs.
- [Flows](architecture/flows.md): the journey above in more detail, plus improving the harness, a risky action, the nightly pipeline and onboarding a repo.
- [Glossary](glossary.md): every term on this page.
