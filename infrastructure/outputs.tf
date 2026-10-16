


output "ecs_cluster_arn" {
  description = "ARN of the ECS cluster"
  value       = module.ecs.cluster_arn
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "gke_cluster_endpoint" {
  description = "GKE cluster API endpoint"
  value       = module.gke.cluster_endpoint
}

output "cdn_domain" {
  description = "Cloudflare CDN domain"
  value       = module.cdn.domain
}
