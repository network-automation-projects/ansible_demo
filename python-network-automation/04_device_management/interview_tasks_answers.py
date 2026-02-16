"""
Interview-style tasks: Netmiko + NAPALM with parsing, backup, compliance, and bonus patterns.
Real connections only (no mock mode). Requires netmiko and napalm; provide device inventory.
"""

import csv
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml
from jinja2 import Template

from netmiko import ConnectHandler
import napalm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Netmiko block
# ---------------------------------------------------------------------------


def connect_to_device(device_info: Dict[str, str]) -> Any:
    """Connect to a device via Netmiko."""
    return ConnectHandler(**device_info)


def run_commands(connection: Any, commands: List[str]) -> Dict[str, str]:
    """Run show commands and return {command: output}."""
    result: Dict[str, str] = {}
    for cmd in commands:
        result[cmd] = connection.send_command(cmd)
    return result


def parse_show_ip_int_brief(output: str) -> List[Dict[str, str]]:
    """Parse 'show ip interface brief' into list of dicts (interface, ip, status, protocol)."""
    interfaces: List[Dict[str, str]] = []
    for line in output.strip().splitlines():
        if line.lower().startswith("interface") or "IP-Address" in line:
            continue
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        interface, ip = parts[0], parts[1]
        protocol = parts[-1]
        if len(parts) >= 6 and parts[-3] == "administratively" and parts[-2] == "down":
            status = "administratively down"
        else:
            status = parts[-2]
        interfaces.append({"interface": interface, "ip": ip, "status": status, "protocol": protocol})
    return interfaces


