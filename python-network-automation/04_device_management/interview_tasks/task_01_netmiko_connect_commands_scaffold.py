"""
INTERVIEW PROMPT (about 45 min)
-------------------------------
Connect to a network device via SSH using Netmiko. Run a list of show commands
and return a dictionary mapping each command to its output. Assume Netmiko is
installed. Device info (host, username, password, device_type) is provided to
you. Handle connection errors appropriately.
"""

import logging
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

from netmiko import ConnectHandler


# --- Step 1: I'm going to connect to the device with error handling. ---
def connect_to_device(device_info: Dict[str, str]) -> Any:
    """Connect to device via Netmiko. Raise on failure."""
    # TODO: 
    return ConnectHandler(**device_info)
    #raise NotImplementedError("Step 1: connect with ConnectHandler(**device_info)")


# --- Step 2: Next I'm going to get output from the device for each command. ---
def run_commands(connection: Any, commands: List[str]) -> Dict[str, str]:
    """Run show commands and return {command: output}."""
    # TODO: 
    result = {}
    for cmd in commands:
        result = connection.send_command(cmd)
    return result
    # raise NotImplementedError("Step 2: run commands and return dict")


# --- Step 3: main() — use device_info (provided), connect, run commands, disconnect, print. ---
def main() -> None:
    # Device info is provided by the interviewer / test environment.
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }
    ###
    try:
        conn = connect_to_device(device_info=device_info)

        outputs = run_commands(conn, ["show version", "show ip interface brief"])
        for cmd,out in outputs.items():
            logger.info(f"{out}")
            print(f"{out}")

    pass


if __name__ == "__main__":
    main()
