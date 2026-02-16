# Module 03: Roles and Handlers

Reusable roles: directory layout, tasks, handlers, vars, templates, and using roles in a playbook.

## Learning Objectives

- Understand role directory structure (tasks/, handlers/, vars/, templates/, defaults/)
- Create a minimal role (e.g. "hello" role with one task and optional handler)
- Use the role in a playbook with `roles:` or `tasks:` + `include_role`

## Concepts Covered

- **Role**: A reusable unit: `roles/myrole/` contains `tasks/main.yml`, optional `handlers/main.yml`, `vars/main.yml`, `defaults/main.yml`, `templates/`. Playbooks reference roles by name.
- **tasks/main.yml**: Default list of tasks for the role.
- **handlers/main.yml**: Handlers used by this role (notified from role tasks).
- **vars/main.yml** and **defaults/main.yml**: Variables; defaults have lower precedence and can be overridden.
- **templates/**: Jinja2 templates (e.g. `.j2` files) used by the `template` module.
- **Using a role**: In a play, list under `roles: - myrole` or call `ansible.builtin.include_role: name: myrole`.

## Examples

- **examples/roles/hello/** — Minimal role: one task (debug) and optional handler. Playbook in **examples/playbook.yml** uses the role.

Run from this directory (parent of `roles/`):

```bash
ansible-playbook -i examples/inventory.yml examples/playbook.yml
```

## Exercises

1. Create a new role under **exercises/roles/** (e.g. `greet`) with:
   - `tasks/main.yml`: one or two tasks (e.g. set_fact and debug).
   - Optional: `defaults/main.yml` with a variable (e.g. `greet_name: "World"`).
2. Create **exercises/playbook.yml** that targets localhost and uses your role.
3. Run the playbook.

## See Also

- **ansible_demo/roles/cisco_backup/** — Full role structure (tasks, handlers, vars, templates) for network backup.