def report_down_interfaces(parsed: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter to interfaces that are down or administratively down."""
    down = [
        p
        for p in parsed
        if p.get("status") != "up" or p.get("protocol") != "up"
    ]
    for d in down:
        logger.info("Down interface: %s %s %s/%s", d["interface"], d["ip"], d["status"], d["protocol"])
    return down


def backup_config(connection: Any, backup_dir: Path) -> Path:
    """Backup running config to backup_dir/hostname_timestamp.txt."""
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    config = connection.send_command("show running-config")
    hostname = getattr(connection, "find_prompt", lambda: "unknown")() or "unknown"
    hostname = hostname.rstrip("#>").strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = backup_dir / f"{hostname}_{timestamp}.txt"
    path.write_text(config)
    logger.info("Backup saved: %s", path)
    return path


def compliance_interfaces_no_description(config_text: str) -> List[str]:
    """Return interface names that have no 'description' in their block (simple check)."""
    without_desc: List[str] = []
    current = None
    for line in config_text.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("interface "):
            current = line_stripped.split(maxsplit=1)[-1].strip()
        elif current and line_stripped.startswith("description "):
            current = None
        elif current and line_stripped and not line_stripped.startswith("!"):
            if line_stripped.startswith("interface ") or line_stripped == "end":
                if current:
                    without_desc.append(current)
                current = None if line_stripped == "end" else line_stripped.split(maxsplit=1)[-1]
    if current:
        without_desc.append(current)
    return without_desc


# ---------------------------------------------------------------------------
# NAPALM block
# ---------------------------------------------------------------------------


def connect_napalm(device_info: Dict[str, str]) -> Any:
    """Connect via NAPALM."""
    driver = napalm.get_network_driver(device_info.get("driver", "ios"))
    conn = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"],
    )
    conn.open()
    return conn


def get_facts(conn: Any) -> Dict[str, Any]:
    """Return NAPALM get_facts()."""
    return conn.get_facts()


def get_interfaces(conn: Any) -> Dict[str, Dict[str, Any]]:
    """Return NAPALM get_interfaces()."""
    return conn.get_interfaces()


def stage_and_get_diff(conn: Any, new_config: str) -> str:
    """Stage config and return diff; discard so no commit."""
    conn.load_merge_candidate(config=new_config)
    diff = conn.compare_config() or ""
    conn.discard_config()
    return diff


# ---------------------------------------------------------------------------
# Bonus: device list, retry, JSON output, Jinja2
# ---------------------------------------------------------------------------


def load_devices_from_yaml(path: Path) -> List[Dict[str, Any]]:
    """Load devices from YAML file (expect key 'devices' as list of dicts)."""
    path = Path(path)
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    return data.get("devices", [])


def load_devices_from_csv(path: Path) -> List[Dict[str, Any]]:
    """Load devices from CSV: hostname,ip,device_type,username,password -> netmiko-style dicts."""
    path = Path(path)
    devices: List[Dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append({
                "host": row.get("ip", row.get("hostname", "")),
                "hostname": row.get("hostname", row.get("ip", "")),
                "username": row.get("username", ""),
                "password": row.get("password", ""),
                "device_type": row.get("device_type", "cisco_ios"),
            })
    return devices


def run_with_retry(
    device_info: Dict[str, str],
    operation: Callable[[Any], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:
    """Connect with Netmiko, run operation(conn), retry on ConnectionError/TimeoutError with backoff."""
    last_exc: Optional[Exception] = None
    conn = None
    for attempt in range(max_attempts):
        try:
            conn = connect_to_device(device_info)
            return operation(conn)
        except (ConnectionError, TimeoutError, OSError) as e:
            last_exc = e
            if attempt < max_attempts - 1:
                delay = min(base_delay * (2 ** attempt), 30.0)
                time.sleep(delay)
        finally:
            if conn is not None and hasattr(conn, "disconnect"):
                try:
                    conn.disconnect()
                except Exception:
                    pass
            conn = None
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("Max retries exceeded")


def output_report_json(results: List[Dict[str, Any]], path: Path) -> None:
    """Write results to JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    logger.info("Report written: %s", path)


def render_config_jinja2(template_str: str, variables: Dict[str, Any]) -> str:
    """Render Jinja2 template with variables."""
    return Template(template_str).render(**variables)


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main() -> None:
    base = Path(__file__).resolve().parent
    devices_yaml = base / "fixtures" / "devices.yaml"
    devices_csv = base / "fixtures" / "devices.csv"
    backup_dir = base / "backups"
    report_path = base / "report.json"

    devices: List[Dict[str, Any]] = []
    if devices_yaml.exists():
        devices = load_devices_from_yaml(devices_yaml)
    if not devices and devices_csv.exists():
        devices = load_devices_from_csv(devices_csv)
    if not devices:
        logger.warning("No devices in inventory; nothing to do.")
        sys.exit(0)

    netmiko_info = {
        "host": devices[0].get("host", devices[0].get("ip", "")),
        "username": devices[0].get("username", "admin"),
        "password": devices[0].get("password", ""),
        "device_type": devices[0].get("device_type", "cisco_ios"),
    }

    # Netmiko flow
    logger.info("Netmiko: connect, run commands, parse, report down, backup")
    conn = connect_to_device(netmiko_info)
    try:
        outputs = run_commands(conn, ["show version", "show ip interface brief", "show running-config"])
        parsed = parse_show_ip_int_brief(outputs.get("show ip interface brief", ""))
        down = report_down_interfaces(parsed)
        backup_path = backup_config(conn, backup_dir)
        logger.info("Down interfaces count: %s, backup: %s", len(down), backup_path)
    finally:
        conn.disconnect()

    # NAPALM flow
    logger.info("NAPALM: connect, get_facts, get_interfaces, get_diff")
    napalm_info = {
        "hostname": netmiko_info["host"],
        "username": netmiko_info["username"],
        "password": netmiko_info["password"],
        "driver": "ios",
    }
    napalm_conn = connect_napalm(napalm_info)
    try:
        facts = get_facts(napalm_conn)
        interfaces = get_interfaces(napalm_conn)
        new_config = "interface GigabitEthernet0/3\ndescription test\n"
        diff = stage_and_get_diff(napalm_conn, new_config)
        logger.info(
            "NAPALM facts hostname: %s, interfaces: %s, diff length: %s",
            facts.get("hostname"),
            len(interfaces),
            len(diff),
        )
    finally:
        napalm_conn.close()

    # Bonus: JSON report, Jinja2
    report_data = [{"down_interfaces": down, "hostname": netmiko_info["host"]}]
    output_report_json(report_data, report_path)
    template_str = "interface {{ name }}\n description {{ description }}\n"
    rendered = render_config_jinja2(template_str, {"name": "GigabitEthernet0/4", "description": "from-jinja"})
    logger.info("Rendered snippet: %s", rendered.strip())

    print("Done.")


if __name__ == "__main__":
    main()
