# Ansible Lessons

Beginner-to-advanced Ansible practice: inventory, playbooks, variables, roles, handlers, Vault, and running Ansible from Python.

## Overview

This lesson series is organized into four modules. Each module has a README (objectives and concepts), an `examples/` folder with sample inventory and playbooks, and an `exercises/` folder with tasks or TODOs.

## Prerequisites

- **Ansible** installed (e.g. `pip install ansible-core` or system package). Verify with:
  ```bash
  ansible-playbook --version
  ```
- Basic familiarity with YAML and the command line.

## Learning Path

| Module | Level | Focus |
|--------|--------|--------|
| [01_basics](01_basics/) | Beginner | What Ansible is; inventory (hosts, groups); ad-hoc commands; first playbook; `ansible-playbook` |
| [02_playbooks_variables](02_playbooks_variables/) | Intermediate | Variables, group_vars/host_vars, conditionals, loops, handlers |
| [03_roles_handlers](03_roles_handlers/) | Intermediate | Roles (tasks, handlers, vars, templates), directory layout, using roles in a playbook |
| [04_advanced](04_advanced/) | Advanced | Ansible Vault; running playbooks from Python; parsing play recap |

## Setup

1. Install Ansible (if not already):
   ```bash
   pip install -r requirements.txt
   ```
2. Start with [01_basics](01_basics/): read the README, run the example playbook, then try the exercises.

## Related Projects in This Repo

- **ansible_demo/** — Full Ansible network automation project (Cisco IOS, playbooks, roles, Vault, backups). Use as reference after completing these lessons.
- **coding-interview-challenges/ansible_playbook_parser/** — Python exercise: load playbook and inventory YAML, list plays/tasks/hosts.
- **coding-interview-challenges/ansible_playbook_driver/** — Python exercise: run `ansible-playbook` from Python and parse the play recap.

## License

For educational use. Use responsibly in production.
