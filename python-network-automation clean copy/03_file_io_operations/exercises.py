"""
Python Network Automation - File I/O Operations Exercises
==========================================================

Fill-in-the-blank exercises for learning file operations
in the context of network automation.
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXERCISE 1: Reading Configuration Files
# ============================================================================

"""
Tutorial: open() and File Context Managers
-------------------------------------------

open(file, mode) opens a file. Use 'with' statement for automatic closing.

Modes:
- 'r' - Read (default)
- 'w' - Write (overwrites existing)
- 'a' - Append
- 'r+' - Read and write
- 'b' - Binary mode

Always use 'with' statement to ensure files are closed properly!
"""


def read_config_file(file_path: str) -> str:
    """
    Read a configuration file and return its contents.
    
    Args:
        file_path: Path to configuration file
        
    Returns:
        File contents as string
        
    Example:
        >>> content = read_config_file('config.txt')
        >>> print(content)
        'interface Eth0\n  ip address 10.0.0.1 255.255.255.0'
    """
    # TODO: Fill in the blank - use 'with open()' to read file
    # Hint: with open(file_path, 'r') as f: return f.read()
    with None:  # Fill in open() call
        return None  # Fill in f.read()


# ============================================================================
# EXERCISE 2: Writing Configuration Files
# ============================================================================

def write_config_file(file_path: str, content: str) -> None:
    """
    Write configuration content to a file.
    
    Args:
        file_path: Path to output file
        content: Configuration content to write
        
    Example:
        >>> write_config_file('output.txt', 'interface Eth0')
    """
    # TODO: Fill in the blank - use 'with open()' in write mode
    # Hint: with open(file_path, 'w') as f: f.write(content)
    with None:  # Fill in open() call with 'w' mode
        None  # Fill in f.write(content)


# ============================================================================
# EXERCISE 3: Path Operations
# ============================================================================

"""
Tutorial: os.path Operations
---------------------------

os.path.join() - Join path components (handles OS differences)
os.path.exists() - Check if path exists
os.path.dirname() - Get directory name
os.path.abspath() - Get absolute path
os.getcwd() - Get current working directory
"""


def create_backup_path(device_name: str, backup_dir: str) -> str:
    """
    Create a backup file path for a device configuration.
    
    Args:
        device_name: Device hostname
        backup_dir: Directory for backups
        
    Returns:
        Full path to backup file
        
    Example:
        >>> create_backup_path('router1', '/backups')
        '/backups/router1_20260128_120000.txt'
    """
    # TODO: Fill in the blank - use os.path.join() to create path
    # Generate filename: device_name_timestamp.txt
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{device_name}_{timestamp}.txt"
    # Use os.path.join() to combine backup_dir and filename
    return None  # Fill in os.path.join() call


def ensure_backup_directory(backup_dir: str) -> None:
    """
    Ensure backup directory exists, create if it doesn't.
    
    Args:
        backup_dir: Directory path to ensure exists
    """
    # TODO: Fill in the blank - use os.path.exists() and os.mkdir()
    # Check if directory exists, create if not
    if None:  # Check if backup_dir exists
        None  # Create directory using os.mkdir()


# ============================================================================
# EXERCISE 4: JSON Operations
# ============================================================================

"""
Tutorial: JSON Operations
--------------------------

json.loads(str) - Parse JSON string to Python object
json.dumps(obj) - Convert Python object to JSON string
json.load(file) - Read JSON from file object
json.dump(obj, file) - Write JSON to file object

JSON is great for structured data that needs to be human-readable.
"""


def load_device_inventory(json_file: str) -> List[Dict[str, Any]]:
    """
    Load device inventory from JSON file.
    
    Args:
        json_file: Path to JSON file
        
    Returns:
        List of device dictionaries
        
    Example:
        >>> devices = load_device_inventory('inventory.json')
        >>> print(devices[0]['hostname'])
        'router1'
    """
    # TODO: Fill in the blank - use 'with open()' and json.load()
    with None:  # Open JSON file for reading
        return None  # Use json.load() to parse JSON


def save_device_inventory(devices: List[Dict[str, Any]], json_file: str) -> None:
    """
    Save device inventory to JSON file.
    
    Args:
        devices: List of device dictionaries
        json_file: Path to output JSON file
    """
    # TODO: Fill in the blank - use 'with open()' and json.dump()
    # Hint: Use indent=2 for readable JSON
    with None:  # Open JSON file for writing
        None  # Use json.dump() with indent=2


# ============================================================================
# EXERCISE 5: Environment Variables
# ============================================================================

"""
Tutorial: os.environ
---------------------

os.environ is a dictionary-like object containing environment variables.

Use for:
- API keys and credentials (never hardcode!)
- Configuration values
- Paths and settings

