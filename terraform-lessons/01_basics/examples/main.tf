# Terraform basics example (01_basics). No cloud provider; uses null provider.
terraform {
  required_version = ">= 1.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "example" {
  triggers = {
    label = "terraform-lessons-01"
  }
}
