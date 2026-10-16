
variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "zone_name" {
  type    = string
  default = "example.com"
}

variable "origin_target" {
  type    = string
  default = "origin.example.com"
}
