# Module 02: State and Plan

Terraform state (what it is, local backend), reading plan output, resource dependencies, and built-in functions.

## Learning Objectives

- Understand what **state** is (mapping of config to real resource IDs) and where it lives (local file or remote backend)
- Read **plan** output: "Plan: N to add, N to change, N to destroy" and "No changes"
- Understand **resource dependencies** (implicit via references; explicit with `depends_on`)
- Use simple **built-in functions** (e.g. `timestamp()`, `cidrsubnet()` in more advanced configs)

## Concepts Covered

- **State**: Terraform stores a state file (by default `terraform.tfstate`) that maps resource addresses to real IDs and attributes. Needed for drift detection and updates. Backend can be local or remote (S3, etc.).
- **Plan**: `terraform plan` shows what would change: add/change/destroy counts. Output can go to stdout/stderr; often the summary line is at the end.
- **Dependencies**: If resource B references resource A (e.g. `id = aws_instance.foo.id`), Terraform creates A before B. Use `depends_on = [resource.x]` for ordering without attribute reference.
- **Functions**: `timestamp()`, `file()`, `cidrsubnet()`, etc. Used in expressions.

## Examples

- **examples/main.tf** — Minimal config (null_resource with trigger); run init and plan. Observe plan output and state file after apply.
- **examples/README_plan.md** — Short note on how to read plan output and where the summary line appears.

## Exercises

1. Run `terraform init`, `terraform plan`, and `terraform apply` in **examples/** (or 01_basics/examples). Inspect `terraform.tfstate` (JSON) to see how the resource is recorded.
2. (Optional) Parse the plan summary line in Python: write a small script that runs `terraform plan -no-color` and extracts "Plan: X to add, Y to change, Z to destroy" or "No changes." See **coding-interview-challenges/terraform_python_driver** for full exercise.

## See Also

- **coding-interview-challenges/terraform_python_driver** — Run terraform from Python, parse plan summary.
- **coding-interview-challenges/terraform_plan_parser** — Parse Terraform plan JSON (resource_changes).
