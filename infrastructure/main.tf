

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

module "vpc" {
  source     = "./modules/vpc"
  app_name   = var.app_name
  environment = var.environment
}

module "rds" {
  source      = "./modules/rds"
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
  db_password = var.db_password
}

module "ecs" {
  source      = "./modules/ecs"
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
}

module "gke" {
  source      = "./modules/gke"
  app_name    = var.app_name
  environment = var.environment
}

module "cloud_sql" {
  source      = "./modules/cloud-sql"
  app_name    = var.app_name
  environment = var.environment
  db_password = var.db_password
}

module "cdn" {
  source      = "./modules/cdn"
  app_name    = var.app_name
  environment = var.environment
}
