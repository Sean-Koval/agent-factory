# Team harness (example) — moved

The example team harness now lives in its own repository:
**[Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness)**.

It moved because it is a registry, not just a directory: hangar resolves channels that aren't the current lock
(`team-default@stable` = r1) from the git history of `harnesses/team-default/harness.lock` relative to the repository
root, so it only works as a standalone repo. Its history is one commit per lock revision (r1 stable, r2 and r3, then r4
candidate with the ai-dlc workflow plugin), imported from this directory as it stood at
[`d59921b`](https://github.com/Sean-Koval/agent-factory/tree/d59921beeab0/examples/team-harness), and its own CI
(`hangar harness check`, `scripts/check_registry.py`, `flightdeck spec lint`, hook tests) runs there.

Make changes in that repository; this directory is kept only so old links land somewhere.
