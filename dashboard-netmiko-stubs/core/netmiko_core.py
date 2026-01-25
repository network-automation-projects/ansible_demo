"""
core/netmiko_core.py

Core module for Netmiko connections with:
- Inventory loading from YAML
- Secure credential handling (env vars + fallback)
- Concurrent execution support
- Comprehensive error handling and logging
- Device facts collection (hostname, model, version, serial)

LEARNING NOTES:
This module handles all network device connections using Netmiko.
Netmiko is a Python library that simplifies SSH connections to network devices.

KEY CONCEPTS:
1. YAML inventory loading - devices are defined in config/devices.yaml
2. Credential handling - secure way to get username/password
3. Concurrent execution - connect to multiple devices in parallel
4. Error handling - network connections can fail in many ways
5. Facts collection - gather device information like hostname, version, etc.

IMPLEMENTATION ORDER:
1. Start with load_inventory() - simplest function
2. Then get_credentials() - credential handling
3. Then gather_device_facts() - single device connection
4. Then backup_config() - configuration backup
5. Finally collect_all_facts() - parallel execution
"""

import os
import logging
# TODO: Uncomment when ready to use
# import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from getpass import getpass
from typing import List, Dict, Optional

# TODO: Uncomment when ready to use Netmiko
# from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/netmiko_core.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_inventory(inventory_file: str = "config/devices.yaml") -> List[Dict]:
    """
    Load device inventory from YAML file.
    
    TODO: Implement this function to:
    1. Open and read the YAML file using yaml.safe_load()
    2. Extract the 'devices' list from the YAML data
    3. Log how many devices were loaded
    4. Handle FileNotFoundError, yaml.YAMLError, and other exceptions
    5. Return the list of device dictionaries
    
    Expected YAML format:
    devices:
      - hostname: r1.example.com
        ip: 192.168.1.1
        device_type: cisco_ios
    
    Returns:
    List[Dict]: List of device dictionaries with keys: hostname, ip, device_type
    
    Example return:
    [
        {'hostname': 'r1.example.com', 'ip': '192.168.1.1', 'device_type': 'cisco_ios'},
        {'hostname': 'r2.example.com', 'ip': '192.168.1.2', 'device_type': 'cisco_ios'}
    ]
    """
    try:
        # TODO: Implement YAML loading
        # with open(inventory_file, 'r') as f:
        #     data = yaml.safe_load(f)
        # devices = data.get('devices', [])
        # logger.info(f"Loaded {len(devices)} devices from inventory.")
        # return devices
        
        logger.warning("load_inventory() not yet implemented - returning empty list")
        return []
    except FileNotFoundError:
        logger.error(f"Inventory file {inventory_file} not found.")
        raise
    except Exception as e:
        logger.error(f"Failed to load inventory file {inventory_file}: {e}")
        raise


def get_credentials(username: Optional[str] = None, password: Optional[str] = None) -> tuple:
    """
    Get username/password securely.
    Priority: passed args > env vars > prompt
    
    TODO: Implement this function to:
    1. If username not provided, check NET_USER environment variable, then prompt with input()
    2. If password not provided, check NET_PASS environment variable, then prompt with getpass()
    3. Return tuple (username, password)
    
    Security best practice: Use environment variables in production, never hardcode credentials!
    
    Returns:
    tuple: (username, password)
    """
    # TODO: Implement credential handling
    # if not username:
    #     username = os.getenv("NET_USER") or input("Username: ")
    # if not password:
    #     password = os.getenv("NET_PASS") or getpass("Password: ")
    # return username, password
    
    logger.warning("get_credentials() not yet implemented - returning placeholder")
    return ("admin", "password")  # Placeholder - replace with actual implementation


