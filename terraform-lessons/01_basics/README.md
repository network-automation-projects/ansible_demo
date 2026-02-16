# Module 01: Terraform Basics

What Terraform is, HCL syntax, provider and resource blocks, variables and outputs, and the basic workflow: init, plan, apply.

## Learning Objectives

- Understand what Terraform does (infrastructure as code, declarative, state)
- Read and write basic HCL (blocks, arguments)
- Use a **provider** (e.g. `null`) and a **resource** (e.g. `null_resource`)
- Define **variables** and **outputs**
- Run `terraform init`, `terraform plan`, and `terraform apply` (apply is optional with null_resource)

## Concepts Covered

- **HCL**: HashiCorp Configuration Language. Blocks like `resource "type" "name" { ... }`, `variable "name" { }`, `output "name" { }`.
- **Provider**: Plugin that talks to an API (e.g. AWS, null). Declared in `terraform { required_providers { ... } }`.
- **Resource**: A piece of infrastructure (e.g. `null_resource`, `aws_instance`). Has arguments and optional `triggers` for when to replace.
- **Variable**: Input value; can have default, type, description. Set via `terraform.tfvars`, `-var`, or env.
- **Output**: Value to show after apply; `terraform output`.
- **Workflow**: `terraform init` (download providers, init backend), `terraform plan` (preview changes), `terraform apply` (apply changes; use `-auto-approve` in automation).

## Examples

- **examples/main.tf** — Minimal config: null provider and one null_resource. No cloud account needed.
- **examples/variables.tf** (optional) — Example variable.
- **examples/outputs.tf** (optional) — Example output.

Run from **examples** directory:

```bash
cd examples
terraform init
terraform plan
# terraform apply   # optional; null_resource has no lasting effect
```

## Exercises

1. In **exercises/**, create a **main.tf** with:
   - `terraform { required_version = ">= 1.0"; required_providers { null = { source = "hashicorp/null", version = "~> 3.0" } } }`
   - One `resource "null_resource" "demo" { triggers = { label = "exercise" } }`
2. Run `terraform init` and `terraform plan` in the exercises directory.
3. Add a **variable** (e.g. "prefix") and use it in the resource triggers. Add an **output** that exposes something (e.g. the resource id).

## See Also

- **coding-interview-challenges/terraform_python_driver/minimal/** — Minimal Terraform config used by the Python driver exercise.
