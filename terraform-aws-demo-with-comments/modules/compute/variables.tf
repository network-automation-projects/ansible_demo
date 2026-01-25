variable "subnet_id" {
  description = "ID of the subnet where the EC2 instance will be launched"
  type        = string

  validation {
    condition     = can(regex("^subnet-", var.subnet_id))
    error_message = "Subnet ID must be a valid AWS subnet identifier (starts with 'subnet-')."
  }
}

variable "security_group_ids" {
  description = "List of security group IDs to attach to the EC2 instance"
  type        = list(string)

  validation {
    condition     = length(var.security_group_ids) > 0
    error_message = "At least one security group ID must be provided."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = can(regex("^[a-z0-9]+\\.[a-z0-9]+$", var.instance_type))
    error_message = "Instance type must be a valid AWS instance type (e.g., t2.micro, t3.small)."
  }
}

variable "aws_region" {
  description = "AWS region for AMI lookup"
  type        = string
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "ami_id" {
  description = "AMI ID to use for EC2 instance (leave empty to use latest Amazon Linux 2)"
  type        = string
  default     = ""
}
