


variable "app_name" {}
variable "environment" {}

resource "google_container_cluster" "main" {
  name     = "${var.app_name}-${var.environment}-gke"
  location = data.google_compute_zones.available.names[0]
  remove_default_node_pool = true
  initial_node_count       = 1
  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.main.name
  ip_allocation_policy {}
  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
  workload_identity_config {
    workload_pool = "${data.google_project.current.project_id}.svc.id.goog"
  }
  tags = ["${var.app_name}", var.environment]
}

resource "google_container_node_pool" "main" {
  name       = "${var.app_name}-${var.environment}-pool"
  location   = google_container_cluster.main.location
  cluster    = google_container_cluster.main.name
  node_count = 2
  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    tags = ["${var.app_name}", var.environment]
  }
}

resource "google_compute_network" "main" {
  name                    = "${var.app_name}-${var.environment}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main" {
  name          = "${var.app_name}-${var.environment}-subnet"
  ip_cidr_range = "10.1.0.0/24"
  region        = data.google_client_config.current.region
  network       = google_compute_network.main.id
}

data "google_project" "current" {}
data "google_client_config" "current" {}
data "google_compute_zones" "available" {
  region = data.google_client_config.current.region
}
