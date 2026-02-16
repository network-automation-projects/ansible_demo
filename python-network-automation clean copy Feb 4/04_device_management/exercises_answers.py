"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_device(device_info: Dict[str, str]) -> Any:
    """Connect to a network device using Netmiko."""
    from netmiko import ConnectHandler
    return ConnectHandler(**device_info)


def get_device_version(connection: Any) -> str:
    """Get device version information."""
    return connection.send_command("show version")


def configure_interface(
    connection: Any, interface: str, ip_address: str, subnet_mask: str
) -> str:
    """Configure an interface with IP address."""
    config_commands = [
        f"interface {interface}",
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown",
    ]
    return connection.send_config_set(config_commands)


def save_device_config(connection: Any) -> None:
    """Save running configuration to startup config."""
    connection.save_config()


def connect_with_napalm(device_info: Dict[str, str]) -> Any:
    """Connect to device using NAPALM."""
    import napalm
    driver = napalm.get_network_driver(device_info["driver"])
    conn = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"],
    )
    conn.open()
    return conn


def get_device_facts(connection: Any) -> Dict[str, Any]:
    """Get device facts using NAPALM."""
    return connection.get_facts()


def get_interface_list(connection: Any) -> Dict[str, Dict[str, Any]]:
    """Get interface information."""
    return connection.get_interfaces()


def stage_and_compare_config(connection: Any, new_config: str) -> str:
    """Stage configuration and get diff."""
    connection.load_merge_candidate(config=new_config)
    diff = connection.compare_config()
    return diff or ""


def apply_configuration(connection: Any) -> None:
    """Apply staged configuration."""
    connection.commit_config()


def safe_device_operation(device_info: Dict[str, str], operation: callable) -> Any:
    """Safely connect, perform operation, and disconnect."""
    connection = None
    try:
        from netmiko import ConnectHandler
        connection = ConnectHandler(**device_info)
        result = operation(connection)
        return result
    except Exception as e:
        logger.error(f"Error during device operation: {e}")
        raise
    finally:
        if connection:
            connection.disconnect()


if __name__ == "__main__":
    print("04_device_management – answer key (run exercises.py to practice)")
