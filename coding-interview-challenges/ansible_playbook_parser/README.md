# Ansible Playbook and Inventory Parser (Python)

Practice exercise for **Ansible + Python** without running Ansible. Focus: load playbook and inventory YAML in Python and answer structural questions (plays, tasks, host groups). Proves understanding of playbook and inventory layout.

## What You'll Use

- **PyYAML:** `yaml.safe_load()` for playbook and inventory.
- **Dict/list navigation:** Plays are a list of dicts; each play has `hosts`, `tasks`, `name`, etc. Inventory has `all.children`, `all.hosts`, or direct `hosts` under groups.
- **pathlib:** Resolve paths to sample files.

## Problem

1. **load_playbook(path)**  
   Load YAML from path; return list of plays (list of dicts). If the file is a single play (one dict), return `[play]`. Handle missing file (raise or return empty list per your convention).

2. **list_tasks_from_play(play)**  
   Given one play dict, return a list of task names. A task can have `name`, or be a block with `block` containing tasks; flatten one level (tasks inside a block get their names). Return list of strings; use `"unnamed"` when `name` is missing.

3. **load_inventory(path)**  
   Load inventory YAML from path; return the raw structure (dict). Handle missing file (raise or return empty dict).

4. **list_hosts_in_group(inventory, group_name)**  
   Given the loaded inventory dict and a group name (e.g. `"web"` or `"all"`), return a list of host names in that group. Handle common structures: `all.children.<group>.hosts` (YAML inventory) and `all.hosts` for ungrouped. Return empty list if group not found.

5. **main()**  
   Load sample playbook and inventory from the exercise directory; print plays (names), tasks per play, and hosts per group. Use the included sample files so it runs without your real Ansible repo.

## Files

- **sample_playbook.yml** – Small playbook (e.g. 2 plays, a few tasks each) with clear `name` and `hosts`.
- **sample_inventory.yml** – Small inventory (e.g. `all.children.web.hosts`, `all.children.db.hosts`) so `list_hosts_in_group` is testable.
- **exercise.py** – Skeleton with TODOs; implement the five pieces yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and install PyYAML: `pip install pyyaml` (or `pip install -r requirements.txt`).
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory; check plays, tasks, and hosts output.
4. Compare with `solution.py`.

## Prerequisites

- **PyYAML:** `pip install pyyaml` (see `requirements.txt` in this directory).

## Example

- `list_tasks_from_play(play)` for a play with tasks named "Ping" and "Debug" → `["Ping", "Debug"]`.
- `list_hosts_in_group(inv, "web")` → `["web1", "web2"]` from sample inventory.
