# Starters — interview and on-the-job templates

All starter files in one place. Copy or import into your project; each may need its own dependencies (see below).

| File | Description | When to use |
|------|-------------|-------------|
| `netmiko_napalm_starter.py` | Netmiko/NAPALM Protocol types and connect/run helpers | Building Netmiko or NAPALM tools; need IntelliSense and safe connect/disconnect. Deps: `netmiko`, `napalm`. |
| `ansible_module_starter.py` | Minimal Ansible Python module (AnsibleModule, exit_json/fail_json) | Writing a custom Ansible module. Deps: Ansible (e.g. `pip install ansible` or use system). |
| `ansible_playbook_snippet.yml` | Minimal playbook (hosts, vars, tasks, register, when, loop, handler) | Quick playbook structure for interviews or one-off automation. |
| `terraform_starter/` | Minimal Terraform module (main.tf, variables.tf, outputs.tf) | New Terraform module or “paste and fill” layout. |
| `terraform_from_python_starter.py` | Run Terraform from Python (run_terraform, parse_plan_summary) | Automating `terraform init/plan/apply` from Python or CI. |
| `flask_api_starter.py` | Minimal Flask REST API (JSON GET/POST, 404/500 handlers) | New REST API or microservice; interview API task. Deps: `flask`. |
