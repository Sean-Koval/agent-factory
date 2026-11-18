# 1.0 decisions

Which of Sean's 1.0 decisions are made, and which still block work? The rulings come from KAN-215's decision tickets and KAN-536. Checked on 18 November 2026. The criteria they shape are on [1.0 readiness](readiness.md).

| Decision | Ticket | Status | Ruling |
| --- | --- | --- | --- |
| D1: what 1.0 means and when | KAN-239 | Decided | Option 1: rc on 24 November 2026, full 1.0 after adoption. |
| D2: surface cuts | KAN-240 | Decided | A2A, `/e2b`, the Projects door and `gemini` are removed. |
| D3: feature freeze | KAN-241 | Decided | Until KAN-23's engineers merge 3 agent PRs each; backstop 20 November 2026. |
| D4: licences | KAN-242 | Decided | The work org has Claude, some Vertex and Jira; no Copilot or Codex, so there's no bake-off. |
| D5: harnesses in 1.0 | KAN-243 | Decided | As recommended: Claude Code fully, Codex for ungoverned jobs. |
| D6: repo 1, engineers, a second approver, power hours | KAN-244 | Needs decision | Blocks KAN-23, KAN-144's backup on-call and KAN-216. |
| D7: flightdeck scope | KAN-245 | Decided | KAN-31 runs on regression-v0; team benchmarks are digested task sets. |
| Spend cap per engineer | KAN-536 | Needs decision | $400 a month stands if unanswered. Due before KAN-23. |

Two are open, and both are due before work onboarding (KAN-23). KAN-215, the index ticket, can close once D6 is decided.
