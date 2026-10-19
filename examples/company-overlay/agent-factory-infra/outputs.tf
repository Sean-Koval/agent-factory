# The values agent-factory-deploy's overlays/<environment>/hangar-deploy.yaml and hangar-site.yaml take.
output "gcp_service_account" {
  value = module.hangar.gcp_service_account
}

output "run_bucket_url" {
  value = module.hangar.run_bucket_url
}

output "session_bucket_url" {
  value = module.hangar.session_bucket_url
}

output "static_ip_name" {
  value = module.hangar.static_ip_name
}
