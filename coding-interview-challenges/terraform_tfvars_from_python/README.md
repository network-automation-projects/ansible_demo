# Generate or Validate terraform.tfvars from Python

Practice exercise for **Terraform + Python**. Focus: convert a Python dict to HCL tfvars format, write it to a file, and validate that a tfvars file contains required variable keys (simple key=value parsing).

## What You'll Use

- **pathlib:** `Path` for file paths
- **String formatting:** Build lines like `key = "value"` or `key = 123` or `key = true`
- **File I/O:** `open()` with UTF-8; read lines, strip, split on first `=`
- **Types:** Strings quoted in tfvars; numbers and booleans unquoted. Keys sorted for stable output.

## Problem

1. **dict_to_tfvars(variables)**  
   Convert a flat dict `{str: str | int | bool}` to HCL tfvars content. Each line: `key = value`. Strings in double quotes; numbers and booleans unquoted. Sort keys for stable output.

2. **write_tfvars(path, variables)**  
   Write the result of `dict_to_tfvars(variables)` to `path`. Use UTF-8.

3. **validate_tfvars_keys(path, required)**  
   Read the file at `path`. Assume simple key=value lines (first `=` splits key and value; strip both). Skip blank lines and lines starting with `#`. Return `(all_required_present, missing_keys)` where `missing_keys` is the set of required keys not found in the file.

4. **main()**  
   Build a sample dict (e.g. `aws_region`, `instance_type`, `enable_nat_gateway`). Write `terraform.tfvars` in the script directory. Then validate that required keys (e.g. `aws_region`, `instance_type`) are present and print the result.

## Files

- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; check the generated file and validation output.
4. Compare with `solution.py`.

## tfvars format notes

- Strings: `key = "value"` (escape internal double quotes if needed).
- Numbers: `key = 42` or `key = 3.14`.
- Booleans: `key = true` or `key = false` (lowercase, unquoted).
