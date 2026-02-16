# TODO: Add terraform block and module block (see README)
terraform {
  required_version = ">= 1.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

module "hello" {
  source = "./modules/hello"
  name   = "world"
}

output "hello_id" {
  value = module.hello.resource_id
}
