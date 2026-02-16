# Exercises (04_python_integration)

1. **run_terraform(working_dir, *args)**
   - Use `subprocess.run(["terraform", *args], cwd=working_dir, capture_output=True, text=True)`.
   - Return the `CompletedProcess` instance. Do not use `shell=True`.

2. **parse_plan_summary(text)**
   - From terraform plan output (stdout or stderr), extract:
     - "Plan: X to add, Y to change, Z to destroy" -> return `{"add": X, "change": Y, "destroy": Z}`.
     - "No changes. Your infrastructure matches..." -> return `{"add": 0, "change": 0, "destroy": 0}` or None.
   - Return None if pattern not found.

3. **Main block**
   - Run `terraform init` and `terraform plan -input=false` in a minimal config directory (e.g. **examples/minimal/** or **coding-interview-challenges/terraform_python_driver/minimal/**). Print success/failure and the parsed plan summary.

4. (Optional) **tfvars**: Write a function that generates `terraform.tfvars` from a Python dict, or validates that a tfvars file contains required keys. See **coding-interview-challenges/terraform_tfvars_from_python**.
