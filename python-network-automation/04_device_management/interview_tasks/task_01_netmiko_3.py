# INTERVIEW PROMPT (about 45 min)
# -------------------------------
# Connect to a network device via SSH using Netmiko. Run a list of show commands
# and return a dictionary mapping each command to its output. Assume Netmiko is
# installed. Device info (host, username, password, device_type) is provided to
# you. Handle connection errors appropriately.
# """

# Given:
# device_info = {
#         "host": "192.168.1.1",
#         "username": "admin",
#         "password": "secret",
#         "device_type": "cisco_ios",
#     }
# """

from typing import List, Dict, Any, final
from netmiko import ConnectHandler, ConnectionException, NetmikoAuthenticationException, NetmikoTimeoutException

def connect_to_device(device_info: Dict[str,str]) -> Any:
    return ConnectHandler(**device_info)

def run_commands(conn: Any, cmds: List[str]) -> Dict[str, str]:
    result = {}
    for cmd in cmds:
        output = conn.send_command(cmd)
        result[cmd] = output
    return result


def main():
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }


    try:
        #connect
        conn = connect_to_device(device_info=device_info)


        #send command
        outputs = {}
        outputs = run_commands(conn, ["show version", "show ip interface briefly"])

        #print result
        for cmd,output in outputs.items():
            print (f"Command {cmd} produced {len(output)} characters")

    except(NetmikoAuthenticationException,NetmikoTimeoutException,ConnectionException) as e: 
        print(f"Error {e}")

    finally:
        #close
        conn.disconnect()


if __name__ == "__main__":
    main()