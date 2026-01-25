# Minimal example configuration
# This demonstrates the simplest possible usage of the terraform-aws-demo modules

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Networking Module
module "networking" {
  source = "../../modules/networking"

  vpc_cidr           = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  aws_region         = var.aws_region
  enable_nat_gateway = var.enable_nat_gateway
  project_name       = var.project_name
  environment        = var.environment
}

# Security Module
module "security" {
  source = "../../modules/security"

  vpc_id            = module.networking.vpc_id
  allowed_ssh_cidr  = var.allowed_ssh_cidr
  allowed_http_cidr = var.allowed_http_cidr
  project_name      = var.project_name
  environment       = var.environment
}

# Compute Module
module "compute" {
  source = "../../modules/compute"

  subnet_id          = module.networking.private_subnet_id
  security_group_ids = [module.security.web_security_group_id]
  instance_type      = var.instance_type
  aws_region         = var.aws_region
  project_name       = var.project_name
  environment        = var.environment
}

# Outputs
output "vpc_id" {
  value = module.networking.vpc_id
}

output "ec2_instance_id" {
  value = module.compute.instance_id
}

output "ec2_private_ip" {
  value = module.compute.private_ip
}
