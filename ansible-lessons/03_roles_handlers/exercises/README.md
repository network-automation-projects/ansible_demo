# Exercises (03_roles_handlers)

1. Create a role **exercises/roles/greet/** with:
   - **tasks/main.yml**: at least one task (e.g. debug with a message).
   - **defaults/main.yml** (optional): variable `greet_name: "World"` and use it in the task.

2. Create **exercises/playbook.yml** that targets localhost and includes the role (use `roles: - greet` and set `roles_path` or run from a directory where `roles/` is next to the playbook).

3. Run from **exercises** directory so the `roles/` folder is found:
   ```bash
   cd exercises
   ansible-playbook -i ../examples/inventory.yml playbook.yml
   ```
