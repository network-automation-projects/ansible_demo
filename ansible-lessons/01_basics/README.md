# Module 01: Ansible Basics

What Ansible is, how inventory and playbooks work, and how to run your first playbook.

## Learning Objectives

- Understand what Ansible is (agentless automation, YAML playbooks, inventory)
- Write a simple inventory (hosts and groups)
- Run ad-hoc commands with `ansible -m ping`
- Write a minimal playbook (hosts, tasks, ping, debug)
- Run a playbook with `ansible-playbook -i inventory playbook.yml`

## Concepts Covered

- **Inventory**: Defines hosts and groups. Can be a single file (e.g. `inventory.yml`) or directory. Each host can have `ansible_host`, `ansible_connection`, etc.
- **Ad-hoc**: One-off commands, e.g. `ansible all -i inventory.yml -m ping`.
- **Playbook**: YAML file with one or more **plays**. Each play has `hosts`, optional `gather_facts`, and a list of **tasks**. Tasks use **modules** (e.g. `ansible.builtin.ping`, `ansible.builtin.debug`).
- **Running a playbook**: `ansible-playbook -i inventory.yml playbook.yml` (from the directory containing the playbook so relative paths work).

## Examples

- **examples/inventory.yml** — Minimal inventory with one host (localhost) so you can run without real servers.
- **examples/playbook.yml** — One play: ping and debug message.

Run from this directory:

```bash
ansible-playbook -i examples/inventory.yml examples/playbook.yml
```

## Exercises

1. In **exercises/**, create an inventory with a group `myhosts` containing one host (e.g. `localhost` with `ansible_connection: local`).
2. Create a playbook that targets `myhosts`, runs `ansible.builtin.ping`, then `ansible.builtin.debug` with a message of your choice.
3. Run the playbook: `ansible-playbook -i exercises/inventory.yml exercises/playbook.yml`.

## See Also

- **coding-interview-challenges/ansible_playbook_parser/** — Sample inventory and playbook YAML; Python exercise to load and list plays/tasks/hosts.
