# Minimal Terraform config for terraform_python_driver exercise.
# No cloud provider; uses null_resource so init/validate/plan work offline.

terraform {
  required_version = ">= 1.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "exercise" {
  triggers = {
    always = timestamp()
  }
}
