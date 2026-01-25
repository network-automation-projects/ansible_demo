variable "vpc_id" {
  description = "ID of the VPC where security groups will be created"
  type        = string

  validation {
    condition     = can(regex("^vpc-", var.vpc_id))
    error_message = "VPC ID must be a valid AWS VPC identifier (starts with 'vpc-')."
  }
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed for SSH access (use /32 for single IP)"
  type        = string

  validation {
    condition     = can(cidrhost(var.allowed_ssh_cidr, 0))
    error_message = "Allowed SSH CIDR must be a valid CIDR block."
  }
}

variable "allowed_http_cidr" {
  description = "CIDR block allowed for HTTP access"
  type        = string

  validation {
    condition     = can(cidrhost(var.allowed_http_cidr, 0))
    error_message = "Allowed HTTP CIDR must be a valid CIDR block."
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}
