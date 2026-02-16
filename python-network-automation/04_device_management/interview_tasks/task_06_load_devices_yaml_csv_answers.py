"""
Task 06: Load devices from YAML or CSV — full solution.
Path to the file is provided (e.g. by interviewer or sys.argv).
"""

import csv
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_devices_from_yaml(path: Path) -> List[Dict[str, Any]]:
    """Load devices from YAML file (expect key 'devices' as list of dicts)."""
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
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


def main() -> None:
    if len(sys.argv) < 2:
        logger.info("Usage: python task_06_...py <path_to_devices.yaml_or_devices.csv>")
        return
    path = Path(sys.argv[1])
    if not path.exists():
        logger.warning("File not found: %s", path)
        return
    if path.suffix.lower() in (".yaml", ".yml"):
        devices = load_devices_from_yaml(path)
    else:
        devices = load_devices_from_csv(path)
    logger.info("Loaded %s devices", len(devices))
    print("Done.")


if __name__ == "__main__":
    main()
