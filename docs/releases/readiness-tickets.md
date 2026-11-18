# Every 1.0 ticket

Every Jira ticket labelled `release:1.0`, sorted into three groups. A human-only ticket is `lane:human` or `needs-sean`: only Sean can move it. Agent-workable tickets can take a PR, though some wait on a person's step on the cluster. Checked on 18 November 2026. The exit criteria they serve are on [1.0 readiness](readiness.md).

| Group | Tickets |
| --- | --- |
| Done | 37 of 74 |
| Agent-workable | 23 of 74 |
| Human-only | 14 of 74 |

To list them yourself, search Jira for `labels = "release:1.0" ORDER BY Rank`.

## Human-only

<details markdown>
<summary>14 open tickets</summary>

| Ticket | Status | What it is | Next step |
| --- | --- | --- | --- |
| [KAN-21](https://seanmkoval.atlassian.net/browse/KAN-21) | To Do | Merge the ready PR queue | Merge the queue in the order posted on the ticket. |
| [KAN-22](https://seanmkoval.atlassian.net/browse/KAN-22) | To Do | Switch on the outbox and compactor with cloud credentials | Turn on the outbox and compactor with cloud credentials. |
| [KAN-23](https://seanmkoval.atlassian.net/browse/KAN-23) | To Do | Onboard repo 1 with two engineers | Onboard repo 1 and its two engineers. Waits on KAN-244 and KAN-214. |
| [KAN-24](https://seanmkoval.atlassian.net/browse/KAN-24) | To Do | Repos 2–3 and all six engineers | Repos 2 and 3, and all six engineers. Comes after KAN-23. |
| [KAN-25](https://seanmkoval.atlassian.net/browse/KAN-25) | To Do | Friday harness review and first 20 labelled failures | Start the Friday harness review and label the first 20 failures. |
| [KAN-68](https://seanmkoval.atlassian.net/browse/KAN-68) | To Do | hangar part B exit: six active delegators, every run captured, approvals enforced through Tower | hangar part B exit. Waits on adoption. |
| [KAN-146](https://seanmkoval.atlassian.net/browse/KAN-146) | To Do | Suite 1.0 exit: verify every criterion, tag 1.0 and publish what it includes | Verify every criterion, tag 1.0 and publish the 1.0 page. This tracker is agent-factory#61. |
| [KAN-141](https://seanmkoval.atlassian.net/browse/KAN-141) | To Do | Suite 1.0 · production release of hangar, Tower and flightdeck | The epic. It closes with KAN-146. |
| [KAN-214](https://seanmkoval.atlassian.net/browse/KAN-214) | To Do | Before onboarding: fund org API keys with spend caps, and get work infosec to sign off on where code and transcripts live | Fund org API keys with caps, and get infosec sign-off on data location. |
| [KAN-215](https://seanmkoval.atlassian.net/browse/KAN-215) | In Progress | Roadmap decisions: 1.0-rc date, surface cuts, licences, harnesses in 1.0, repo 1 and a second approver | The decision index. Only D6 (KAN-244) is still open. |
| [KAN-223](https://seanmkoval.atlassian.net/browse/KAN-223) | To Do | Fund and place the flightdeck#20 run: an API key with a $300 cap, a Docker hangar at main, and eval-window nights | Fund the flightdeck#20 run: a key with a $300 cap and eval nights. |
| [KAN-244](https://seanmkoval.atlassian.net/browse/KAN-244) | Needs Decision | Decide: repo 1, the two engineers, a second approver and power hours (D6) | Name repo 1, the two engineers, a second approver and the power hours. |
| [KAN-336](https://seanmkoval.atlassian.net/browse/KAN-336) | To Do | Turn on Tower's IAP header check: set iap.audience on the GKE deploy (KAN-173 L-5) | Set `iap.audience` on Tower's GKE deploy. |
| [KAN-536](https://seanmkoval.atlassian.net/browse/KAN-536) | Needs Decision | What spend cap per engineer should hangar ship with at work (monthly, and the daily, repo and job caps it implies)? | Pick the per-engineer spend cap. $400 a month stands if unanswered. |

</details>

## Agent-workable

<details markdown>
<summary>23 open tickets</summary>

| Ticket | Status | What it is | Next step |
| --- | --- | --- | --- |
| [KAN-27](https://seanmkoval.atlassian.net/browse/KAN-27) | To Do | Live intake check on the deployed safe release | hangar#482 adds the check. It runs once production is on a tag. |
| [KAN-32](https://seanmkoval.atlassian.net/browse/KAN-32) | In Review | Deploy Tower next to hangar | Code merged. A person applies Tower's deploy.md on the cluster. |
| [KAN-33](https://seanmkoval.atlassian.net/browse/KAN-33) | In Progress | Passports: Tower#14 then hangar#174, then hangar#172 shadow | Merged, off by default. A person deploys, then a shadow week. |
| [KAN-78](https://seanmkoval.atlassian.net/browse/KAN-78) | In Progress | Managed, fail-closed Tower hook in sandboxes (Claude Code; Codex where possible) | Repo side done on Docker; GKE and E2B refuse. Closing is Sean's call. |
| [KAN-54](https://seanmkoval.atlassian.net/browse/KAN-54) | To Do | Tower as hangar's governance plane: epic exit (one approval of each kind end to end) | tower#133 covers it in CI. The live run needs Tower deployed. |
| [KAN-88](https://seanmkoval.atlassian.net/browse/KAN-88) | To Do | Regression suite v1: mine tasks from the 20 labelled first failures | Regression v1. Waits on KAN-25's labels; moved to Next. |
| [KAN-31](https://seanmkoval.atlassian.net/browse/KAN-31) | To Do | flightdeck#20: change one real decision | flightdeck#110 readies the run. It waits on KAN-223. |
| [KAN-87](https://seanmkoval.atlassian.net/browse/KAN-87) | To Do | flightdeck v0 exit: the Judge plane changes one real decision within its line budget | flightdeck#112 checks the exit against main. Follows KAN-31. |
| [KAN-142](https://seanmkoval.atlassian.net/browse/KAN-142) | In Progress | Security review of hangar and Tower before 1.0 | Close the open mediums, then a reviewer signs the review. |
| [KAN-143](https://seanmkoval.atlassian.net/browse/KAN-143) | In Progress | Backup/restore drill and upgrade/rollback rehearsal for hangar and Tower | Tower's drills are in tower#135. A restore drill on GKE gives the real RTO. |
| [KAN-144](https://seanmkoval.atlassian.net/browse/KAN-144) | In Progress | SLOs, alerts, on-call owner and incident runbooks for hangar and Tower | Tower's SLOs (tower#108). A person turns alerting on and fires test alerts. |
| [KAN-145](https://seanmkoval.atlassian.net/browse/KAN-145) | In Progress | Release process: version and tag Tower and flightdeck; one checklist across the suite | The rc PRs are open: hangar, tower#134, flightdeck#111, agent-factory#60. Sean tags. |
| [KAN-66](https://seanmkoval.atlassian.net/browse/KAN-66) | To Do | hangar part A exit: safe release, harness definition, MCP split and cleanup | hangar part A exit review. |
| [KAN-167](https://seanmkoval.atlassian.net/browse/KAN-167) | In Progress | [Security M-2] Tower on GKE: audit export isn't tamper-evident (same volume as the DB, signing key in the pod) | tower#109 merged on 9 November. The ticket can close. |
| [KAN-172](https://seanmkoval.atlassian.net/browse/KAN-172) | In Review | [Security M-7] Scope hangar's GCP roles; give Tower its own AR repo and deploy it by digest | hangar#446 merged on 9 November. Check what's left, then close. |
| [KAN-174](https://seanmkoval.atlassian.net/browse/KAN-174) | In Progress | [Security Lows] hangar: dashboard CSP, pod hardening, egress default, gateway caps, branch reservation | Code merged. A person applies the L-10 Terraform. |
| [KAN-186](https://seanmkoval.atlassian.net/browse/KAN-186) | In Progress | [Security H-1] Run ask and deny-risky turns through the driver sidecar on GKE | Code merged. A person runs the check on a cluster. A stretch goal. |
| [KAN-216](https://seanmkoval.atlassian.net/browse/KAN-216) | In Progress | Show how far production is behind main: deployed SHA in doctor and the console, a lag alert, a named second approver | Repo side merged. A person names the second approver (KAN-244). |
| [KAN-218](https://seanmkoval.atlassian.net/browse/KAN-218) | To Do | Capacity rehearsal: 60 concurrent sessions on GKE on a stub harness, with cost per engineer-day from repo 1 | Capacity rehearsal on GKE. Needs the cluster. |
| [KAN-222](https://seanmkoval.atlassian.net/browse/KAN-222) | In Progress | Regression-v0: 20 rule-picked tasks from merged PRs, so KAN-31 doesn't wait on labelled failures | The suite is on main. team-harness#92 fixes three graders. |
| [KAN-275](https://seanmkoval.atlassian.net/browse/KAN-275) | In Review | CI: run the real Claude Code and Codex CLI tests nightly (governance hook, harden, verify gate) | hangar#478 meets the verify step and is waiting for review. |
| [KAN-291](https://seanmkoval.atlassian.net/browse/KAN-291) | In Review | Claude Code on Vertex AI as a first-class model route for team jobs | hangar#478 is waiting for review. A person runs one Vertex job. |
| [KAN-296](https://seanmkoval.atlassian.net/browse/KAN-296) | In Review | Data handling for a company install: audit retention, a tamper-evident audit sink, and per-person purge and export | Merged. The audit bucket check is a follow-up. |

</details>

## Done

<details markdown>
<summary>37 closed tickets</summary>

| Ticket | What it was |
| --- | --- |
| ✓ [KAN-20](https://seanmkoval.atlassian.net/browse/KAN-20) | Reject stale deploy run 39090659248 and approve the newest hangar deploy |
| ✓ [KAN-28](https://seanmkoval.atlassian.net/browse/KAN-28) | Tag v0.2.0 and publish the release |
| ✓ [KAN-74](https://seanmkoval.atlassian.net/browse/KAN-74) | Next hangar release enforces: remove HANGAR_INTAKE_POSTURE=warn and HANGAR_SUBSCRIPTION_LOGINS=any |
| ✓ [KAN-18](https://seanmkoval.atlassian.net/browse/KAN-18) | Honor https behind a TLS-terminating proxy (cookies, same-origin, OAuth redirect) |
| ✓ [KAN-57](https://seanmkoval.atlassian.net/browse/KAN-57) | Tower activity stream and per-run stop (stop reaches hangar as a signed run.stop event) |
| ✓ [KAN-77](https://seanmkoval.atlassian.net/browse/KAN-77) | hangar governance events receiver: suspend/resume turns on Tower approvals, honour run.stop |
| ✓ [KAN-79](https://seanmkoval.atlassian.net/browse/KAN-79) | Risky tool-call, egress and secret approvals ask Tower (new `governed` approval policy) |
| ✓ [KAN-86](https://seanmkoval.atlassian.net/browse/KAN-86) | Move hangar's evals/semver to flightdeck: port metrics and the rule labeller onto the data plane, then delete it from hangar |
| ✓ [KAN-83](https://seanmkoval.atlassian.net/browse/KAN-83) | Spike: grader/replay isolation on GKE, where there is no uid split |
| ✓ [KAN-70](https://seanmkoval.atlassian.net/browse/KAN-70) | Weekly metrics: reviewer attention per merged agent PR |
| ✓ [KAN-165](https://seanmkoval.atlassian.net/browse/KAN-165) | [Security H-1] GKE/E2B: ask and deny-risky turns don't bind the agent (no uid split, warn-only default) |
| ✓ [KAN-166](https://seanmkoval.atlassian.net/browse/KAN-166) | [Security M-1] Tower: cap request bodies before auth on unauthenticated endpoints |
| ✓ [KAN-168](https://seanmkoval.atlassian.net/browse/KAN-168) | [Security M-3] hangar broker: lease write-back lets a sandbox replace a stored team login |
| ✓ [KAN-169](https://seanmkoval.atlassian.net/browse/KAN-169) | [Security M-4] hangar: Codex ask turns bypassable through ~/.codex/rules, .codex/rules and approve MCP servers |
| ✓ [KAN-170](https://seanmkoval.atlassian.net/browse/KAN-170) | [Security M-5] hangar image: install from uv.lock with hashes, pin uv and base images, run non-root |
| ✓ [KAN-171](https://seanmkoval.atlassian.net/browse/KAN-171) | [Security M-6] Pin GitHub Actions by full SHA in privileged jobs (hangar and Tower) |
| ✓ [KAN-173](https://seanmkoval.atlassian.net/browse/KAN-173) | [Security Lows] Tower: dev-mode flag, agent-scoped hook runs, sign-in phishing, IAP assertion, OAuth receipts |
| ✓ [KAN-179](https://seanmkoval.atlassian.net/browse/KAN-179) | hangar CI security scanning: dependencies, image, secrets and static analysis |
| ✓ [KAN-180](https://seanmkoval.atlassian.net/browse/KAN-180) | GKE cluster hardening for 1.0: private nodes, secrets encryption, shielded nodes, in-transit encryption, deletion protection |
| ✓ [KAN-181](https://seanmkoval.atlassian.net/browse/KAN-181) | hangar security review packet for SRE and infosec: control map, findings status, accepted-risk register |
| ✓ [KAN-182](https://seanmkoval.atlassian.net/browse/KAN-182) | hangar audit log: export each entry off the pod to retained, write-once storage |
| ✓ [KAN-183](https://seanmkoval.atlassian.net/browse/KAN-183) | GKE node pools run as the Compute Engine default service account (CIS 5.2.1) |
| ✓ [KAN-185](https://seanmkoval.atlassian.net/browse/KAN-185) | Control-plane image: the apt layer (gcloud, docker CLI, buildx) is frozen by the build cache |
| ✓ [KAN-187](https://seanmkoval.atlassian.net/browse/KAN-187) | Driver sidecar: per-edit trees and the verify gate when the driver can't see the workspace |
| ✓ [KAN-189](https://seanmkoval.atlassian.net/browse/KAN-189) | [Security H-1] E2B: decide how ask and deny-risky turns run without a uid split |
| ✓ [KAN-198](https://seanmkoval.atlassian.net/browse/KAN-198) | Tower#14: accept hangar's passports on /v1 and /hooks (requester_claim, audiences, federation trust) |
| ✓ [KAN-219](https://seanmkoval.atlassian.net/browse/KAN-219) | Pre-onboarding doc fixes (split from KAN-81): no subscription logins for team work, Slack follow-up rule, runbooks README |
| ✓ [KAN-234](https://seanmkoval.atlassian.net/browse/KAN-234) | Experiment trials can't see the answer: clone at base_sha with no later refs, and closed egress by default for eval jobs |
| ✓ [KAN-239](https://seanmkoval.atlassian.net/browse/KAN-239) | Decide: what 1.0 means and when (D1) |
| ✓ [KAN-240](https://seanmkoval.atlassian.net/browse/KAN-240) | Decide: surface cuts for 1.0 (D2) |
| ✓ [KAN-241](https://seanmkoval.atlassian.net/browse/KAN-241) | Decide: feature freeze until adoption (D3) |
| ✓ [KAN-242](https://seanmkoval.atlassian.net/browse/KAN-242) | Decide: which licences the work org already has, and the bake-off (D4) |
| ✓ [KAN-243](https://seanmkoval.atlassian.net/browse/KAN-243) | Decide: which harnesses 1.0 supports (D5) |
| ✓ [KAN-245](https://seanmkoval.atlassian.net/browse/KAN-245) | Decide: flightdeck scope for 1.0 (D7) |
| ✓ [KAN-290](https://seanmkoval.atlassian.net/browse/KAN-290) | Spend guardrails on by default before onboarding: job budget, repo and person daily caps, and a spend alert |
| ✓ [KAN-294](https://seanmkoval.atlassian.net/browse/KAN-294) | SSO sign-in for hangar's console and API (OIDC, with IAP as an option) and IdP-driven deprovisioning |
| ✓ [KAN-333](https://seanmkoval.atlassian.net/browse/KAN-333) | [Security L-3] Tower's passport hook path still names runs from 8 chars of the session id; use hook_run_id() |

</details>

