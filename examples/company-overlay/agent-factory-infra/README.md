# agent-factory-infra (infra repo, template)

The factory's cloud resources, as code, on a GKE cluster your platform team already runs. It calls hangar's
`hangar-workload` module at the release `agent-factory-deploy` pins (`HANGAR_TAG`): hangar's service account and its
Workload Identity binding, the session and run buckets, and the ingress's static IP. It never creates a cluster,
a node pool or a registry you already have.

```sh
terraform init
terraform plan -var-file=env/dev.tfvars      # reviewed in the PR; your pipeline applies after merge
terraform output                             # the values agent-factory-deploy's overlays/dev/ take
```

The agent's role environment for this repo (`role-infra` in the team harness) has terraform and runs
`terraform validate` without a backend; it never runs `plan` against real state or `apply`. SRE approves every PR
here through `CODEOWNERS`, and the repo policy sets `self_approval: never`.

Replace `HANGAR_TAG`, the `env/*.tfvars` values and the backend. The module's inputs and outputs here follow hangar's
`deploy/terraform/modules/hangar-workload`; check its `variables.tf` at the tag you pin.
