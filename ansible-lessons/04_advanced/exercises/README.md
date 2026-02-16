# Exercises (04_advanced)

1. **Vault**
   - Run `ansible-vault create vault_vars.yml` and add one variable (e.g. `my_secret: "hello"`). Save and exit.
   - Create a playbook that uses `vars_files: [vault_vars.yml]` and prints the variable with debug. Run with `ansible-playbook ... --ask-vault-pass`.
   - See **ansible_demo** for full vault usage (vault/vault.yml, group_vars referencing vault).

2. **Python driver**
   - Implement `run_playbook(playbook_path, inventory_path)` that:
     - Runs `ansible-playbook` with subprocess (cwd = playbook directory).
     - Returns the CompletedProcess (or success boolean and recap string).
   - Parse the play recap line (e.g. "ok=2 changed=0 failed=0") from stdout or stderr.
   - Full exercise and solution: **coding-interview-challenges/ansible_playbook_driver**.
