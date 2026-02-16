# Exercises (02_playbooks_variables)

1. Create **playbook.yml** that:
   - Defines a variable (e.g. `greeting`) and uses it in a `debug` task.
   - Uses `loop` to print three different values.
   - Has a task with `when: some_var | default(false)` (or similar) so you can run with `-e some_var=true` to see the task run.

2. Optional: Add a **handlers** section with one handler (e.g. a debug message) and **notify** it from a task (e.g. when a dummy condition is true).

3. Run:
   ```bash
   ansible-playbook -i ../01_basics/examples/inventory.yml playbook.yml
   ansible-playbook -i ../01_basics/examples/inventory.yml playbook.yml -e some_var=true
   ```
