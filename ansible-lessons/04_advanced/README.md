# Module 04: Advanced (Vault, Python Integration)

Ansible Vault for secrets; running playbooks from Python; parsing play recap.

## Learning Objectives

- Encrypt and decrypt files with Ansible Vault (`ansible-vault create/edit/view`)
- Run a playbook with vault-protected vars (`--ask-vault-pass` or `--vault-password-file`)
- Run `ansible-playbook` from Python (subprocess) and handle exit code and output
- Parse the play recap from playbook output (e.g. "ok=2 changed=0 unreachable=0 failed=0")

## Concepts Covered

- **Ansible Vault**: Encrypts YAML files (e.g. vars with passwords). Commands: `ansible-vault create file.yml`, `edit`, `view`, `encrypt`, `decrypt`. Use `--ask-vault-pass` or `--vault-password-file` when running playbooks that reference vault-encrypted vars.
- **Running from Python**: Use `subprocess.run(["ansible-playbook", "-i", inventory, playbook], cwd=..., capture_output=True, text=True)`. Check `returncode`; parse stdout/stderr for recap.
- **Play recap**: At the end of playbook output, Ansible prints a summary line per host (e.g. "localhost : ok=3 changed=0 unreachable=0 failed=0 skipped=0 ..."). Parsing this (e.g. with regex) lets you report success/failure programmatically.

## Examples

- **examples/inventory.yml** — Same localhost inventory.
- **examples/playbook.yml** — Minimal playbook (same as 01) for testing the Python runner.
- **examples/run_playbook.py** — Script that runs ansible-playbook via subprocess and prints return code and recap snippet. Run from this directory: `python examples/run_playbook.py`.

## Exercises

1. **Vault**: Create a vault-encrypted file (e.g. `exercises/vault_vars.yml`) with one variable. In a playbook, include it with `vars_files` and run with `--ask-vault-pass`. See **ansible_demo** for full vault usage.
2. **Python driver**: Implement (or adapt) a function `run_playbook(playbook_path, inventory_path)` that runs `ansible-playbook`, returns the subprocess result, and parses the last "PLAY RECAP" or summary line. Use or reference **coding-interview-challenges/ansible_playbook_driver** (exercise and solution).

## See Also

- **ansible_demo/** — Full project with Vault (vault/vault.yml), playbooks, and roles.
- **coding-interview-challenges/ansible_playbook_driver/** — Python exercise: run ansible-playbook from Python, parse play recap; includes minimal playbook and inventory.
