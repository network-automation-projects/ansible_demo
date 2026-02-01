# Parse Terraform Plan JSON

Practice exercise for **Terraform + Python**. Focus: load Terraform plan JSON (from `terraform show -json <planfile>` or a fixture), navigate the structure, and summarize resource changes (add / change / destroy).

## What You'll Use

- **json:** `json.load()` to read plan JSON from a file
- **pathlib:** `Path` for file paths
- **Dict navigation:** `plan["resource_changes"]`, each change’s `change["actions"]`
- **List comprehensions:** Build to_add, to_change, to_destroy from resource addresses

## Problem

1. **load_plan_json(path)**  
   Read the JSON file at `path`. Return the parsed dict. Handle `FileNotFoundError` (re-raise or return empty dict) and invalid JSON (catch `json.JSONDecodeError`, print message, re-raise or return empty dict).

2. **summarize_resource_changes(plan)**  
   From the plan’s `resource_changes` list, classify each resource by its `change.actions`:
   - **to_add:** `["create"]` only
   - **to_change:** `["update"]` or any update-in-place
   - **to_destroy:** `["delete"]` only, or replace (e.g. `["delete", "create"]`) — treat as destroy + add if you need both; for this exercise, put the address in to_destroy if "delete" is in actions.
   Return `(to_add, to_change, to_destroy)` — each a list of resource **address** strings (e.g. `module.networking.aws_vpc.this`). Use the `address` field of each change.

3. **main()**  
   Load the plan JSON from `plan_fixture.json` (or a path from CLI). Call `summarize_resource_changes` and print the three lists.

## Inputs and outputs

### What goes into main()

The script reads a **Terraform plan JSON file** (path from CLI or default `plan_fixture.json`). That file looks like this — a top-level object with `resource_changes`, each entry having `address` and `change.actions`:

```json
{
  "format_version": "1.0",
  "resource_changes": [
    {
      "address": "module.networking.aws_vpc.this",
      "change": { "actions": ["create"], "before": null, "after": { "cidr_block": "10.0.0.0/16" } }
    },
    {
      "address": "aws_instance.old_server",
      "change": { "actions": ["update"], "before": { "instance_type": "t2.micro" }, "after": { "instance_type": "t2.small" } }
    },
    {
      "address": "null_resource.deprecated",
      "change": { "actions": ["delete"], "before": { "id": "abc123" }, "after": null }
    }
  ]
}
```

### What gets printed (stdout)

Running `python solution.py` (or `python exercise.py`) with the above plan prints exactly:

```
To add: ['module.networking.aws_vpc.this', 'module.networking.aws_subnet.public[0]']  
To change: ['aws_instance.old_server']
To destroy: ['null_resource.deprecated']
```

Nothing is written to any file — only these three lines to stdout.

## Files

- **plan_fixture.json** – Minimal Terraform plan JSON (no AWS required). You can also use a real plan: `terraform plan -out=tfplan` then `terraform show -json tfplan > plan.json`.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `plan_fixture.json`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; check the printed to_add, to_change, to_destroy lists.
4. Compare with `solution.py`.

## Generating a real plan JSON

From a Terraform project directory:

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

Then run the script with `plan.json` as the path (e.g. via CLI arg).
