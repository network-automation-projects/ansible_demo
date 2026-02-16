"""
Python Network Automation - Netmiko Decorators Exercise
=================================================
"""

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

def apply_config_netmiko(host, user, pw, config_lines, device_type="cisco_ios"):
    """
    Push configuration lines to a network device using Netmiko.
    config_lines: list of strings, e.g. ["interface GigabitEthernet1", "description Automated"]
    """
    device = {
        "device_type": device_type,
        "host": host,
        "username": user,
        "password": pw,
        # "secret": "enable_pw_if_needed",
    }

    try:
        with ConnectHandler(**device) as conn:
            conn.enable()  # enter enable mode if needed
            output = conn.send_config_set(config_lines)
            conn.save_config()  # write memory
            print(f"Config applied to {host}:\n{output}")
            return True
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Failed to connect to {host}: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Example usage
changes = [
    "interface Loopback100",
    "description Managed by Python automation - Rebecca",
    "ip address 192.168.100.1 255.255.255.255",
    "no shutdown"
]

apply_config_netmiko(
    host="192.168.1.10",          # replace with real device IP
    user="your_username",
    pw="your_password",
    config_lines=changes,
    device_type="cisco_ios"       # or juniper_junos, arista_eos, etc.
)