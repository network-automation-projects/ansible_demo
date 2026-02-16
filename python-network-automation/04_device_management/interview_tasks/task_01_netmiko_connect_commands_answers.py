"""
Task 01: Netmiko connect and run commands — full solution.
Assume Netmiko is installed; device_info is provided.
"""

# INTERVIEW PROMPT (about 45 min)
# -------------------------------
# Connect to a network device via SSH using Netmiko. Run a list of show commands
# and return a dictionary mapping each command to its output. Assume Netmiko is
# installed. Device info (host, username, password, device_type) is provided to
# you. Handle connection errors appropriately.
# """

import logging
from typing import Any, Dict, List

from netmiko import ConnectHandler, ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException


# from netmiko.exceptions import ( ConnectionException, 
# NetmikoAuthenticationException, 
# NetmikoConnectionException
# )

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)



def connect_to_device(device_info: Dict[str, str]) -> Any:
    """Connect to device via Netmiko."""
    return ConnectHandler(**device_info)


def run_commands(connection: Any, commands: List[str]) -> Dict[str, str]:
    """Run show commands and return {command: output}."""
    result: Dict[str, str] = {}
    for cmd in commands:
        result[cmd] = connection.send_command(cmd)
    return result


def main() -> None:
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }
    try:
        conn = connect_to_device(device_info)
    except (ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        logger.error("Conn failed %s", e)
        print ("Conn failed")
        return

    try:
        outputs = run_commands(conn, ["show version", "show ip interface brief"])
        for cmd, out in outputs.items():
            logger.info("%s -> %s chars", cmd, len(out))
            print(out)
            
    except (NetmikoTimeoutException, NetmikoAuthenticationException, ConnectionException) as e:
        logger.error("Error running commands %s", e)
        return
    finally:
        conn.disconnect()
    print("Done.")


if __name__ == "__main__":
    main()
