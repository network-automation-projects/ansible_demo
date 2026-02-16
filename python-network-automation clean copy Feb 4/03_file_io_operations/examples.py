"""
Python Network Automation - File I/O Operations Examples
=========================================================

Complete working examples demonstrating file operations
in real-world network automation scenarios.
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Configuration Backup Manager
# ============================================================================

class ConfigBackupManager:
    """Manages device configuration backups."""
    
    def __init__(self, backup_dir: str = "backups"):
        """
        Initialize backup manager.
        
        Args:
            backup_dir: Directory for storing backups
        """
        self.backup_dir = backup_dir
        self._ensure_backup_directory()
    
    def _ensure_backup_directory(self) -> None:
        """Ensure backup directory exists."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"Created backup directory: {self.backup_dir}")
    
    def backup_config(self, device_name: str, config: str) -> str:
        """
        Backup device configuration to file.
        
        Args:
            device_name: Device hostname
            config: Configuration content
            
        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{device_name}_{timestamp}.txt"
        backup_path = os.path.join(self.backup_dir, filename)
        
        with open(backup_path, 'w') as f:
            f.write(config)
        
        logger.info(f"Backed up config for {device_name} to {backup_path}")
        return backup_path
    
    def list_backups(self, device_name: Optional[str] = None) -> List[str]:
        """
        List backup files.
        
        Args:
            device_name: Optional device name to filter
            
        Returns:
            List of backup file paths
        """
        backups = []
        if os.path.exists(self.backup_dir):
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.txt'):
                    if device_name is None or filename.startswith(device_name):
                        backups.append(os.path.join(self.backup_dir, filename))
        return sorted(backups, reverse=True)  # Most recent first


# ============================================================================
# Example 2: Device Inventory Manager
# ============================================================================

class DeviceInventoryManager:
    """Manages device inventory in JSON format."""
    
    def __init__(self, inventory_file: str = "inventory.json"):
        """
        Initialize inventory manager.
        
        Args:
            inventory_file: Path to inventory JSON file
        """
        self.inventory_file = inventory_file
        self.inventory = self._load_inventory()
    
    def _load_inventory(self) -> List[Dict[str, Any]]:
        """Load inventory from JSON file."""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    inventory = json.load(f)
                    logger.info(f"Loaded {len(inventory)} devices from inventory")
                    return inventory
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing inventory file: {e}")
                return []
        else:
            logger.info("Inventory file not found, starting with empty inventory")
            return []
    
    def save_inventory(self) -> None:
        """Save inventory to JSON file."""
        try:
            with open(self.inventory_file, 'w') as f:
                json.dump(self.inventory, f, indent=2)
            logger.info(f"Saved {len(self.inventory)} devices to inventory")
        except Exception as e:
            logger.error(f"Error saving inventory: {e}")
            raise
    
    def add_device(self, device: Dict[str, Any]) -> None:
        """
        Add device to inventory.
        
        Args:
            device: Device dictionary
        """
        self.inventory.append(device)
        self.save_inventory()
        logger.info(f"Added device: {device.get('hostname', 'unknown')}")
    
    def get_device(self, hostname: str) -> Optional[Dict[str, Any]]:
        """
        Get device by hostname.
        
        Args:
            hostname: Device hostname
            
        Returns:
            Device dictionary or None
        """
        for device in self.inventory:
            if device.get('hostname') == hostname:
                return device
        return None


# ============================================================================
# Example 3: Environment-Based Configuration
# ============================================================================

class ConfigFromEnvironment:
    """Load configuration from environment variables."""
    
    @staticmethod
    def get_netmiko_config() -> Dict[str, Optional[str]]:
        """
        Get Netmiko connection configuration from environment.
        
        Returns:
            Dictionary with connection parameters
        """
        config = {
            'device_type': os.environ.get('NETMIKO_DEVICE_TYPE', 'cisco_ios'),
            'host': os.environ.get('NETMIKO_HOST'),
            'username': os.environ.get('NETMIKO_USERNAME'),
            'password': os.environ.get('NETMIKO_PASSWORD'),
            'secret': os.environ.get('NETMIKO_SECRET'),
            'port': int(os.environ.get('NETMIKO_PORT', '22'))
        }
        
        # Validate required fields
        required = ['host', 'username', 'password']
        missing = [key for key in required if not config.get(key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        
        return config
    
    @staticmethod
    def get_api_config() -> Dict[str, Optional[str]]:
        """
        Get API configuration from environment.
        
        Returns:
            Dictionary with API configuration
        """
        return {
            'api_url': os.environ.get('API_URL', 'https://api.example.com'),
            'api_token': os.environ.get('API_TOKEN'),
            'api_timeout': int(os.environ.get('API_TIMEOUT', '30'))
        }


# ============================================================================
# Example 4: Log File Manager
# ============================================================================

class LogFileManager:
    """Manages log files for automation."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize log manager.
        
        Args:
            log_dir: Directory for log files
        """
        self.log_dir = log_dir
        self._ensure_log_directory()
    
    def _ensure_log_directory(self) -> None:
        """Ensure log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def write_log(self, message: str, level: str = 'INFO', 
                  log_file: Optional[str] = None) -> None:
        """
        Write log entry to file.
        
        Args:
            message: Log message
            level: Log level
            log_file: Optional specific log file (defaults to dated file)
        """
        if log_file is None:
            date_str = datetime.now().strftime('%Y%m%d')
            log_file = os.path.join(self.log_dir, f"automation_{date_str}.log")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
    def read_logs(self, log_file: str, lines: Optional[int] = None) -> List[str]:
        """
        Read log entries from file.
        
        Args:
            log_file: Path to log file
            lines: Optional number of lines to read (from end)
            
        Returns:
            List of log entries
        """
        if not os.path.exists(log_file):
            logger.warning(f"Log file not found: {log_file}")
            return []
        
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
        
        if lines is not None:
            return all_lines[-lines:]
        return all_lines


