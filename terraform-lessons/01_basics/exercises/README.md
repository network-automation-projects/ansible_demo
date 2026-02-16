# Exercises (01_basics)

1. Create **main.tf** with:
   - `terraform` block: `required_version = ">= 1.0"` and `required_providers` for `hashicorp/null` ~> 3.0.
   - One `resource "null_resource" "demo"` with `triggers = { label = "exercise" }`.

2. Run from this directory:
   ```bash
   terraform init
   terraform plan
   ```

3. Add **variables.tf** with one variable (e.g. `prefix`) and use it in the resource. Add **outputs.tf** with one output (e.g. resource id). Run `terraform plan` again.
