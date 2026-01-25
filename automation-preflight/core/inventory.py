"""YAML inventory loading and validation."""

import os
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import yaml
from pydantic import ValidationError

from models.device import DeviceInventory

logger = logging.getLogger(__name__)


def get_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Get credentials from environment variables.

    Returns:
        tuple: (username, password) from NET_USER and NET_PASS env vars
    """
    username = os.environ.get("NET_USER")
    password = os.environ.get("NET_PASS")
    return username, password


def load_inventory(inventory_file: str = "config/inventory.yaml") -> List[DeviceInventory]:
    """
    Load device inventory from YAML file.

    Args:
        inventory_file: Path to inventory YAML file

    Returns:
        List of DeviceInventory objects

    Raises:
        FileNotFoundError: If inventory file doesn't exist
        yaml.YAMLError: If YAML parsing fails
        ValidationError: If inventory structure is invalid
    """
    inventory_path = Path(inventory_file)

    if not inventory_path.exists():
        logger.error(f"Inventory file {inventory_file} not found")
        raise FileNotFoundError(f"Inventory file {inventory_file} not found")

    try:
        with open(inventory_path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "devices" not in data:
            raise ValueError("Inventory YAML must contain a 'devices' key with a list")

        devices_raw = data.get("devices", [])
        if not isinstance(devices_raw, list):
            raise ValueError("'devices' must be a list")

        username, password = get_credentials()

        devices = []
        for idx, device_dict in enumerate(devices_raw):
            if not isinstance(device_dict, dict):
                logger.warning(f"Skipping invalid device entry at index {idx}: not a dictionary")
                continue

            device_dict = device_dict.copy()

            if username and "username" not in device_dict:
                device_dict["username"] = username
            if password and "password" not in device_dict:
                device_dict["password"] = password

            try:
                device = DeviceInventory(**device_dict)
                devices.append(device)
            except ValidationError as e:
                logger.error(f"Invalid device entry at index {idx}: {e}")
                raise

        logger.info(f"Loaded {len(devices)} devices from inventory")
        return devices

    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML file {inventory_file}: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to load inventory file {inventory_file}: {e}")
        raise
