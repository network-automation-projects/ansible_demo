# Reading plan output

- After `terraform plan`, look at the last lines. Terraform prints a summary like:
  - `Plan: 1 to add, 0 to change, 0 to destroy.`
  - Or: `No changes. Your infrastructure matches the configuration.`
- Plan output may go to stderr in some Terraform versions; when scripting, capture both stdout and stderr.
- For machine-readable plan: `terraform plan -out=tfplan` then `terraform show -json tfplan` to get plan JSON (see terraform_plan_parser exercise).
