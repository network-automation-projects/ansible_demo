"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
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


def read_config_file(file_path: str) -> str:
    """Read a configuration file and return its contents."""
    with open(file_path, "r") as f:
        return f.read()


def write_config_file(file_path: str, content: str) -> None:
    """Write configuration content to a file."""
    with open(file_path, "w") as f:
        f.write(content)                #this would overrite the whole file's contents?


def create_backup_path(device_name: str, backup_dir: str) -> str:
    """Create a backup file path for a device configuration."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{device_name}_{timestamp}.txt"
    return os.path.join(backup_dir, filename)


def ensure_backup_directory(backup_dir: str) -> None:
    """Ensure backup directory exists, create if it doesn't."""
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)


def load_device_inventory(json_file: str) -> List[Dict[str, Any]]:
    """Load device inventory from JSON file."""
    with open(json_file, "r") as f:
        return json.load(f)           #  json.load returns a python object based on the file. 
                                    # if file has objects, it will become a python dict
                                    # if file has array, it will become python list


def save_device_inventory(devices: List[Dict[str, Any]], json_file: str) -> None:
    """Save device inventory to JSON file."""
    with open(json_file, "w") as f:         #will create file if it doesn't exist?
        json.dump(devices, f, indent=2)


def get_api_credentials() -> Dict[str, Optional[str]]:
    """Get API credentials from environment variables."""
    return {
        "username": os.environ.get("API_USERNAME"),
        "password": os.environ.get("API_PASSWORD"),
    }


def read_device_list(file_path: str) -> List[str]:
    """Read device hostnames from a text file (one per line)."""
    devices = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                devices.append(line)
    return devices


def append_log_entry(log_file: str, message: str, level: str = 'INFO') -> None:
    """Append a log entry to a log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with open(log_file, "a") as f:
        f.write(log_entry)


def save_automation_state(state: Dict[str, Any], state_file: str) -> None:
    """Save automation state to a pickle file."""
    with open(state_file, "wb") as f:
        pickle.dump(state, f)


def load_automation_state(state_file: str) -> Optional[Dict[str, Any]]:
    """Load automation state from a pickle file. Returns None if file doesn't exist."""
    if os.path.exists(state_file):
        with open(state_file, "rb") as f:
            return pickle.load(f)
    return None


if __name__ == "__main__":
    print("03_file_io_operations – answer key (run exercises.py to practice)")
