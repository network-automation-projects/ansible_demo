"""
Task 04: NAPALM connect, get_facts, get_interfaces — full solution.
Assume NAPALM is installed; device_info is provided.
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


def get_facts(conn: Any) -> Dict[str, Any]:
    """Return NAPALM get_facts()."""
    return conn.get_facts()


def get_interfaces(conn: Any) -> Dict[str, Dict[str, Any]]:
    """Return NAPALM get_interfaces()."""
    return conn.get_interfaces()


def main() -> None:
    device_info = {
        "hostname": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "driver": "ios",
    }
    conn = connect_napalm(device_info)
    try:
        facts = get_facts(conn)
        interfaces = get_interfaces(conn)
        logger.info("Facts: %s", facts.get("hostname"))
        logger.info("Interfaces count: %s", len(interfaces))
    finally:
        conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
