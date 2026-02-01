"""
Python Network Automation - Device Management Exercises
======================================================

Fill-in-the-blank exercises for learning Netmiko, NAPALM, and Paramiko
in the context of network automation.

Note: These exercises use mock/example code. In production, ensure proper
credentials management and network connectivity.
"""

from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Note: In real usage, you would import:
# from netmiko import ConnectHandler
# import napalm
# import paramiko


# ============================================================================
# EXERCISE 1: Netmiko Connection
# ============================================================================

"""
Tutorial: Netmiko ConnectHandler
---------------------------------

ConnectHandler(**kwargs) establishes SSH connection to network device.

Required parameters:
- device_type: 'cisco_ios', 'juniper_junos', 'arista_eos', etc.
- host: Device IP or hostname
- username: SSH username
- password: SSH password
- secret: Enable password (optional)

Always use try/except and disconnect() in finally block!
"""


def connect_to_device(device_info: Dict[str, str]) -> Any:
    """
    Connect to a network device using Netmiko.
    
    Args:
        device_info: Dictionary with 'host', 'username', 'password', 'device_type'
        
    Returns:
        Netmiko connection object
        
    Example:
        >>> device = {
        ...     'host': '10.0.0.1',
        ...     'username': 'admin',
        ...     'password': 'secret',
        ...     'device_type': 'cisco_ios'
        ... }
        >>> conn = connect_to_device(device)
    """
    # TODO: Fill in the blank - use ConnectHandler to create connection
    # from netmiko import ConnectHandler
    # conn = ConnectHandler(**device_info)
    # return conn
    pass  # Replace with actual implementation


# ============================================================================
# EXERCISE 2: Execute Show Command
# ============================================================================

"""
Tutorial: send_command()
-------------------------

connection.send_command(command_string) executes a command and returns output.

Common commands:
- 'show version' - Device version info
- 'show ip interface brief' - Interface status
- 'show running-config' - Current configuration
"""


def get_device_version(connection: Any) -> str:
    """
    Get device version information.
    
    Args:
        connection: Netmiko connection object
        
    Returns:
        Command output as string
    """
    # TODO: Fill in the blank - use send_command() to execute 'show version'
    return None  # Execute 'show version' command


# ============================================================================
# EXERCISE 3: Send Configuration
# ============================================================================

"""
Tutorial: send_config_set()
----------------------------

connection.send_config_set(config_commands) sends configuration commands.

config_commands can be:
- List of strings: ['interface Eth0', 'ip address 10.0.0.1 255.255.255.0']
- String with newlines: 'interface Eth0\nip address 10.0.0.1 255.255.255.0'
"""


def configure_interface(connection: Any, interface: str, ip_address: str, 
                        subnet_mask: str) -> str:
    """
    Configure an interface with IP address.
    
    Args:
        connection: Netmiko connection object
        interface: Interface name (e.g., 'GigabitEthernet0/0')
        ip_address: IP address
        subnet_mask: Subnet mask
        
    Returns:
        Command output
    """
    # TODO: Fill in the blank - use send_config_set() with config commands
    config_commands = [
        f"interface {interface}",
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown"
    ]
    return None  # Send configuration commands


# ============================================================================
# EXERCISE 4: Save Configuration
# ============================================================================

"""
Tutorial: save_config()
-----------------------

connection.save_config() saves running configuration to startup config.

Equivalent to 'write memory' or 'copy running-config startup-config'.
"""


def save_device_config(connection: Any) -> None:
    """
    Save running configuration to startup config.
    
    Args:
        connection: Netmiko connection object
    """
    # TODO: Fill in the blank - use save_config() method
    None  # Save configuration


# ============================================================================
# EXERCISE 5: NAPALM Connection
# ============================================================================

"""
Tutorial: NAPALM get_network_driver
------------------------------------

napalm.get_network_driver('ios') returns a driver class.
driver(hostname=..., username=..., password=...) creates connection.
connection.open() establishes connection.

NAPALM provides vendor-agnostic interface.
"""


def connect_with_napalm(device_info: Dict[str, str]) -> Any:
    """
    Connect to device using NAPALM.
    
    Args:
        device_info: Dictionary with 'hostname', 'username', 'password', 'driver'
        
    Returns:
        NAPALM connection object
        
    Example:
        >>> device = {
        ...     'hostname': '10.0.0.1',
        ...     'username': 'admin',
        ...     'password': 'secret',
        ...     'driver': 'ios'
        ... }
        >>> conn = connect_with_napalm(device)
    """
    # TODO: Fill in the blank - use napalm.get_network_driver()
    # import napalm
    # driver = napalm.get_network_driver(device_info['driver'])
    # conn = driver(
    #     hostname=device_info['hostname'],
    #     username=device_info['username'],
    #     password=device_info['password']
    # )
    # conn.open()
    # return conn
    pass  # Replace with actual implementation


# ============================================================================
# EXERCISE 6: Get Device Facts
# ============================================================================

"""
Tutorial: get_facts()
----------------------

connection.get_facts() returns structured dictionary with:
- hostname, vendor, model, os_version, serial_number, uptime, etc.
"""


def get_device_facts(connection: Any) -> Dict[str, Any]:
    """
    Get device facts using NAPALM.
    
    Args:
        connection: NAPALM connection object
        
    Returns:
        Dictionary with device facts
    """
    # TODO: Fill in the blank - use get_facts() method
    return None  # Get device facts


