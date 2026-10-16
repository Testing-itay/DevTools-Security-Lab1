


variable "app_name" {}
variable "environment" {}
variable "db_password" {
  type      = string
  sensitive = true
}

resource "google_sql_database_instance" "main" {
  name             = "${var.app_name}-${var.environment}-sql"
  database_version = "POSTGRES_15"
  region           = data.google_client_config.current.region
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = null
    }
    backup_configuration {
      enabled            = true
      start_time         = "03:00"
      point_in_time_recovery_enabled = false
    }
  }
  deletion_protection = var.environment == "prod"
}

resource "google_sql_database" "main" {
  name     = "devtools"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "main" {
  name     = "postgres"
  instance = google_sql_database_instance.main.name
  password = var.db_password
}

data "google_client_config" "current" {}
