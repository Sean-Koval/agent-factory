<span class="af-eyebrow">At work</span>

# Run the factory at your company

From a ticket to a deployed change across a service's infra, code, database and deploy repos, on your own cluster, with your own approvers.

A company runs the same suite. hangar on its GKE cluster, its own fork of the team harness, and its own bot in the chat it already uses. What it adds is values, never code in the suite. Which repos make up a service, who approves each one, where secrets come from and which release runs.

Those values live in four private repositories of its own, laid out by the same convention as the services the agents work on.

| | |
| --- | --- |
| Templates | [`examples/company-overlay/`](https://github.com/Sean-Koval/agent-factory/tree/main/examples/company-overlay) (the factory's four repos) and [`examples/symphony-bot/`](https://github.com/Sean-Koval/agent-factory/tree/main/examples/symphony-bot) here; the `work-default` harness, role environments and an example change-set profile in [team-harness](https://github.com/Sean-Koval/team-harness). |
| Needs from hangar | Change sets (one ticket across several repos), the portable deploy package and `hangar apply`, the plugin host with events out, and delegated identity for the bot. These are in review; hangar has no release tag yet ([hangar#274](https://github.com/Sean-Koval/hangar/issues/274)), so `HANGAR_TAG` in the templates is the first one you pin. |
| Minimum first run | Change sets, the deploy package and these templates, driven from Claude Code with a hangar token. The Symphony bot adds the plugin host and delegated identity. |

[Company overlay](https://github.com/Sean-Koval/agent-factory/tree/main/examples/company-overlay){ .md-button .md-button--primary } [Symphony bot](https://github.com/Sean-Koval/agent-factory/tree/main/examples/symphony-bot){ .md-button }

## The four-repo convention

Each service is four repositories, and a ticket may touch any of them:

| Role | Holds | Who approves | The agent |
| --- | --- | --- | --- |
| **infra** | Terraform for the service's cloud resources | SRE, through `CODEOWNERS` | edits; runs `terraform validate` without a backend, never `plan` on real state or `apply` |
| **database** | Migrations | the database owners; `self_approval: never` | edits; runs migrations up, tests and down against a database service in its own sandbox |
| **code** | The service | the team | edits; runs the repo's own checks |
| **trigger-deployment** | Overlays and image pins per environment | whoever merges deploys | reads only; a deterministic step, not the agent, opens the deploy PR |

A **change-set profile** names the four repos, the environment that has every toolchain, and the order they land in. It lives in the factory's deploy repo, never in a service repo's `.hangar/`, which is the service's own and untrusted:

```yaml
schema: hangar.changeset-profile/v1
name: example-service
environment: work-multirepo
repos:
  infra:    {repo: example-org/example-service-infra}
  database: {repo: example-org/example-service-db}
  code:     {repo: example-org/example-service-app}
  deploy:   {repo: example-org/example-service-deploy, agent: read}
land_order: [database, infra, code]
deploy:
  role: deploy
  after: [database, infra, code]
  ready: {kind: image-ready, image: "registry.example.com/example-service/app", tag: "{code.merge_sha}"}
  apply: {kind: command, run: "./scripts/bump.sh dev {code.merge_sha}"}
  environments: [dev]
```

## From a ticket to a deploy

1. **Ask.** SVC-412 is in "Ready for agent". Someone says `@hangar do SVC-412` in a Symphony room. The bot calls hangar's MCP `submit_job` with the ticket and the profile, on behalf of that person, so the job is theirs. A person can make the same call from Claude Code or Antigravity.
2. **Admit.** hangar's limits apply; it resolves the profile and each repo's policy (verify, environment, approvers, naming). The Jira tracker moves the ticket to In Progress, and the room hears that the job is queued.
3. **Work.** One sandbox of `work-multirepo` from the harness `work-default@stable` clones the four repos to `/workspace/<role>`. The agent reads the ticket, plans across the roles with the `change-set` skill and edits `database/`, `infra/` and `code/`. A question goes to the room as a form, and the answer continues the turn.
4. **Deliver.** hangar runs each changed repo's own verify in its own checkout, then opens one PR per changed repo as the GitHub App. Each title carries the ticket key and each body a table of the sibling PRs. Each repo's push grant names only that repo.
5. **Land.** The database owners, SRE and a teammate approve their PRs; each repo's CI runs. hangar merges database, then infra, then code. A code PR approved first waits for the database PR. The room hears each landing, and the tracker comments on the ticket.
6. **Deploy.** Your CI builds the service image. Once `example-service/app:<merge sha>` exists, hangar runs the profile's deploy step in a fresh sandbox with no agent. It runs `bump.sh dev <sha>` on a branch of the deploy repo, then opens a PR under that repo's own policy. Its approvers merge it, your CD rolls dev, and the ticket moves to Done. Prod promotion stays yours.
7. **Capture.** The run lands in the outbox as `hangar.run/v1`, with the plugins and the profile's digest. flightdeck judges the harness on it like any other run.

If a PR in the set is closed unmerged, the set is broken. Later PRs stop, the deploy step never runs, and the room hears why. There is no automatic revert, and nothing merges across repos atomically.

## Installing it

1. **Infra.** `agent-factory-infra` calls hangar's `hangar-workload` module on the cluster you already run; it never creates one. Its outputs feed the deploy overlay.
2. **Image.** `agent-factory-bots` builds `FROM ghcr.io/sean-koval/hangar@sha256:…` with your pinned plugins and your harness fork's environments, and tags it with the merge commit. Mirror hangar's images by digest into your registry.
3. **Deploy.** `agent-factory-deploy` holds `overlays/{dev,prod}` over hangar's base at `HANGAR_TAG`, the `hangar-site` settings (doors, plugins, harness repo, egress), External Secrets for every credential, and `policy/`. CD applies the overlay, then `hangar apply -f policy/`.
4. **Harness.** Fork team-harness, set the credential names in `bindings/work-default.yaml`, and freeze `work-default` from a good run. `HANGAR_DEFAULT_HARNESS` points at its `stable` channel.
5. **A service.** Onboarding is one reviewed PR to the deploy repo: four repo policies, one profile, one Jira project entry.

## What stays open and what stays yours

The suite repositories ship mechanisms, schemas and templates; yours hold names, URLs, credentials, repo lists, approvers and pins. Nothing naming your company goes into a suite repository.

| Open: the suite | Yours |
| --- | --- |
| hangar's code, released images and tags, the kustomize base and components, the infra module | the tag and digest you run, your cluster, project, domains and buckets |
| The plugin surface `hangar.plugin/v1`, the built-in doors, notifiers and the `command` and `image-ready` deliverers | your plugins (a deploy bumper for your CD, a sign-in plugin for your IdP) and which are enabled |
| Schemas: repo policy, change-set profile, `hangar.event/v1`, the harness lock | your policies, approvers, profiles and landing orders |
| These templates, the bot template, the example harness | your bot's config, your harness fork, its locks and channels |
| | every secret, kept in your secret manager and passed to hangar by name |

## Questions to settle first

- Is the code on github.com or GitHub Enterprise Server? hangar recognizes github.com only today.
- What applies the deploy repo (Argo CD, Flux, a pipeline)? It decides the deploy bumper.
- How does your code CI tag images: by merge commit? The profile's `ready` step waits for that tag.
- Which database engine, and where do its test images live? The database role's service image comes from there.
- Can hangar verify Symphony's identity itself, or does it trust the bot to vouch for users?