# ============================================================================
# EXERCISE 7: Get Interfaces
# ============================================================================

"""
Tutorial: get_interfaces()
---------------------------

connection.get_interfaces() returns dictionary of interfaces with:
- status, speed, description, mac_address, etc.
"""


def get_interface_list(connection: Any) -> Dict[str, Dict[str, Any]]:
    """
    Get interface information.
    
    Args:
        connection: NAPALM connection object
        
    Returns:
        Dictionary mapping interface names to interface data
    """
    # TODO: Fill in the blank - use get_interfaces() method
    return None  # Get interfaces


# ============================================================================
# EXERCISE 8: Load and Compare Config
# ============================================================================

"""
Tutorial: load_merge_candidate() and compare_config()
------------------------------------------------------

connection.load_merge_candidate(config=config_string) stages configuration.
connection.compare_config() shows diff between candidate and running.
connection.commit_config() applies changes.
connection.discard_config() discards staged changes.
"""


def stage_and_compare_config(connection: Any, new_config: str) -> str:
    """
    Stage configuration and get diff.
    
    Args:
        connection: NAPALM connection object
        new_config: Configuration string to stage
        
    Returns:
        Diff string showing changes
    """
    # TODO: Fill in the blank - use load_merge_candidate() and compare_config()
    # Load candidate config
    None  # Use load_merge_candidate(config=new_config)
    # Get diff
    diff = None  # Use compare_config()
    return diff


# ============================================================================
# EXERCISE 9: Commit Configuration
# ============================================================================

"""
Tutorial: commit_config()
--------------------------

connection.commit_config() applies staged configuration.
Always compare first to review changes!
"""


def apply_configuration(connection: Any) -> None:
    """
    Apply staged configuration.
    
    Args:
        connection: NAPALM connection object
    """
    # TODO: Fill in the blank - use commit_config()
    None  # Commit configuration


# ============================================================================
# EXERCISE 10: Proper Connection Cleanup
# ============================================================================

"""
Tutorial: Connection Cleanup
----------------------------

Always close connections properly:
- Use try/except/finally blocks
- Call disconnect() or close() in finally
- Handle exceptions gracefully
"""


def safe_device_operation(device_info: Dict[str, str], operation: callable) -> Any:
    """
    Safely connect, perform operation, and disconnect.
    
    Args:
        device_info: Device connection parameters
        operation: Function to execute with connection
        
    Returns:
        Operation result
    """
    connection = None
    try:
        # TODO: Fill in the blank - connect to device
        connection = None  # Connect using ConnectHandler or NAPALM
        
        # Execute operation
        result = operation(connection)
        return result
    
    except Exception as e:
        logger.error(f"Error during device operation: {e}")
        raise
    
    finally:
        # TODO: Fill in the blank - always disconnect
        if connection:
            None  # Disconnect/close connection


# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEVICE MANAGEMENT EXERCISES")
    print("=" * 70)
    print("\nNote: These exercises require actual device connections.")
    print("Uncomment and modify device_info with your device credentials.")
    
    # Example device info (DO NOT commit real credentials!)
    # device_info = {
    #     'host': '10.0.0.1',
    #     'username': 'admin',
    #     'password': 'secret',
    #     'device_type': 'cisco_ios'
    # }
    
    # Test Exercise 1
    # print("\nExercise 1: Connect to Device")
    # conn = connect_to_device(device_info)
    # print("Connected successfully")
    
    # Test Exercise 2
    # print("\nExercise 2: Get Version")
    # version = get_device_version(conn)
    # print(version[:100])  # Print first 100 chars
    
    # Test Exercise 3
    # print("\nExercise 3: Configure Interface")
    # output = configure_interface(conn, 'GigabitEthernet0/0', '10.0.0.1', '255.255.255.0')
    # print(output)
    
    # Test Exercise 4
    # print("\nExercise 4: Save Config")
    # save_device_config(conn)
    # print("Config saved")
    
    # Test Exercise 5
    # print("\nExercise 5: NAPALM Connection")
    # napalm_info = {
    #     'hostname': '10.0.0.1',
    #     'username': 'admin',
    #     'password': 'secret',
    #     'driver': 'ios'
    # }
    # napalm_conn = connect_with_napalm(napalm_info)
    # print("NAPALM connected")
    
    # Test Exercise 6
    # print("\nExercise 6: Get Facts")
    # facts = get_device_facts(napalm_conn)
    # print(f"Hostname: {facts.get('hostname')}")
    
    # Test Exercise 7
    # print("\nExercise 7: Get Interfaces")
    # interfaces = get_interface_list(napalm_conn)
    # print(f"Found {len(interfaces)} interfaces")
    
    # Test Exercise 8
    # print("\nExercise 8: Compare Config")
    # new_config = "interface GigabitEthernet0/1\nip address 10.0.0.2 255.255.255.0"
    # diff = stage_and_compare_config(napalm_conn, new_config)
    # print(diff)
    
    # Test Exercise 9
    # print("\nExercise 9: Commit Config")
    # # Only uncomment if you want to actually apply changes!
    # # apply_configuration(napalm_conn)
    # print("Config would be applied (commented out for safety)")
    
    # Test Exercise 10
    # print("\nExercise 10: Safe Operation")
    # def get_version(conn):
    #     return conn.send_command('show version')
    # result = safe_device_operation(device_info, get_version)
    # print("Operation completed safely")
    
    print("\nUncomment test cases above to verify your solutions!")
    print("Remember: Never commit real credentials to version control!")
