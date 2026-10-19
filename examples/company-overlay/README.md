# Company overlay (template)

What a company holds to run the agent factory on its own cluster, as four repositories, one per directory. They
follow the same four-repo convention as the services the factory works on: **infra**, **code**, **database** and
**trigger-deployment**. Copy each directory into a private repository of your own; nothing in them names a real
organization, and everything you replace is a placeholder.

| Directory | Becomes | Holds |
| --- | --- | --- |
| [`agent-factory-infra/`](agent-factory-infra/) | `<company>/agent-factory-infra` | Terraform calling hangar's `hangar-workload` module on your existing GKE cluster: service account, Workload Identity, buckets, static IP |
| [`agent-factory-bots/`](agent-factory-bots/) | `<company>/agent-factory-bots` | The image you run (`FROM ghcr.io/sean-koval/hangar@sha256:…` plus pinned plugins), your plugins, the Symphony bot, your team-harness fork as a submodule |
| [`agent-factory-database/`](agent-factory-database/) | none in v1 | hangar keeps its state in SQLite on a volume |
| [`agent-factory-deploy/`](agent-factory-deploy/) | `<company>/agent-factory-deploy` | Kustomize overlays over hangar's base at a pinned tag, `hangar-site` settings, External Secrets, and `policy/` (repo policies, change-set profiles, credentials) that CD applies with `hangar apply` and `hangar changeset profile-set` |

Your fork of [team-harness](https://github.com/Sean-Koval/team-harness) is the fifth piece: the `work-default`
harness, the role environments (`role-infra`, `role-code`, `role-database`, `role-deploy`, `work-multirepo`) and
the channels.

## The boundary

The suite repositories ship versioned mechanisms, schemas and templates. Your repositories hold names, URLs,
credentials, repo lists, approvers and pins.

| Open (suite, `Sean-Koval/*`) | Closed (yours) |
| --- | --- |
| hangar's code, image and release tags; its kustomize base and components; the `hangar-workload` module | which tag and digest you run, your cluster, project, domains and buckets |
| The plugin surface (`hangar.plugin/v1`), built-in doors, notifiers and deliverers | your plugins (a deploy bumper, a sign-in plugin for your IdP) and which ones are enabled |
| Schemas: repo policy, change-set profile, `hangar.event/v1`, the harness lock | your repo policies, approvers, profiles and the order your repos land in |
| These templates, the Symphony bot template, the example team harness | your bot's config, your harness fork, its locks and channels |
| | every secret, which lives in your secret manager and reaches hangar by name |

Nothing naming your company goes into a `Sean-Koval/*` repository. A change to a mechanism goes there as a generic
change; a change to a value stays in yours.

## Placeholders to replace

`<company>` and `example-org` (your GitHub organization), `example.com` and `example-project` (domains, cloud
project), `HANGAR_TAG` (a hangar release tag), `HANGAR_IMAGE_DIGEST` and `BOTS_IMAGE_DIGEST` (image digests),
`company-secret-store` (your External Secrets ClusterSecretStore). The walkthrough from ticket to deploy, and what
each step needs, is on the suite site: [Run the factory at your company](https://sean-koval.github.io/agent-factory/work/).
