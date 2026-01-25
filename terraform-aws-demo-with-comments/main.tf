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

  default_tags {
    tags = merge(
      {
        Project     = var.project_name
        Environment = var.environment
        ManagedBy   = "Terraform"
      },
      var.tags
    )
  }
}

# Networking Module - Core infrastructure (VPC, subnets, routing)
module "networking" {
  source = "./modules/networking"

  vpc_cidr           = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  availability_zone  = var.availability_zone
  aws_region         = var.aws_region
  enable_nat_gateway = var.enable_nat_gateway
  project_name       = var.project_name
  environment        = var.environment
}

# Security Module - Security groups and access policies
module "security" {
  source = "./modules/security"

  vpc_id            = module.networking.vpc_id
  allowed_ssh_cidr  = var.allowed_ssh_cidr
  allowed_http_cidr = var.allowed_http_cidr
  project_name      = var.project_name
  environment       = var.environment
}

# Compute Module - EC2 instance provisioning
module "compute" {
  source = "./modules/compute"

  subnet_id              = module.networking.private_subnet_id
  security_group_ids     = [module.security.web_security_group_id]
  instance_type          = var.instance_type
  aws_region             = var.aws_region
  project_name           = var.project_name
  environment            = var.environment
}
