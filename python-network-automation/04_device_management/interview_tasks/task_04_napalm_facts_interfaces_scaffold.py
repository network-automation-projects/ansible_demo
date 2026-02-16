"""
INTERVIEW PROMPT (about 30 min)
-------------------------------
Use NAPALM to connect to a device (vendor-agnostic). Retrieve and return device
facts (hostname, vendor, model, etc.) and interface data. Assume NAPALM is
installed. Device info (hostname, username, password, driver) is provided.
"""

import logging
from typing import Any, Dict

import napalm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to connect with NAPALM. ---
def connect_napalm(device_info: Dict[str, str]) -> Any:
    """Connect via NAPALM; return open connection."""
    # TODO: driver = napalm.get_network_driver(device_info["driver"]); conn = driver(...); conn.open(); return conn
    raise NotImplementedError("Step 1: connect NAPALM")


# --- Step 2: Next I'm going to get device facts from the connection. ---
def get_facts(conn: Any) -> Dict[str, Any]:
    """Return NAPALM get_facts()."""
    # TODO: return conn.get_facts()
    raise NotImplementedError("Step 2: get_facts")


# --- Step 3: Next I'm going to get interface data from the connection. ---
def get_interfaces(conn: Any) -> Dict[str, Dict[str, Any]]:
    """Return NAPALM get_interfaces()."""
    # TODO: return conn.get_interfaces()
    raise NotImplementedError("Step 3: get_interfaces")


# --- Step 4: main() — connect (device_info provided), get facts and interfaces, close. ---
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
