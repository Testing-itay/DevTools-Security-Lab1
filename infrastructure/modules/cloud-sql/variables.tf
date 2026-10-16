


variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}
