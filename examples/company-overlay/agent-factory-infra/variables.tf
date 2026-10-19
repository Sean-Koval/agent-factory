variable "project_id" {
  description = "The cloud project of the existing GKE cluster hangar runs in (this repo never creates one)"
  type        = string
}

variable "region" {
  description = "Region of the cluster and the buckets"
  type        = string
}

variable "environment" {
  description = "dev or prod; names the service account and buckets"
  type        = string
}
