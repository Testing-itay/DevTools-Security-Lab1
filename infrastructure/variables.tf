

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "gcp_project" {
  description = "GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "db_password" {
  description = "Database password for RDS and Cloud SQL"
  type        = string
  sensitive   = true
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "devtools-lab"
}
