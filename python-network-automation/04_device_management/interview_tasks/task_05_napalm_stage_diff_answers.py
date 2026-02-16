"""
Task 05: NAPALM stage config and get diff — full solution.
Assume NAPALM is installed; device_info and candidate config are provided.
"""

import logging
from typing import Any, Dict

import napalm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


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


def stage_and_get_diff(conn: Any, new_config: str) -> str:
    """Stage config and return diff; discard so no commit."""
    conn.load_merge_candidate(config=new_config)
    diff = conn.compare_config() or ""
    conn.discard_config()
    return diff


def main() -> None:
    device_info = {
        "hostname": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "driver": "ios",
    }
    conn = connect_napalm(device_info)
    try:
        new_config = "interface GigabitEthernet0/3\ndescription test\n"
        diff = stage_and_get_diff(conn, new_config)
        logger.info("Diff length: %s", len(diff))
        if diff:
            logger.info("Diff:\n%s", diff)
    finally:
        conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
