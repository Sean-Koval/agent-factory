# Glossary

| Term | Meaning |
| --- | --- |
| Harness | Everything that shapes an agent apart from the model: instructions, skills, hooks, MCP servers, plugins and the CLI version. |
| `harness.lock` | A small file that pins a harness's parts by digest, next to its native files. |
| `harness_digest` | The one hash that identifies a harness, in the lock, the manifest, the PR trailer and every report. |
| Manifest | `hangar.manifest/v1`: the effective configuration captured when a turn starts. |
| Trace | `hangar.trace/v1`: OTLP spans for every step of a run, with tool kinds and shell operations. |
| Outbox | Cloud Storage objects written once per finished run, the input to flightdeck's data plane. |
| Door | A place where work starts: a Jira status, a GitHub label, Slack, an MCP client, a schedule. |
| Inbox | One list per person of reviews, questions, approvals and failures, delivered to Slack. |
| Taint | A mark on a turn or session that has read untrusted content; it raises the bar to push and land. |
| Intake posture | hangar's rule that intake jobs need the git gateway and an egress allowlist. |
| Trial | One attempt at one task with one variant, inside an experiment. |
| Sealed grader | A grading sandbox with no network, no credentials and hidden tests from a pristine copy. |
| `infra_error` | An outcome caused by infrastructure (preemption, power-down, rate limits); retried and excluded from statistics. |
| Behavior spec | A predicate over a trace, such as "tests run before a PR opens", judged per run. |
| Decision point | The workspace API hangar asks before releasing, landing or running a risky action. |
| Passport | A short-lived token the workspace issues in exchange for a workload token, with the requester as subject. |
| Receipt | A hash-chained record of a decision, attached to the action it allowed. |
| Airframe | The suite's design system; its tokens live in this repo's `theme/`. |
