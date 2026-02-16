# TODO: Add terraform block and null_resource (see README)
terraform {
  required_version = ">= 1.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "demo" {
  triggers = {
    label = "exercise"
  }
}
