


variable "app_name" {}
variable "environment" {}

variable "zone_name" {
  type    = string
  default = "example.com"
}

variable "origin_target" {
  type    = string
  default = "origin.example.com"
}

data "cloudflare_zone" "main" {
  name = var.zone_name
}

resource "cloudflare_record" "cdn" {
  zone_id = data.cloudflare_zone.main.id
  name    = "${var.app_name}-${var.environment}"
  content = var.origin_target
  type    = "CNAME"
  proxied = true
  ttl     = 1
}

resource "cloudflare_page_rule" "cache" {
  zone_id  = data.cloudflare_zone.main.id
  target   = "${var.app_name}-${var.environment}.${var.zone_name}/*"
  priority = 1
  actions {
    cache_level = "cache_everything"
    ssl        = "full"
  }
}