Always provide defaults and handle missing variables gracefully.
"""


def get_api_credentials() -> Dict[str, Optional[str]]:
    """
    Get API credentials from environment variables.
    
    Returns:
        Dictionary with 'username' and 'password' keys
        
    Example:
        >>> # Set env vars: export API_USERNAME=admin API_PASSWORD=secret
        >>> creds = get_api_credentials()
        >>> print(creds['username'])
        'admin'
    """
    # TODO: Fill in the blank - use os.environ.get() with defaults
    # Get 'API_USERNAME' and 'API_PASSWORD' from environment
    return {
        'username': None,  # Use os.environ.get('API_USERNAME')
        'password': None   # Use os.environ.get('API_PASSWORD')
    }


# ============================================================================
# EXERCISE 6: Reading Lines from Files
# ============================================================================

def read_device_list(file_path: str) -> List[str]:
    """
    Read device hostnames from a text file (one per line).
    
    Args:
        file_path: Path to text file
        
    Returns:
        List of device hostnames (stripped of whitespace)
        
    Example:
        >>> devices = read_device_list('devices.txt')
        >>> print(devices)
        ['router1', 'router2', 'router3']
    """
    devices = []
    # TODO: Fill in the blank - read file line by line
    with None:  # Open file for reading
        for None in None:  # Iterate over file lines
            # Strip whitespace and skip empty lines
            line = None  # Strip whitespace from line
            if line:  # If line is not empty
                devices.append(None)  # Add to list
    return devices


# ============================================================================
# EXERCISE 7: Appending to Log Files
# ============================================================================

def append_log_entry(log_file: str, message: str, level: str = 'INFO') -> None:
    """
    Append a log entry to a log file.
    
    Args:
        log_file: Path to log file
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    # TODO: Fill in the blank - use 'a' mode to append
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with None:  # Open file in append mode ('a')
        None  # Write log_entry to file


# ============================================================================
# EXERCISE 8: State Persistence with Pickle
# ============================================================================

"""
Tutorial: pickle
-----------------

pickle.dump(obj, file) - Serialize Python object to file
pickle.load(file) - Deserialize Python object from file

Use pickle for:
- Complex Python objects
- Objects that can't be JSON serialized
- Internal state that doesn't need to be human-readable

Warning: Only unpickle data from trusted sources!
"""


def save_automation_state(state: Dict[str, Any], state_file: str) -> None:
    """
    Save automation state to a pickle file.
    
    Args:
        state: State dictionary to save
        state_file: Path to state file
    """
    # TODO: Fill in the blank - use 'with open()' in binary mode and pickle.dump()
    # Hint: Open with 'wb' mode, use pickle.dump(state, f)
    with None:  # Open file in binary write mode ('wb')
        None  # Use pickle.dump() to save state


def load_automation_state(state_file: str) -> Optional[Dict[str, Any]]:
    """
    Load automation state from a pickle file.
    
    Args:
        state_file: Path to state file
        
    Returns:
        State dictionary or None if file doesn't exist
    """
    # TODO: Fill in the blank - check if file exists, then load
    if None:  # Check if state_file exists
        with None:  # Open file in binary read mode ('rb')
            return None  # Use pickle.load() to restore state
    return None


# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FILE I/O OPERATIONS EXERCISES")
    print("=" * 70)
    
    # Test Exercise 1
    # print("\nExercise 1: Reading Files")
    # # Create a test file first
    # with open('test_config.txt', 'w') as f:
    #     f.write('interface Eth0\n  ip address 10.0.0.1 255.255.255.0')
    # content = read_config_file('test_config.txt')
    # print(content)
    
    # Test Exercise 2
    # print("\nExercise 2: Writing Files")
    # write_config_file('test_output.txt', 'test content')
    # print("File written")
    
    # Test Exercise 3
    # print("\nExercise 3: Path Operations")
    # backup_path = create_backup_path('router1', '/tmp/backups')
    # print(f"Backup path: {backup_path}")
    # ensure_backup_directory('/tmp/test_backup')
    # print("Directory ensured")
    
    # Test Exercise 4
    # print("\nExercise 4: JSON Operations")
    # test_devices = [{'hostname': 'r1', 'ip': '10.0.0.1'}]
    # save_device_inventory(test_devices, 'test_inventory.json')
    # loaded = load_device_inventory('test_inventory.json')
    # print(loaded)
    
    # Test Exercise 5
    # print("\nExercise 5: Environment Variables")
    # # Set: export API_USERNAME=testuser API_PASSWORD=testpass
    # creds = get_api_credentials()
    # print(f"Username: {creds['username']}")
    
    # Test Exercise 6
    # print("\nExercise 6: Reading Lines")
    # # Create test file
    # with open('test_devices.txt', 'w') as f:
    #     f.write('router1\nrouter2\nrouter3\n')
    # devices = read_device_list('test_devices.txt')
    # print(devices)
    
    # Test Exercise 7
    # print("\nExercise 7: Appending Logs")
    # append_log_entry('test.log', 'Test message', 'INFO')
    # print("Log entry appended")
    
    # Test Exercise 8
    # print("\nExercise 8: Pickle State")
    # state = {'devices_processed': 5, 'last_device': 'router1'}
    # save_automation_state(state, 'test_state.pkl')
    # loaded_state = load_automation_state('test_state.pkl')
    # print(loaded_state)
    
    print("\nUncomment test cases above to verify your solutions!")
