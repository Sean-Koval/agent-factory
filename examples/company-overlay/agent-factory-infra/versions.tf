terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.0"
    }
  }
  # Your state backend, e.g. a bucket the platform team owns:
  # backend "gcs" { bucket = "example-project-tfstate", prefix = "agent-factory" }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
