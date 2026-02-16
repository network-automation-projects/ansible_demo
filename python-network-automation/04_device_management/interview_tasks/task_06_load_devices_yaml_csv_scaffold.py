"""
INTERVIEW PROMPT (about 25 min)
-------------------------------
Load a device inventory from a YAML file (expect key 'devices' as a list of
dicts) or from a CSV with columns such as hostname, ip, device_type, username,
password. Return a list of device dicts suitable for Netmiko/NAPALM. Assume you
are given a path to the file (no supporting files unless provided by the
interviewer).
"""

import csv
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to load devices from a YAML file (key 'devices'). ---
def load_devices_from_yaml(path: Path) -> List[Dict[str, Any]]:
    """Load devices from YAML file (expect key 'devices' as list of dicts)."""
    # TODO: with open(path) as f: data = yaml.safe_load(f) or {}
    # TODO: return data.get("devices", [])
    raise NotImplementedError("Step 1: load YAML, return devices list")


# --- Step 2: Next I'm going to load devices from a CSV into Netmiko-style dicts. ---
def load_devices_from_csv(path: Path) -> List[Dict[str, Any]]:
    """Load devices from CSV: hostname,ip,device_type,username,password -> netmiko-style dicts."""
    # TODO: csv.DictReader; for each row build dict with host/hostname, username, password, device_type
    raise NotImplementedError("Step 2: csv.DictReader, build list of device dicts")


# --- Step 3: main() — use path provided (e.g. command-line arg or given by interviewer). ---
def main() -> None:
    # Path is provided by the interviewer or as first command-line argument.
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
