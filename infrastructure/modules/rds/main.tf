
variable "app_name" {}
variable "environment" {}
variable "vpc_id" {}
variable "subnet_ids" {
  type = list(string)
}
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-${var.environment}-db-subnet"
  subnet_ids = var.subnet_ids
  tags       = { Name = "${var.app_name}-${var.environment}-db-subnet" }
}

resource "aws_security_group" "rds" {
  name        = "${var.app_name}-${var.environment}-rds-sg"
  description = "RDS PostgreSQL security group"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "${var.app_name}-${var.environment}-rds-sg" }
}

resource "aws_db_instance" "main" {
  identifier           = "${var.app_name}-${var.environment}-postgres"
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  storage_encrypted    = true
  db_name              = "devtools"
  username             = "postgres"
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  multi_az             = false
  publicly_accessible  = false
  skip_final_snapshot  = var.environment != "prod"
  tags                 = { Name = "${var.app_name}-${var.environment}-rds" }
}
