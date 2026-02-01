# Terraform CLI Driver (Python)

Practice exercise for **Terraform + Python** integration. Focus: run Terraform from Python via subprocess, handle exit codes and stderr/stdout, and parse the plan summary line.

## Instructions
Remeber to brew install terraform before you start.

## What You'll Use

- **subprocess:** `subprocess.run()` with `capture_output=True`, `text=True`, `cwd`
- **pathlib:** `Path` for working directory
- **Regex:** Extract "Plan: X to add, Y to change, Z to destroy" from stdout
- **Return codes:** Check `CompletedProcess.returncode` for success/failure

## Problem

1. **run_terraform(working_dir, *args)**  
   Run `terraform` with the given args (e.g. `init`, `validate`, `plan`). Use `cwd=working_dir`, capture stdout and stderr as text. Return the `CompletedProcess` instance. Do not use `shell=True`.

2. **parse_plan_summary(stdout)**  
   From Terraform plan stdout, extract the line like "Plan: 1 to add, 0 to change, 1 to destroy." Return a dict e.g. `{"add": 1, "change": 0, "destroy": 1}` or `None` if the line is not found.

3. **main()**  
   From the exercise directory, run `terraform init` and `terraform validate` (or `terraform plan -input=false`) against the `minimal/` Terraform config. Print success/failure for each step and, for plan, print the parsed summary.

## Files

- **minimal/** – Minimal Terraform config (null_resource) so the exercise works without AWS.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and ensure Terraform is installed (`terraform version`).
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory; check init/validate/plan output.
4. Compare with `solution.py`.

## Prerequisites

- **Terraform** >= 1.0 (no cloud provider required for `minimal/`).
