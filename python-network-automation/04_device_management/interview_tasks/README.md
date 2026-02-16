# Interview Tasks (per-task sets)

Each task is a self-contained interview-style code challenge with a **scaffold** (step-by-step prompts + placeholders) and an **answers** file (full solution).

## Assumptions

- **Netmiko and NAPALM are installed.** No mock or fixture support.
- **No supporting files unless provided.** Device info (host, username, password, device_type/driver), config strings, or file paths are given by the interviewer or test environment. Tasks that need sample data use inline strings in `main()` (e.g. task 02, 09) or accept a path as an argument (task 06).

## Running the tasks

- **Connection tasks (01, 03, 04, 05, 07):** `main()` uses placeholder `device_info`; replace with real credentials or use as-is in a environment where the interviewer provides device access.
- **No-connection tasks (02, 08, 09):** `main()` uses inline sample data; run directly. No files required.
- **Task 06 (load devices):** Pass the path to a YAML or CSV file as the first command-line argument: `python task_06_...py /path/to/devices.yaml`
- Fill in the scaffold (replace `NotImplementedError` / `# TODO` with your code), then compare with the corresponding `*_answers.py` file.

## Task list

| Task | Slug | Description |
|------|------|-------------|
| 01 | `netmiko_connect_commands` | Connect via Netmiko, run show commands, return `{command: output}`; device_info provided. |
| 02 | `parse_report_down_interfaces` | Parse `show ip interface brief` text → list of dicts; filter to down/administratively down. |
| 03 | `backup_config` | From existing connection, get running config, save to `backup_dir/hostname_timestamp.txt`. |
| 04 | `napalm_facts_interfaces` | Connect with NAPALM, return `get_facts()` and `get_interfaces()`. |
| 05 | `napalm_stage_diff` | Stage merge candidate, return diff, discard (no commit). |
| 06 | `load_devices_yaml_csv` | Load device list from YAML (`devices` key) or CSV; path provided. |
| 07 | `retry_backoff` | Connect, run `operation(conn)`, retry on connection/timeout with exponential backoff. |
| 08 | `json_report_jinja2` | Write list of dicts to JSON file; render Jinja2 template with variables. |
| 09 | `compliance_no_description` | Given config text, return interface names with no `description` in their block. |

## File layout

Each set is two files:

- `task_<NN>_<slug>_scaffold.py` — Interview prompt in docstring, step-by-step “I’m going to …” sections, and placeholders to fill in.
- `task_<NN>_<slug>_answers.py` — Full solution for that task only.

## Dependencies

Netmiko, NAPALM, Jinja2, PyYAML. From repo root: `pip install -r requirements.txt`.

## Combined tasks

The single-file versions (full flow in one script) remain in the parent folder: `interview_tasks_practice.py`, `interview_tasks_scaffold.py`, `interview_tasks_answers.py`.
