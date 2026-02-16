# Exercises (02_state_and_plan)

1. In a directory with a minimal Terraform config (e.g. copy 01_basics/examples or use 01_basics/exercises), run:
   - `terraform init`
   - `terraform plan -no-color`
   - Observe the plan summary line. Optionally run `terraform apply -auto-approve` and then inspect `terraform.tfstate`.

2. (Optional) Python: Write a function that runs `terraform plan -no-color` (or `-input=false`) and parses the output for "Plan: N to add, N to change, N to destroy" or "No changes." Return a small dict or None. See **coding-interview-challenges/terraform_python_driver** for the full exercise and solution.
