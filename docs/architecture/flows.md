# Flows

Each flow ends at a pull request or a report, and each step names the tool and what it hands on.

## A Jira ticket to a merged PR

1. An engineer moves the ticket to **Ready for agent**. A signed webhook reaches **hangar**.
2. hangar resolves the person and dedupes the ticket. The ticket text is untrusted, so the job is tainted from its first turn. A sender hangar can't link waits for an approval.
3. Admission applies budgets and fairness. Intake posture `enforce` requires the git gateway and an egress allowlist.
4. hangar claims a sandbox with the pinned harness, model and approvals, and records `hangar.manifest/v1` as the turn starts.
5. The agent works under `deny-risky` or `ask`. Questions go back to Jira and the engineer's inbox. Every step streams into `hangar.trace/v1`.
6. hangar runs the trusted verify and secret scan, pushes one commit through the gateway as the GitHub App, and opens the PR as a **draft** labelled `hangar:tainted`.
7. The reviewer gets an inbox item and a review packet.
8. An approval of the head commit by someone other than the requester, with green checks, arms auto-merge for exactly that commit. Once [hangar#172](https://github.com/Sean-Koval/hangar/issues/172) lands, landing also asks Tower and stores its receipt.
9. The merge lands in the trace and the outbox writes the run's objects.

## Improving the team harness

1. Change a skill, a hook, the guide or a plugin in the **[team harness repo](../team-harness.md)**. A change to ai-dlc's workflow plugin starts in **ai-dlc**: its build script regenerates the plugin and its content digest, and its publish script writes the plugin into the harness repo for a PR.
2. Re-pin the harness: `hangar harness freeze <job> --turn 1 --out harnesses/team-default` from a good run (or the repo's `relock.py` for a hand edit) writes the native files and a new `harness.lock` revision with a new `harness_digest`.
3. The PR points the `candidate` channel at the new digest; `stable` doesn't move.
4. `flightdeck experiment run suite.yaml` submits `hangar.experiment/v1` with the stable harness and the candidate as variants, after a cost gate.
5. hangar runs pinned trials with sealed graders. Infrastructure failures are retried and left out of the statistics.
6. `flightdeck report experiment --decision decision.yaml --post owner/repo#n` posts the paired verdict on the harness PR.
7. A PR moves the `stable` channel to the candidate, with an approver other than its author. Turn-one drift checks catch any mismatch in production.

## A risky action mid-run

1. The agent reads untrusted content: a web page, a remote MCP server, an outside host. hangar marks the turn and the session tainted.
2. A push from the sandbox fails: job sandboxes hold a fetch-only grant. The driver treats push, PR and MCP writes as risky.
3. Under `ask`, the request reaches the person through the inbox, MCP elicitation, Slack or Jira.
4. With Tower connected ([hangar#173](https://github.com/Sean-Koval/hangar/issues/173)), hangar asks for a `tool.call` decision with the arguments' hash, the taint and the digests. Cedar answers allow, deny or wait, and a waiting card goes to an approver who is not the requester.
5. A long wait suspends the turn and frees its slot; a signed event from Tower resumes it ([hangar#190](https://github.com/Sean-Koval/hangar/issues/190)).
6. hangar delivers; landing needs a different human and a receipt.
7. Tower reconciles hangar's tool-call spans against its receipts (Tower#20, [hangar#176](https://github.com/Sean-Koval/hangar/issues/176)).

## The nightly pipeline

1. At 01:00 ET the sandbox pools power down. Jobs queue and resume at 10:00. A turn cut by the power-down is an infrastructure error, retried at power-up.
2. All day the outbox has written each finished run once, retrying while storage is unreachable. Failures are kept until exported.
3. A Cloud Run compactor flattens the new objects into `flightdeck.parquet/v1`.
4. The harness canary proposes CLI lock bumps from contract tests.
5. `flightdeck check run` judges every behavior spec and accepted ADR check over the day and opens one GitHub issue per new step in violations, naming the `harness_digest` that changed. Scheduling it nightly is [flightdeck#15](https://github.com/Sean-Koval/flightdeck/issues/15).
6. In the morning, weekly metrics and the standup line go to Slack.

## Onboarding a repo

1. Optionally, ai-dlc bootstraps the engineer's machine. hangar work never needs it.
2. An admin adds the person and links their GitHub, Slack and Jira ids, and stores an API key. Subscription logins are refused for jobs.
3. `hangar connect` writes the MCP config for their client.
4. `hangar repo set OWNER/REPO --verify … --land auto_after_approval --approver LOGIN` (repeat `--approver` for each approver), then `hangar repo check OWNER/REPO`, which reports the App install, branch protection, gateway, sudo, egress, logins, Jira transitions and Slack mapping.
5. Map the doors: the Jira project, the GitHub `hangar` label, the Slack channel.
6. Point hangar at the team harness repo (`HANGAR_HARNESS_REPO`) and set `HANGAR_DEFAULT_HARNESS=team-default@stable`: intake jobs then run from the stable channel ([hangar#138](https://github.com/Sean-Koval/hangar/issues/138)).
