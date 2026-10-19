# The factory's cloud resources on a cluster the platform team already runs: hangar's Google service account and its
# Workload Identity binding for hangar/hangar, the session and run (outbox) buckets, and the ingress's static IP. The
# module is hangar's, at the same release the deploy repo pins; it never creates a cluster or node pools.
module "hangar" {
  source = "git::https://github.com/Sean-Koval/hangar.git//deploy/terraform/modules/hangar-workload?ref=HANGAR_TAG"

  project_id       = var.project_id
  region           = var.region
  name             = "hangar-${var.environment}" # prefixes the service account, buckets and IP
  create_static_ip = true                        # for the ingress-gce component
  # registry = { create = false, repository_id = "agent-factory", location = "us" }   # to grant hangar an existing AR
}
