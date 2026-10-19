# The factory's cloud resources on a cluster the platform team already runs: hangar's namespace service account and
# its Workload Identity binding, the session and run (outbox) buckets, and the static IP for the ingress. The module
# is hangar's, at the same release the deploy repo pins; it never creates a cluster.
module "hangar" {
  source = "git::https://github.com/Sean-Koval/hangar.git//deploy/terraform/modules/hangar-workload?ref=HANGAR_TAG"

  project_id   = var.project_id
  region       = var.region
  cluster_name = var.cluster_name
  name_suffix  = var.environment
}
