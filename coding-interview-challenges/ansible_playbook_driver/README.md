# Ansible Playbook Driver (Python)

Practice exercise for **Ansible + Python** integration. Focus: run Ansible from Python via subprocess, handle exit codes and stdout, and parse the play recap.

## What You'll Use

- **subprocess:** `subprocess.run()` with `cwd`, `capture_output=True`, `text=True` (no `shell=True`)
- **pathlib:** `Path` for playbook/inventory paths
- **Regex:** Extract recap line `host : ok=N changed=N unreachable=N failed=N skipped=N rescued=N ignored=N`
- **Return codes:** Check `CompletedProcess.returncode` for success/failure

## Problem

1. **run_ansible_playbook(playbook_path, inventory_path, *extra_args)**  
   Run `ansible-playbook` with `-i inventory_path` and optional args (e.g. `-v`). Use `cwd` set to the directory containing the playbook so relative paths work. Return the `CompletedProcess` instance. Do not use `shell=True`.

2. **parse_play_recap(stdout)**  
   From playbook stdout, find the PLAY RECAP section and the line for each host (e.g. `localhost : ok=2 changed=0 ...`). Return a dict mapping hostname to counts, e.g. `{"localhost": {"ok": 2, "changed": 0, "unreachable": 0, "failed": 0, "skipped": 0, "rescued": 0, "ignored": 0}}`. If no recap found, return `{}` or `None`.

3. **main()**  
   From the exercise directory, run the included minimal playbook against the included minimal inventory (localhost only). Print success/failure for the run and, on success, print the parsed recap.

## Files

- **minimal/playbook.yml** – Single play: `hosts: localhost`, one or two tasks (ping, debug). No network devices or credentials.
- **minimal/inventory.yml** – Simple YAML inventory with one host (localhost) so the playbook runs without real servers.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and ensure Ansible is installed (`ansible-playbook --version`).
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory; check playbook run and recap output.
4. Compare with `solution.py`.

## Prerequisites

- **Ansible** (ansible-core or full Ansible) installed. No Python dependencies beyond the standard library.

## Example Recap Parsing

Input (snippet): `localhost : ok=2 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0`  
Output: `{"localhost": {"ok": 2, "changed": 0, "unreachable": 0, "failed": 0, "skipped": 0, "rescued": 0, "ignored": 0}}`
