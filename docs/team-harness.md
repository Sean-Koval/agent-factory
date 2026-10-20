<span class="af-eyebrow">Agent factory · Define</span>

# Team harness

The harness as native files and a lock, frozen from a good run and promoted on evidence.

A team harness is everything that shapes how the team's coding agent works, kept in git and pinned by digest. Instructions, skills, hooks and plugins, the MCP servers it may call, the CLI version, the model and the approval mode.

The Define plane is not a tool or a spec. It is a git repository of the files each agent CLI already reads, plus one small `harness.lock`. hangar writes the lock from a turn that went well; there is no spec language and no compiler ([harness locks](https://sean-koval.github.io/hangar/harness-lock/)).

| | |
| --- | --- |
| Owns | `harnesses/<name>/` (native files and `harness.lock`), `channels.yaml`, the credential names in `bindings/`, the A/B suite and its decision, the behavior specs, the repo's CI. |
| Does not own | Running agents (hangar), judging changes (flightdeck), approval policy (Tower), or the workflow plugin's source (ai-dlc publishes it here). |
| Used by | The harness owner who freezes, tests and promotes; hangar, which thaws a channel for every claim; flightdeck, which compares channels. |
| Status | Lock, freeze, check and thaw are on main in hangar, and the example is public. The team's own repo and its first freeze are next. See [P2 on the roadmap](roadmap.md#p2-adopt-and-capture). |
| Docs site | None: the example's README is its documentation. |

[Example repository](https://github.com/Sean-Koval/team-harness){ .md-button .md-button--primary } [Harness locks in hangar](https://sean-koval.github.io/hangar/harness-lock/){ .md-button }

The example is built around a typical stack (OpenSpec, GitHub with Projects, Jira, Splunk and GKE) and holds nothing from a real organisation. It is its own repository, not a folder here, because hangar resolves older channel revisions from the git history of `harness.lock`.

## What's in it

```text
harnesses/team-default/
  CLAUDE.md                     the team's instructions (AGENTS.md is the same bytes, for Codex)
  skills/<name>/SKILL.md        openspec-change, github-pr, jira-ticket, splunk-logs, gke-diagnose
  native/claude-code/           settings.json (hooks and deny rules) and hooks/guard_readonly.py
  native/codex/ai-dlc-workflow/ the workflow plugin's Codex form: skills, hooks, an AGENTS fragment
  plugins/team-harness/         a Claude Code directory marketplace holding ai-dlc's workflow plugin
  harness.lock                  pins all of the above, plus the CLI version, model and MCP bindings
  env.stable.yaml, env.candidate.yaml   hangar environments rendered from the lock
channels.yaml                   team-default: {stable: sha256:…, candidate: sha256:…}
bindings/team-default.yaml      where each MCP credential comes from, by name
flightdeck/                     suite.yaml, decision.yaml, specs/, tasks/
```

## The lock and its digest

`harness.lock` has one component per file or directory, the CLI version, the concrete model, and a binding layer that holds names, never values. Abridged:

```yaml
schema: hangar.harness-lock/v1
name: team-default
revision: 4
runtime: {harness: claude-code, version: 2.1.296}
model: {id: claude-opus-5-5, policy: balanced}
components:
- {id: guide:CLAUDE.md, digest: sha256:2ac8…, path: CLAUDE.md}
- {id: skill:github-pr, digest: sha256:4991…, tree: sha256:7205…, path: skills/github-pr}
# … four more skills
- {id: plugin:ai-dlc-workflow@team-harness, digest: sha256:50cc…, tree: sha256:1fde…,
   path: plugins/team-harness/ai-dlc-workflow, enabled: true}
# … the Claude Code and Codex native files
binding:
  mcp: […]                          # github, gke, jira, splunk: transports, endpoints, header and env names
  permissions: {approvals: deny-risky}
plugins: {autoUpdate: false}
```

The harness's identity is `harness_digest`, a SHA-256 over the lock's identity fields. The name, revision and paths are not part of it. A turn run from the lock reports the same digest in its manifest, the PR trailer and every flightdeck report. `hangar harness check harnesses/team-default` recomputes every digest and prints it.

## Channels: stable and candidate

`channels.yaml` maps a channel to a `harness_digest`. In the example, `stable` is r1 (no workflow plugin) and `candidate` is r4 (the plugin on). hangar resolves `team-default@stable` to a digest and finds that lock in the checkout or its git history. Yesterday's harness stays runnable after the files move on.

```sh
# hangar server settings
HANGAR_HARNESS_REPO=https://github.com/Sean-Koval/team-harness   # hangar keeps its own full checkout
HANGAR_DEFAULT_HARNESS=team-default@stable                        # optional: what intake jobs run from

# anyone with a hangar token
hangar harness thaw team-default@stable --env team-default "Pick up ABC-123"
```

A thaw mounts the lock's files read-only into the sandbox; credentials come from the environment. Turn 1 is compared with the lock, and any difference is recorded as drift.

## From change to promotion

1. **A change becomes a candidate.** Someone edits the harness, here by turning on ai-dlc's workflow plugin. The PR re-pins the files (`hangar harness freeze` from a good run, or `scripts/relock.py` for a hand edit) and points `candidate` at the new digest. `stable` doesn't move.
2. **The candidate becomes an experiment.** `flightdeck/decision.yaml` is committed first: promote only if resolved tasks don't drop by more than 5 points, over at least 10 tasks. `flightdeck/suite.yaml` runs the same tasks on both arms, and the behavior specs judge how each arm worked. The example ships no tasks; mine them from the team's labelled failures.
3. **The experiment becomes a promotion, or doesn't.** flightdeck posts its report on the PR. If the verdict holds, a second person opens a one-line PR that sets `stable` to the candidate's digest. If the candidate is worse or the evidence is underpowered, `stable` stays, and the report says so.

## Where ai-dlc fits

ai-dlc contributes one optional component: its workflow plugin (workflow guidance, team skills and safety hooks). ai-dlc publishes it into the harness repo by PR; then `scripts/relock.py` re-pins and `candidate` moves. A harness doesn't need ai-dlc for anything else.

## Copy it

1. Fork [Sean-Koval/team-harness](https://github.com/Sean-Koval/team-harness), or clone it and push it to your own remote. Keep the history: channels resolve through it.
2. Replace the Splunk endpoint (`splunk.example.com`) with yours, adjust the skills, and set the credential names in `bindings/team-default.yaml`.
3. Install hangar at the commit the repo's CI pins (`HANGAR_REF` in `.github/workflows/check.yml`), then re-pin and regenerate:

    ```sh
    python scripts/relock.py harnesses/team-default --write
    python scripts/render_envs.py harnesses/team-default
    hangar harness check harnesses/team-default && python scripts/check_registry.py
    ```

4. Point `stable` at the new digest: the only time it moves without a promotion.
5. Freeze the real thing. Once a turn goes well, `hangar harness freeze <job> --out harnesses/team-default` replaces the hand-written pins with an observed run.

Every PR runs `hangar harness check`, `scripts/check_registry.py`, `flightdeck spec lint` and the hook tests, on a full-history checkout.
