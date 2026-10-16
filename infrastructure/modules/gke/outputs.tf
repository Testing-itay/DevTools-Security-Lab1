


output "cluster_endpoint" {
  value     = google_container_cluster.main.endpoint
  sensitive = true
}
