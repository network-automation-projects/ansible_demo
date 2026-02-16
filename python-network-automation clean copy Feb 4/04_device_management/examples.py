"""
Python Network Automation - Device Management Examples
=====================================================

Complete working examples demonstrating Netmiko, NAPALM, and Paramiko
in real-world network automation scenarios.

Note: These examples use mock implementations for safety.
In production, ensure proper credentials management and network connectivity.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock implementations for demonstration
# In production, use:
# from netmiko import ConnectHandler
# import napalm


# ============================================================================
# Example 1: Netmiko Device Manager
# ============================================================================

class NetmikoDeviceManager:
    """Manages device connections using Netmiko."""
    
    def __init__(self, device_info: Dict[str, str]):
        """
        Initialize device manager.
        
        Args:
            device_info: Device connection parameters
        """
        self.device_info = device_info
        self.connection = None
    
    def connect(self) -> None:
        """Establish connection to device."""
        try:
            # In production: from netmiko import ConnectHandler
            # self.connection = ConnectHandler(**self.device_info)
            logger.info(f"Connecting to {self.device_info.get('host')}")
            # Mock connection
            self.connection = {'connected': True, 'host': self.device_info.get('host')}
            logger.info("Connected successfully")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close connection."""
        if self.connection:
            # In production: self.connection.disconnect()
            logger.info("Disconnected")
            self.connection = None
    
    def send_command(self, command: str) -> str:
        """
        Execute show command.
        
        Args:
            command: Command to execute
            
        Returns:
            Command output
        """
        if not self.connection:
            raise RuntimeError("Not connected")
        
        # In production: return self.connection.send_command(command)
        logger.info(f"Executing: {command}")
        return f"Mock output for: {command}"
    
    def send_config(self, config_commands: List[str]) -> str:
        """
        Send configuration commands.
        
        Args:
            config_commands: List of configuration commands
            
        Returns:
            Command output
        """
        if not self.connection:
            raise RuntimeError("Not connected")
        
        # In production: return self.connection.send_config_set(config_commands)
        logger.info(f"Sending config: {len(config_commands)} commands")
        return "Configuration applied"
    
    def save_config(self) -> None:
        """Save running configuration."""
        if not self.connection:
            raise RuntimeError("Not connected")
        
        # In production: self.connection.save_config()
        logger.info("Configuration saved")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# ============================================================================
# Example 2: NAPALM Facts Gatherer
# ============================================================================

class NAPALMFactsGatherer:
    """Gathers device facts using NAPALM."""
    
    def __init__(self, device_info: Dict[str, str]):
        """
        Initialize facts gatherer.
        
        Args:
            device_info: Device connection parameters
        """
        self.device_info = device_info
        self.connection = None
    
    def connect(self) -> None:
        """Establish NAPALM connection."""
        try:
            # In production:
            # import napalm
            # driver = napalm.get_network_driver(self.device_info['driver'])
            # self.connection = driver(
            #     hostname=self.device_info['hostname'],
            #     username=self.device_info['username'],
            #     password=self.device_info['password']
            # )
            # self.connection.open()
            logger.info(f"Connecting to {self.device_info.get('hostname')}")
            self.connection = {'connected': True}
            logger.info("NAPALM connected")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def get_facts(self) -> Dict[str, Any]:
        """
        Get device facts.
        
        Returns:
            Dictionary with device facts
        """
        if not self.connection:
            raise RuntimeError("Not connected")
        
        # In production: return self.connection.get_facts()
        return {
            'hostname': 'router1',
            'vendor': 'cisco',
            'model': 'ASR1000',
            'os_version': '15.1',
            'serial_number': 'ABC123',
            'uptime': 86400
        }
    
    def get_interfaces(self) -> Dict[str, Dict[str, Any]]:
        """
        Get interface information.
        
        Returns:
            Dictionary mapping interface names to interface data
        """
        if not self.connection:
            raise RuntimeError("Not connected")
        
        # In production: return self.connection.get_interfaces()
        return {
            'GigabitEthernet0/0': {
                'is_up': True,
                'is_enabled': True,
                'speed': 1000,
                'description': 'Uplink'
            },
            'GigabitEthernet0/1': {
                'is_up': False,
                'is_enabled': True,
                'speed': 1000,
                'description': ''
            }
        }
    
    def close(self) -> None:
        """Close connection."""
        if self.connection:
            # In production: self.connection.close()
            logger.info("NAPALM connection closed")
            self.connection = None


# ============================================================================
# Example 3: Safe Configuration Deployment
# ============================================================================

