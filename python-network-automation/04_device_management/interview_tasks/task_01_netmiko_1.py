# INTERVIEW PROMPT (about 45 min)
# -------------------------------
# Connect to a network device via SSH using Netmiko. Run a list of show commands
# and return a dictionary mapping each command to its output. Assume Netmiko is
# installed. Device info (host, username, password, device_type) is provided to
# you. Handle connection errors appropriately.

# Given:
# device_info = {
#         "host": "192.168.1.1",
#         "username": "admin",
#         "password": "secret",
#         "device_type": "cisco_ios",
#     }
# """

import logging
from typing import Any,Dict,List

from netmiko import ConnectHandler, ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException

def connect_to_device(device_info: Dict[str, str]) -> Any:
    return ConnectHandler(**device_info)


def run_commands(connection: Any, commands: List[str]) -> Dict[str, str]:
    result: Dict[str,str] = {}
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

    # connect
    try:
        conn = connect_to_device(device_info=device_info)
    except (ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        logging.error("Conn failed %s", e)
        return

    #use connection to run commands
    try:
        output = run_commands(connection=conn, commands=["show version", "show ip interface brief"])
        for cmd, out in output.items():
            logging.info("Command successful: %s Output len %s", cmd, len(out))

    #log/print output from commands
    except (ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        logging.error("Run commands failed %s", e)
        return
    finally: 
        conn.disconnect()

if __name__ == "__main__":
    main()
