# Exercises (03_modules)

1. Create a module in **exercises/modules/hello/**:
   - **variables.tf**: variable `name` (string).
   - **main.tf**: `null_resource` with trigger using `var.name`.
   - **outputs.tf**: output the resource id.

2. In **exercises/main.tf** (root):
   - terraform block with null provider.
   - `module "hello" { source = "./modules/hello"; name = "world" }`
   - Optional: output `module.hello.resource_id`.

3. Run from **exercises**:
   ```bash
   terraform init
   terraform plan
   ```
