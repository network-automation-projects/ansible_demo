# Terraform Lessons

Beginner-to-advanced Terraform practice: HCL, resources, variables, state, plan, modules, and running Terraform from Python.

## Overview

This lesson series is organized into four modules. Each module has a README (objectives and concepts), an `examples/` folder with minimal `.tf` or scripts, and an `exercises/` folder with tasks or TODOs.

## Prerequisites

- **Terraform** installed (e.g. `brew install terraform` or [terraform.io/downloads](https://www.terraform.io/downloads)). Verify with:
  ```bash
  terraform version
  ```
- Module 01 uses the `null` provider only (no cloud account required).

## Learning Path

| Module | Level | Focus |
|--------|--------|--------|
| [01_basics](01_basics/) | Beginner | What Terraform is; HCL; provider, resource, variable, output; init, plan, apply |
| [02_state_and_plan](02_state_and_plan/) | Intermediate | State (local backend); reading plan output; resource dependencies; built-in functions |
| [03_modules](03_modules/) | Intermediate | Module structure (inputs, outputs); calling modules; reusing modules |
| [04_python_integration](04_python_integration/) | Advanced | Running Terraform from Python (subprocess); parsing plan JSON; generating/validating tfvars |

## Setup

1. Install Terraform (see above).
2. Start with [01_basics](01_basics/): read the README, run `terraform init` and `terraform plan` in the examples directory, then try the exercises.

## Related Projects in This Repo

- **terraform-aws-demo-with-comments/** — Full Terraform AWS VPC project (modules, variables, outputs). Use as reference after the lessons.
- **coding-interview-challenges/terraform_python_driver/** — Python exercise: run terraform init/validate/plan from Python, parse plan summary; includes minimal config in `minimal/`.
- **coding-interview-challenges/terraform_plan_parser/** — Parse Terraform plan JSON (resource changes: add/change/destroy).
- **coding-interview-challenges/terraform_tfvars_from_python/** — Generate or validate `terraform.tfvars` from Python.

## License

For educational use. Use responsibly in production.