class SafeConfigDeployer:
    """Safely deploys configuration using NAPALM."""
    
    def __init__(self, connection: Any):
        """
        Initialize config deployer.
        
        Args:
            connection: NAPALM connection object
        """
        self.connection = connection
    
    def deploy_config(self, new_config: str, dry_run: bool = True) -> Dict[str, Any]:
        """
        Deploy configuration with safety checks.
        
        Args:
            new_config: Configuration to deploy
            dry_run: If True, only show diff without applying
            
        Returns:
            Dictionary with deployment results
        """
        try:
            # Load candidate configuration
            # In production: self.connection.load_merge_candidate(config=new_config)
            logger.info("Loaded candidate configuration")
            
            # Compare with running config
            # In production: diff = self.connection.compare_config()
            diff = "Mock diff output"
            
            logger.info(f"Configuration diff:\n{diff}")
            
            if dry_run:
                # Discard changes in dry-run mode
                # In production: self.connection.discard_config()
                logger.info("Dry-run mode: Changes discarded")
                return {
                    'success': True,
                    'dry_run': True,
                    'diff': diff,
                    'applied': False
                }
            else:
                # Commit changes
                # In production: self.connection.commit_config()
                logger.info("Configuration committed")
                return {
                    'success': True,
                    'dry_run': False,
                    'diff': diff,
                    'applied': True
                }
        
        except Exception as e:
            logger.error(f"Configuration deployment failed: {e}")
            # Discard on error
            # In production: self.connection.discard_config()
            return {
                'success': False,
                'error': str(e),
                'applied': False
            }


# ============================================================================
# Example 4: Device Backup Manager
# ============================================================================

class DeviceBackupManager:
    """Manages device configuration backups."""
    
    def __init__(self, device_manager: NetmikoDeviceManager, backup_dir: str = "backups"):
        """
        Initialize backup manager.
        
        Args:
            device_manager: Netmiko device manager
            backup_dir: Directory for backups
        """
        self.device_manager = device_manager
        self.backup_dir = backup_dir
    
    def backup_running_config(self) -> str:
        """
        Backup running configuration.
        
        Returns:
            Path to backup file
        """
        import os
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Get running config
        config = self.device_manager.send_command('show running-config')
        
        # Generate backup filename
        hostname = self.device_manager.device_info.get('host', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f"{hostname}_{timestamp}.txt")
        
        # Save to file
        with open(backup_file, 'w') as f:
            f.write(config)
        
        logger.info(f"Backup saved to {backup_file}")
        return backup_file


# ============================================================================
# Example 5: Multi-Device Operations
# ============================================================================

def gather_facts_from_devices(devices: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Gather facts from multiple devices.
    
    Args:
        devices: List of device connection dictionaries
        
    Returns:
        List of device facts dictionaries
    """
    facts_list = []
    
    for device_info in devices:
        try:
            gatherer = NAPALMFactsGatherer(device_info)
            gatherer.connect()
            
            facts = gatherer.get_facts()
            facts['connection_info'] = device_info.get('hostname')
            facts_list.append(facts)
            
            gatherer.close()
        
        except Exception as e:
            logger.error(f"Failed to gather facts from {device_info.get('hostname')}: {e}")
            facts_list.append({
                'hostname': device_info.get('hostname', 'unknown'),
                'error': str(e)
            })
    
    return facts_list


# ============================================================================
# Demonstration
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEVICE MANAGEMENT EXAMPLES")
    print("=" * 70)
    
    # Example 1: Netmiko connection
    print("\n1. Netmiko Device Manager")
    device_info = {
        'host': '10.0.0.1',
        'username': 'admin',
        'password': 'secret',
        'device_type': 'cisco_ios'
    }
    
    with NetmikoDeviceManager(device_info) as device:
        version = device.send_command('show version')
        print(f"Version output: {version[:50]}...")
    
    # Example 2: NAPALM facts
    print("\n2. NAPALM Facts Gathering")
    napalm_info = {
        'hostname': '10.0.0.1',
        'username': 'admin',
        'password': 'secret',
        'driver': 'ios'
    }
    
    gatherer = NAPALMFactsGatherer(napalm_info)
    gatherer.connect()
    facts = gatherer.get_facts()
    print(f"Hostname: {facts.get('hostname')}")
    print(f"Vendor: {facts.get('vendor')}")
    gatherer.close()
    
    # Example 3: Safe config deployment
    print("\n3. Safe Configuration Deployment")
    deployer = SafeConfigDeployer(gatherer.connection)
    new_config = "interface GigabitEthernet0/1\nip address 10.0.0.2 255.255.255.0"
    result = deployer.deploy_config(new_config, dry_run=True)
    print(f"Dry-run result: {result['success']}")
    
    # Example 4: Backup
    print("\n4. Configuration Backup")
    device_mgr = NetmikoDeviceManager(device_info)
    device_mgr.connect()
    backup_mgr = DeviceBackupManager(device_mgr, backup_dir="/tmp/backups")
    backup_path = backup_mgr.backup_running_config()
    print(f"Backup created: {backup_path}")
    device_mgr.disconnect()
    
    # Example 5: Multi-device
    print("\n5. Multi-Device Facts Gathering")
    devices = [
        {'hostname': 'router1', 'username': 'admin', 'password': 'secret', 'driver': 'ios'},
        {'hostname': 'router2', 'username': 'admin', 'password': 'secret', 'driver': 'ios'}
    ]
    facts_list = gather_facts_from_devices(devices)
    print(f"Gathered facts from {len(facts_list)} devices")
