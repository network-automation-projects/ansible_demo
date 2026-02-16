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

from typing import Dict, List, Any
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetmikoTimeoutException, ConnectionException

def connect_to_device(device_info: Any) -> Any:
    return ConnectHandler(**device_info)

def run_commands(conn: Any, cmds: List[str]) -> Dict[str,str]:
    result = {}
    for cmd in cmds:
        result[cmd] = conn.send_command(cmd)

    return result

def main() -> None:
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }

    
    # connect
    conn = connect_to_device(device_info=device_info)

    try:
        # run command
        output = run_commands(conn, ["show version", "show ip interface brief"])

        # print out puts
        if output:
            print(output)
    
    finally:
        conn.disconnect()


if __name__ == "__main__":
    main()