def gather_device_facts(device: Dict) -> Dict:
    """
    Connect to a single device and collect basic facts using 'show version'.
    Returns enriched device dict with facts or error info.
    
    TODO: Implement this function to:
    1. Make a copy of the device dict (to avoid mutating original)
    2. Get credentials using get_credentials()
    3. Build Netmiko connection parameters:
       - device_type, host, username, password, secret, timeout
    4. Optionally add session_log if NETMIKO_DEBUG env var is set
    5. Use ConnectHandler as context manager (with statement)
    6. Try to enter enable mode (conn.enable())
    7. Send 'show version' command (vendor-specific)
    8. Get hostname from prompt (conn.find_prompt())
    9. Parse output to extract: model, serial, version, uptime
    10. Return device dict with added keys: facts, status='reachable', error=None
    11. Handle NetmikoTimeoutException -> status='unreachable'
    12. Handle NetmikoAuthenticationException -> status='auth_failed'
    13. Handle other exceptions -> status='error'
    
    Expected return format:
    {
        'ip': '192.168.1.1',
        'hostname': 'r1.example.com',
        'device_type': 'cisco_ios',
        'status': 'reachable',  # or 'unreachable', 'auth_failed', 'error'
        'facts': {
            'hostname_from_device': 'router1',
            'model': 'Cisco 2911',
            'serial': 'FTX12345678',
            'version': 'Cisco IOS Software, Version 15.1(4)M4',
            'uptime': '5 days, 2 hours, 30 minutes',
            'raw_version': '...full output...'
        },
        'error': None  # or error message string
    }
    
    Vendor-specific commands:
    - cisco_ios: 'show version'
    - cisco_nxos: 'show version'
    - cisco_xr: 'show version'
    - juniper_junos: 'show version'
    - arista_eos: 'show version'
    """
    device = device.copy()  # Avoid mutating original
    
    # TODO: Get credentials
    # username, password = get_credentials(device.get('username'), device.get('password'))
    
    # TODO: Build Netmiko connection parameters
    # netmiko_params = {
    #     'device_type': device['device_type'],
    #     'host': device['ip'],
    #     'username': username,
    #     'password': password,
    #     'secret': device.get('secret', password),
    #     'timeout': 30,
    # }
    
    # TODO: Optional session logging for debugging
    # if os.getenv('NETMIKO_DEBUG', '').lower() == 'true':
    #     os.makedirs('logs', exist_ok=True)
    #     netmiko_params['session_log'] = f"logs/{device['ip']}_session.log"
    
    try:
        logger.info(f"Connecting to {device['ip']} ({device.get('hostname', 'N/A')})")
        
        # TODO: Connect using Netmiko
        # with ConnectHandler(**netmiko_params) as conn:
        #     try:
        #         conn.enable()
        #     except Exception:
        #         pass  # Some devices don't need enable
        
        # TODO: Send version command
        # version_cmd = {
        #     'cisco_ios': 'show version',
        #     'cisco_nxos': 'show version',
        #     'cisco_xr': 'show version',
        #     'juniper_junos': 'show version',
        #     'arista_eos': 'show version',
        # }.get(device['device_type'], 'show version')
        # output = conn.send_command(version_cmd)
        
        # TODO: Get hostname from prompt
        # prompt = conn.find_prompt()
        # hostname_from_device = prompt.rstrip('>#').strip()
        
        # TODO: Parse output to extract facts
        # facts = {
        #     'raw_version': output,
        #     'uptime': 'Unknown',
        #     'model': 'Unknown',
        #     'serial': 'Unknown',
        #     'version': 'Unknown',
        #     'hostname_from_device': hostname_from_device,
        # }
        # # Parse output to extract model, serial, version, uptime
        
        # device.update({
        #     'facts': facts,
        #     'status': 'reachable',
        #     'error': None
        # })
        # logger.info(f"Successfully gathered facts from {device['ip']}")
        
        logger.warning(f"gather_device_facts() not yet implemented for {device['ip']}")
        device.update({
            'status': 'error',
            'error': 'Not yet implemented',
            'facts': None
        })
        
    except Exception as e:
        # TODO: Handle specific Netmiko exceptions
        # except NetmikoTimeoutException:
        #     error = "Timeout - device unreachable"
        #     device.update({
        #         'status': 'unreachable',
        #         'error': error,
        #         'facts': None
        #     })
        # except NetmikoAuthenticationException:
        #     error = "Authentication failed"
        #     device.update({
        #         'status': 'auth_failed',
        #         'error': error,
        #         'facts': None
        #     })
        
        error = str(e)
        device.update({
            'status': 'error',
            'error': error,
            'facts': None
        })
        logger.error(f"Unexpected error on {device['ip']}: {e}")
    
    return device


