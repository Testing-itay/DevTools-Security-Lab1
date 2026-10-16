


output "domain" {
  value = "${var.app_name}-${var.environment}.${var.zone_name}"
}
