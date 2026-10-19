# agent-factory-deploy (trigger-deployment repo, template)

The factory's trigger-deployment repo: what runs where, at which version, with which settings, and the policy hangar
enforces. A merge here is the only way the factory changes. Your CD applies it; hangar never deploys itself.

```text
overlays/
  dev/  prod/
    kustomization.yaml     hangar's base and components at HANGAR_TAG, the image by digest
    hangar-deploy.yaml     values the components substitute (domain, buckets, service account, secret store)
    hangar-site.yaml       this company's hangar settings: doors, plugins, harness repo, egress
components/credentials/    the credentials, by name, that External Secrets mounts for hangar
policy/
  credentials/             hangar credentials whose value is a mounted file (never a value)
  repos/                   one repo policy per repo: verify, environment, landing, approvers, naming
  changesets/              change-set profiles: which repos a ticket spans and the order they land in
scripts/check.sh           CI: every overlay builds, and the policy applies cleanly (dry run)
```

## What CD does on a merge

1. `kustomize build overlays/<env> | kubectl apply -f -` (or Argo CD, Flux: whatever applies your other services).
2. `hangar apply -f policy/` against that install, with an admin token from your secret manager. It is
   declarative and idempotent: each object becomes what its file says, and one that already matches is left alone.
   A scheduled `hangar apply -f policy/ --check` exits 1 on drift (anything set by hand since, or a repo policy no
   file declares); `--prune` removes those policies.

## Common changes, each one reviewed PR

| Change | Files |
| --- | --- |
| Onboard a service (its four repos) | `policy/repos/<service>-{infra,db,app,deploy}.yaml`, `policy/changesets/<service>.yaml`, and a `projects` entry in `HANGAR_JIRA` |
| Add a credential | a key in `components/credentials/` and a file in `policy/credentials/`; the value goes into your secret manager |
| Upgrade hangar | `HANGAR_TAG` in both overlays' `kustomization.yaml`, and the image digest agent-factory-bots built from it |
| Promote dev to prod | copy the dev digest into `overlays/prod/kustomization.yaml` |
| Enable a plugin | its wheel in agent-factory-bots, its name in `HANGAR_PLUGINS.enable` |

Profiles never go in a target repo's `.hangar/`: that file is the repo's own and untrusted, and a pusher there must
not be able to reorder landing or skip a role's approvers.

## Placeholders

`example-org` (your GitHub organization), `example.com` and `example-project` (your domains and cloud project),
`HANGAR_TAG` and `BOTS_IMAGE_DIGEST` (the versions you pin), `company-secret-store` (your ClusterSecretStore).