def backup_config(device: Dict, backup_dir: str = "backups") -> Optional[str]:
    """
    Backup running configuration from a device.
    Returns path to backup file or None on failure.
    
    TODO: Implement this function to:
    1. Make a copy of the device dict
    2. Get credentials using get_credentials()
    3. Build Netmiko connection parameters
    4. Create backup directory if it doesn't exist
    5. Connect to device using ConnectHandler
    6. Enter enable mode if needed
    7. Send vendor-specific config command:
       - cisco_ios/nxos/xr/eos: 'show running-config'
       - juniper_junos: 'show configuration'
    8. Generate backup filename with timestamp: {hostname}_{ip}_{timestamp}.cfg
    9. Write config output to file
    10. Return backup file path
    11. Handle exceptions and return None on failure
    
    Returns:
    Optional[str]: Path to backup file, or None if backup failed
    
    Example backup filename: r1.example.com_192.168.1.1_20250120_143022.cfg
    """
    device = device.copy()
    
    # TODO: Get credentials
    # username, password = get_credentials(device.get('username'), device.get('password'))
    
    # TODO: Build connection parameters
    # netmiko_params = {...}
    
    # TODO: Vendor-specific config commands
    # config_cmd = {
    #     'cisco_ios': 'show running-config',
    #     'cisco_nxos': 'show running-config',
    #     'cisco_xr': 'show running-config',
    #     'juniper_junos': 'show configuration',
    #     'arista_eos': 'show running-config',
    # }.get(device['device_type'], 'show running-config')
    
    try:
        # TODO: Create backup directory
        # os.makedirs(backup_dir, exist_ok=True)
        # logger.info(f"Backing up config from {device['ip']}")
        
        # TODO: Connect and get config
        # with ConnectHandler(**netmiko_params) as conn:
        #     try:
        #         conn.enable()
        #     except Exception:
        #         pass
        #     config_output = conn.send_command(config_cmd)
        
        # TODO: Generate filename and write file
        # from datetime import datetime
        # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # hostname = device.get('hostname', device['ip'])
        # backup_filename = f"{hostname}_{device['ip']}_{timestamp}.cfg"
        # backup_path = os.path.join(backup_dir, backup_filename)
        # with open(backup_path, 'w') as f:
        #     f.write(config_output)
        # logger.info(f"Backup saved to {backup_path}")
        # return backup_path
        
        logger.warning(f"backup_config() not yet implemented for {device['ip']}")
        return None
        
    except Exception as e:
        logger.error(f"Failed to backup {device['ip']}: {e}")
        return None


def collect_all_facts(
    max_workers: int = 10,
    inventory_file: str = "config/devices.yaml"
) -> List[Dict]:
    """
    Collect facts from all devices concurrently.
    Returns list of enriched device dictionaries.
    
    TODO: Implement this function to:
    1. Load inventory using load_inventory(inventory_file)
    2. Use ThreadPoolExecutor to run gather_device_facts() in parallel
    3. Submit tasks for each device: executor.submit(gather_device_facts, dev)
    4. Collect results as they complete using as_completed()
    5. Log summary: how many devices were reachable
    6. Return list of enriched device dictionaries
    
    This function demonstrates concurrent programming in Python.
    ThreadPoolExecutor allows multiple devices to be queried simultaneously,
    which is much faster than querying them one at a time.
    
    Parameters:
    - max_workers: Maximum number of concurrent connections (default: 10)
    - inventory_file: Path to YAML inventory file
    
    Returns:
    List[Dict]: List of device dictionaries with facts added
    
    Example:
    results = collect_all_facts(max_workers=5)
    # Returns list of devices, each with 'facts', 'status', 'error' keys
    """
    # TODO: Load inventory
    # devices = load_inventory(inventory_file)
    
    # TODO: Use ThreadPoolExecutor for concurrent execution
    # enriched_devices = []
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     future_to_device = {
    #         executor.submit(gather_device_facts, dev): dev for dev in devices
    #     }
    #     for future in as_completed(future_to_device):
    #         result = future.result()
    #         enriched_devices.append(result)
    
    # TODO: Log summary
    # reachable = [d for d in enriched_devices if d['status'] == 'reachable']
    # logger.info(f"Collection complete: {len(reachable)}/{len(devices)} devices reachable")
    
    logger.warning("collect_all_facts() not yet implemented - returning empty list")
    return []


# For quick testing from CLI
if __name__ == "__main__":
    # TODO: Uncomment when ready to test
    # results = collect_all_facts(max_workers=5)
    # for dev in results:
    #     print(f"{dev['ip']}: {dev['status']}")
    #     if dev['status'] == 'reachable':
    #         print(f"   Hostname: {dev['facts']['hostname_from_device']}")
    #         print(f"   Version: {dev['facts']['version'][:60]}...")
    print("Run this module after implementing the functions above")



