"""
Task 03: Backup running config to file — full solution.
Assume Netmiko is installed; device_info is provided.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from netmiko import ConnectHandler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


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


def main() -> None:
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }
    backup_dir = Path("backups")
    conn = ConnectHandler(**device_info)
    try:
        path = backup_config(conn, backup_dir)
        logger.info("Backup saved: %s", path)
    finally:
        conn.disconnect()
    print("Done.")


if __name__ == "__main__":
    main()
