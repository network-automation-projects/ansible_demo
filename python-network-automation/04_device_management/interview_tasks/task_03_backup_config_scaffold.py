"""
INTERVIEW PROMPT (about 25 min)
-------------------------------
Using an existing Netmiko connection, retrieve the running config and save it to
a file under a backup directory. Use hostname and timestamp in the filename
(e.g. hostname_YYYYMMDD_HHMMSS.txt). Assume Netmiko is installed; connection and
device info are provided.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

from netmiko import ConnectHandler


# --- Step 1: I'm going to get the running config and hostname from the connection. ---
# --- Step 2: Next I'm going to write the config to a file with hostname and timestamp. ---
def backup_config(connection: Any, backup_dir: Path) -> Path:
    """Backup running config to backup_dir/hostname_timestamp.txt."""
    # TODO: backup_dir.mkdir(parents=True, exist_ok=True)
    # TODO: config = connection.send_command("show running-config")
    # TODO: hostname from connection.find_prompt() or similar (strip #>)
    # TODO: timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # TODO: path = backup_dir / f"{hostname}_{timestamp}.txt"; path.write_text(config); return path
    raise NotImplementedError("Step 1–2: get config and hostname, write to file")


# --- Step 3: main() — connect (device_info provided), backup, disconnect. ---
def main() -> None:
    device_info: Dict[str, str] = {
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
