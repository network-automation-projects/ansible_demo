"""
PRACTICE FROM SCRATCH
=====================

Use this file when you want to implement the full task yourself with only the prompt below.
Copy this file or implement in place. Run with USE_FIXTURES=1 (and empty devices in
fixtures/devices.yaml) to test without real devices. When done, compare with
interview_tasks_answers.py.

How to practice:
  1. Implement the functions listed below (and used in main()) in this file or a copy.
  2. Run with mock/fixtures first: USE_FIXTURES=1 python interview_tasks_practice.py
  3. Compare your solution with interview_tasks_answers.py when finished.

-----------------------------------------------------------------------------
LIKELY TASKS (PROMPT)
-----------------------------------------------------------------------------

  • Use Netmiko (or Paramiko) to SSH into one or more simulated/mock devices,
    run commands (e.g., show interfaces, show version, show bgp neighbors, or
    show access-lists), parse the output (often with TextFSM/ntc-templates or
    regex), and do something useful—like report down interfaces, generate a
    compliance report, or back up configs.

  • Use NAPALM for vendor-agnostic operations: get facts, get interfaces, or
    perform config replace/merge/get_diff.

  • Bonus variations: Loop over devices from a list/CSV/YAML, add error
    handling/retries, output structured data (JSON), or integrate basic
    templating (Jinja2) to generate configs.

-----------------------------------------------------------------------------
REQUIRED FUNCTION SIGNATURES (checklist)
-----------------------------------------------------------------------------

  Netmiko:
    connect_to_device(device_info: dict, connect_func=None) -> connection
    run_commands(connection, commands: list[str]) -> dict[str, str]
    parse_show_ip_int_brief(output: str) -> list[dict]   # interface, ip, status, protocol
    report_down_interfaces(parsed: list[dict]) -> list[dict]
    backup_config(connection, backup_dir: Path) -> Path

  NAPALM:
    connect_napalm(device_info: dict, connect_func=None) -> connection
    get_facts(conn) -> dict
    get_interfaces(conn) -> dict
    stage_and_get_diff(conn, new_config: str) -> str

  Bonus:
    load_devices_from_yaml(path: Path) -> list[dict]
    load_devices_from_csv(path: Path) -> list[dict]
    run_with_retry(device_info, operation, max_attempts=3, base_delay=1.0, connect_func=None) -> any
    output_report_json(results: list[dict], path: Path) -> None
    render_config_jinja2(template_str: str, variables: dict) -> str

  Optional:
    compliance_interfaces_no_description(config_text: str) -> list[str]
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


def connect_to_device(
    device_info: Dict[str, str],
    connect_func: Optional[Callable[..., Any]] = None,
) -> Any:
    """Connect to device via Netmiko; support mock injector."""
    pass


def run_commands(connection: Any, commands: List[str]) -> Dict[str, str]:
    """Run show commands; return {command: output}."""
    pass


def parse_show_ip_int_brief(output: str) -> List[Dict[str, str]]:
    """Parse show ip interface brief into list of dicts (interface, ip, status, protocol)."""
    pass


def report_down_interfaces(parsed: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter to interfaces that are down or administratively down."""
    pass


def backup_config(connection: Any, backup_dir: Path) -> Path:
    """Backup running config to backup_dir/hostname_timestamp.txt."""
    pass


def connect_napalm(
    device_info: Dict[str, str],
    connect_func: Optional[Callable[..., Any]] = None,
) -> Any:
    """Connect via NAPALM; support mock when USE_FIXTURES."""
    pass


def get_facts(conn: Any) -> Dict[str, Any]:
    """Return NAPALM get_facts()."""
    pass


def get_interfaces(conn: Any) -> Dict[str, Dict[str, Any]]:
    """Return NAPALM get_interfaces()."""
    pass


def stage_and_get_diff(conn: Any, new_config: str) -> str:
    """Stage config, return diff, discard (no commit)."""
    pass


def load_devices_from_yaml(path: Path) -> List[Dict[str, Any]]:
    """Load devices from YAML (key 'devices' as list of dicts)."""
    pass


def load_devices_from_csv(path: Path) -> List[Dict[str, Any]]:
    """Load devices from CSV -> netmiko-style dicts."""
    pass


def run_with_retry(
    device_info: Dict[str, str],
    operation: Callable[[Any], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    connect_func: Optional[Callable[..., Any]] = None,
) -> Any:
    """Connect, run operation(conn), retry on ConnectionError/TimeoutError with backoff."""
    pass


def output_report_json(results: List[Dict[str, Any]], path: Path) -> None:
    """Write results to JSON file."""
    pass


def render_config_jinja2(template_str: str, variables: Dict[str, Any]) -> str:
    """Render Jinja2 template with variables."""
    pass


def main() -> None:
    """Orchestrate: load devices, Netmiko flow (connect, run, parse, report, backup), NAPALM flow, JSON report, Jinja2 example."""
    print("Implement the functions above, then call them from main().")
    print("See docstring at top of file for prompt and checklist.")


if __name__ == "__main__":
    main()
