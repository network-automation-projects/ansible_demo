# Module 02: Playbooks and Variables

Variables, conditionals, loops, and handlers in playbooks.

## Learning Objectives

- Use variables in playbooks (`vars`, `set_fact`, `register`)
- Organize variables with `group_vars` and `host_vars`
- Use conditionals (`when`) and loops (`loop`)
- Define handlers and trigger them with `notify`

## Concepts Covered

- **vars** (play or task level): Define variables for the play or a single task.
- **set_fact**: Set a variable during play execution (persists for the host for the rest of the play).
- **register**: Store the result of a task in a variable (e.g. `register: result`, then `result.stdout`).
- **group_vars/** and **host_vars/**: Directory-based variables per group or host (YAML files named after group or host).
- **when**: Condition for running a task (e.g. `when: result.rc == 0`).
- **loop**: Repeat a task with a list (e.g. `loop: [a, b, c]` or `loop: "{{ mylist }}"`).
- **Handlers**: Tasks that run only when notified; defined in `handlers:` section; triggered by `notify: handler name` in a task.

## Examples

- **examples/inventory.yml** — Groups and host vars (if needed).
- **examples/playbook_with_vars.yml** — Uses `vars`, `loop`, and `when`; optionally a handler.

Run from the **ansible-lessons** or **02_playbooks_variables** directory:

```bash
ansible-playbook -i examples/inventory.yml examples/playbook_with_vars.yml
```

## Exercises

1. Create a playbook that defines a variable `greeting: "Hello"` and uses it in a `debug` task.
2. Use `loop` to print three different messages (e.g. three hostnames or numbers).
3. Use `when` to run a task only when a variable (e.g. `run_extra`) is true.
4. (Optional) Add a handler (e.g. "restart something" as debug) and `notify` it from a task.

## See Also

- **coding-interview-challenges/ansible_playbook_parser** — Load playbook YAML in Python and list plays/tasks.
