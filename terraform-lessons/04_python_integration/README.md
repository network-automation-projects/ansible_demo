# Module 04: Python Integration

Running Terraform from Python (subprocess), parsing plan output or plan JSON, and generating or validating tfvars.

## Learning Objectives

- Run `terraform init`, `terraform validate`, and `terraform plan` from Python using `subprocess`
- Parse the plan summary line ("Plan: N to add, N to change, N to destroy") or "No changes" from stdout/stderr
- Optionally parse Terraform plan JSON (`terraform show -json tfplan`) for resource changes
- Generate or validate `terraform.tfvars` from Python (e.g. write key=value format; check required keys)

## Concepts Covered

- **Subprocess**: Use `subprocess.run(["terraform", "init"], cwd=working_dir, capture_output=True, text=True)`. Same for `validate`, `plan`, `apply`. Check `returncode`; Terraform often sends plan text to stderr.
- **Parsing plan text**: Regex or string search for "Plan: X to add, Y to change, Z to destroy" or "No changes." Return a dict (e.g. `{"add": 1, "change": 0, "destroy": 0}`) or None.
- **Plan JSON**: `terraform plan -out=tfplan` then `terraform show -json tfplan` produces JSON with `resource_changes` (address, change.actions: ["create"], ["update"], ["delete"]). Parse for summaries.
- **tfvars**: Simple key=value or HCL. From Python: write a file with `key = "value"` lines; or read and validate that required keys exist.

## Examples

- **examples/run_terraform.py** — Runs `terraform init` and `terraform plan` in a minimal config directory; prints return code and plan summary snippet. Uses the **minimal/** config (copy of or link to 01_basics/examples or terraform_python_driver/minimal).
- **examples/minimal/** — Minimal Terraform config (null provider) so the script works without AWS.

## Exercises

1. Implement `run_terraform(working_dir, *args)` that runs `terraform` with the given args, `cwd=working_dir`, and returns the CompletedProcess. Handle stdout/stderr (Terraform may use stderr for plan).
2. Implement `parse_plan_summary(stdout_or_stderr_text)` that returns a dict like `{"add": N, "change": N, "destroy": N}` or None if "No changes."
3. (Optional) Generate `terraform.tfvars` from a Python dict (e.g. `region = "us-east-1"`) and write to file; or validate that an existing tfvars file contains required keys. See **coding-interview-challenges/terraform_tfvars_from_python**.

## See Also

- **coding-interview-challenges/terraform_python_driver** — Full exercise and solution: run_terraform, parse_plan_summary, minimal config.
- **coding-interview-challenges/terraform_plan_parser** — Parse plan JSON for resource_changes.
- **coding-interview-challenges/terraform_tfvars_from_python** — Generate or validate tfvars from Python.
