variable "project_id" {
  description = "The cloud project of the existing GKE cluster"
  type        = string
}

variable "region" {
  description = "Region of the cluster and the buckets"
  type        = string
}

variable "cluster_name" {
  description = "The existing GKE cluster hangar is installed into (this repo never creates one)"
  type        = string
}

variable "environment" {
  description = "dev or prod; names the service account and buckets"
  type        = string
}