# ============================================================================
# Example 5: State Persistence Manager
# ============================================================================

class AutomationStateManager:
    """Manages automation state persistence."""
    
    def __init__(self, state_file: str = "automation_state.pkl"):
        """
        Initialize state manager.
        
        Args:
            state_file: Path to state file
        """
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load state from pickle file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'rb') as f:
                    state = pickle.load(f)
                    logger.info("Loaded automation state")
                    return state
            except Exception as e:
                logger.error(f"Error loading state: {e}")
                return {}
        return {}
    
    def save_state(self) -> None:
        """Save state to pickle file."""
        try:
            with open(self.state_file, 'wb') as f:
                pickle.dump(self.state, f)
            logger.info("Saved automation state")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set state value and save."""
        self.state[key] = value
        self.save_state()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple state values."""
        self.state.update(updates)
        self.save_state()


# ============================================================================
# Example 6: Device List Reader
# ============================================================================

def read_device_list_from_file(file_path: str) -> List[str]:
    """
    Read device hostnames from text file (one per line).
    
    Args:
        file_path: Path to text file
        
    Returns:
        List of device hostnames
    """
    devices = []
    
    if not os.path.exists(file_path):
        logger.warning(f"Device list file not found: {file_path}")
        return devices
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                device = line.strip()
                if device and not device.startswith('#'):  # Skip empty lines and comments
                    devices.append(device)
        
        logger.info(f"Loaded {len(devices)} devices from {file_path}")
        return devices
    except Exception as e:
        logger.error(f"Error reading device list: {e}")
        return []


# ============================================================================
# Example 7: Path Utilities
# ============================================================================

class PathUtils:
    """Utility functions for path operations."""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """
        Ensure directory exists, create if needed.
        
        Args:
            path: Directory path
        """
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created directory: {path}")
    
    @staticmethod
    def get_backup_path(base_dir: str, device_name: str, 
                       extension: str = '.txt') -> str:
        """
        Generate backup file path.
        
        Args:
            base_dir: Base directory for backups
            device_name: Device hostname
            extension: File extension
            
        Returns:
            Full path to backup file
        """
        PathUtils.ensure_directory(base_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{device_name}_{timestamp}{extension}"
        return os.path.join(base_dir, filename)
    
    @staticmethod
    def get_absolute_path(relative_path: str) -> str:
        """
        Get absolute path from relative path.
        
        Args:
            relative_path: Relative path
            
        Returns:
            Absolute path
        """
        return os.path.abspath(relative_path)


# ============================================================================
# Demonstration
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FILE I/O OPERATIONS EXAMPLES")
    print("=" * 70)
    
    # Example 1: Config backup
    print("\n1. Configuration Backup")
    backup_mgr = ConfigBackupManager(backup_dir="/tmp/test_backups")
    backup_path = backup_mgr.backup_config('router1', 'interface Eth0\n  ip address 10.0.0.1')
    print(f"Backup created: {backup_path}")
    
    # Example 2: Inventory management
    print("\n2. Device Inventory")
    inventory_mgr = DeviceInventoryManager(inventory_file="/tmp/test_inventory.json")
    inventory_mgr.add_device({'hostname': 'router1', 'ip': '10.0.0.1', 'vendor': 'cisco'})
    device = inventory_mgr.get_device('router1')
    print(f"Retrieved device: {device}")
    
    # Example 3: Environment config
    print("\n3. Environment Configuration")
    # Set env vars before running:
    # export NETMIKO_HOST=10.0.0.1 NETMIKO_USERNAME=admin NETMIKO_PASSWORD=secret
    try:
        config = ConfigFromEnvironment.get_netmiko_config()
        print(f"Config loaded: host={config.get('host')}")
    except ValueError as e:
        print(f"Config error: {e}")
    
    # Example 4: Log management
    print("\n4. Log Management")
    log_mgr = LogFileManager(log_dir="/tmp/test_logs")
    log_mgr.write_log('Test log entry', 'INFO')
    print("Log entry written")
    
    # Example 5: State persistence
    print("\n5. State Persistence")
    state_mgr = AutomationStateManager(state_file="/tmp/test_state.pkl")
    state_mgr.set('devices_processed', 5)
    state_mgr.set('last_device', 'router1')
    print(f"State saved: {state_mgr.get('devices_processed')} devices processed")
    
    # Example 6: Device list
    print("\n6. Device List Reader")
    # Create test file
    with open('/tmp/test_devices.txt', 'w') as f:
        f.write('router1\nrouter2\nrouter3\n')
    devices = read_device_list_from_file('/tmp/test_devices.txt')
    print(f"Devices loaded: {devices}")
    
    # Example 7: Path utilities
    print("\n7. Path Utilities")
    backup_path = PathUtils.get_backup_path('/tmp/backups', 'router1')
    print(f"Backup path: {backup_path}")
