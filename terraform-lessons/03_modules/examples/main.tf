# Root config calling a local module (03_modules).
terraform {
  required_version = ">= 1.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

module "minimal" {
  source = "./modules/minimal"
  label  = "from-root"
}

output "module_output" {
  value = module.minimal.resource_id
}
