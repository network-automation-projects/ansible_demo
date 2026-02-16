# Module 03: Modules

Module structure (inputs and outputs), calling a module from root config, and reusing existing modules.

## Learning Objectives

- Understand Terraform **modules**: reusable packages of resources with inputs (variables) and outputs
- Create a minimal module (e.g. one resource, one input, one output)
- Call the module from root configuration with `module "name" { source = "./path"; var = value }`
- Reference module outputs: `module.name.output_name`

## Concepts Covered

- **Module**: A directory containing `.tf` files (or a git/s3 source). Has **inputs** (variables) and **outputs** (output blocks). Root or another module calls it with `module "x" { source = "..." }`.
- **Source**: `source = "./modules/mymodule"` (local), or `source = "git::..."` / registry.
- **Passing values**: Set variables inside the `module "x" { }` block. Read outputs via `module.x.output_name`.
- **Composition**: Large configs are split into modules (e.g. networking, compute, security); root module wires them together.

## Examples

- **examples/root main.tf** — Root config that calls a local module.
- **examples/modules/minimal/** — Minimal module: one variable, one null_resource, one output.

Run from **examples** (root):

```bash
cd examples
terraform init
terraform plan
```

## Exercises

1. Create **exercises/modules/hello/** with:
   - **variables.tf**: one variable (e.g. `name`).
   - **main.tf**: one `null_resource` that uses the variable in its triggers.
   - **outputs.tf**: one output (e.g. resource id).
2. Create **exercises/main.tf** at root that calls the module: `module "hello" { source = "./modules/hello"; name = "world" }` and optionally outputs the module output.
3. Run `terraform init` and `terraform plan` from exercises.

## See Also

- **terraform-aws-demo-with-comments/** — Full AWS project with networking, security, and compute modules; clear dependency flow.
