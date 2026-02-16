"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from collections import defaultdict, namedtuple, Counter, deque, OrderedDict
from copy import copy, deepcopy
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def group_interfaces_by_status(interfaces: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """Group interface names by their status."""
    grouped = defaultdict(list)
    for interface in interfaces:
        grouped[interface["status"]].append(interface["name"])
    return dict(grouped)


def create_device_facts_tuple() -> type:
    """Create a DeviceFacts namedtuple class. Fields: hostname, vendor, model, version."""
    DeviceFacts = namedtuple(
        "DeviceFacts", ["hostname", "vendor", "model", "version"]
    )
    return DeviceFacts


def count_interface_statuses(interfaces: List[Dict[str, str]]) -> Dict[str, int]:
    """Count how many interfaces are in each status."""
    statuses = [i["status"] for i in interfaces]
    return dict(Counter(statuses))


def create_telemetry_buffer(max_size: int = 100) -> deque:
    """Create a deque buffer for telemetry data."""
    return deque(maxlen=max_size)


def add_to_buffer(buffer: deque, value: Any) -> None:
    """Add value to buffer (automatically removes oldest if at max size)."""
    buffer.append(value)


def create_config_order() -> OrderedDict:
    """Create an OrderedDict to preserve configuration application order."""
    return OrderedDict()


def duplicate_config_shallow(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a shallow copy of configuration dictionary."""
    return copy(config)


def duplicate_config_deep(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a deep copy of configuration dictionary."""
    return deepcopy(config)


def count_errors_by_device(logs: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """Count error types grouped by device."""
    device_errors = defaultdict(Counter)
    for log in logs:
        device = log["device"]
        error_type = log["error_type"]
        device_errors[device][error_type] += 1
    return {device: dict(counter) for device, counter in device_errors.items()}


if __name__ == "__main__":
    print("02_data_structures – answer key (run exercises.py to practice)")
