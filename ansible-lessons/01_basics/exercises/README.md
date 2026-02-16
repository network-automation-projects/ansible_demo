# Exercises (01_basics)

1. Create **inventory.yml** in this folder with:
   - A group (e.g. `myhosts`) containing one host: `localhost` with `ansible_connection: local`.

2. Create **playbook.yml** in this folder with:
   - One play targeting that group.
   - `gather_facts: false`.
   - Two tasks: `ansible.builtin.ping` and `ansible.builtin.debug` with any message.

3. Run from the **01_basics** directory:
   ```bash
   ansible-playbook -i exercises/inventory.yml exercises/playbook.yml
   ```
