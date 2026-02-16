"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Any, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXERCISE 1: Data Validation with all() and any()
# ============================================================================

"""
Tutorial: all() and any()
--------------------------

all(iterable) returns True if ALL elements are truthy (or if iterable is empty).
any(iterable) returns True if ANY element is truthy.

In network automation:
- Use all() to verify all devices/interfaces meet conditions before changes
- Use any() to check if any alerts exist to trigger automated responses
"""


def validate_all_interfaces_up(interface_statuses: List[str]) -> bool:
    """
    Check if all interfaces are in 'up' state before applying configuration.
    """
    return all(status == "up" for status in interface_statuses) # so test each status in interfaces_statuses to see if status == 'up' is true or false, if so, yield true.  exit at the first false
                                                                # so a generator reads like: if _ condition is true for this _ in the list of _ yield the 'answer'

# For each status, yield True/False; all() returns True only if all are True, and stops at first False.
# Generator: for each _ in the list, yield the result of (condition) — here, True or False.

def check_for_critical_alerts(alerts: List[Dict[str, Any]]) -> bool:
    """
    Check if any critical alerts exist in the monitoring system.
    """
    return any(alert.get("severity") == "critical" for alert in alerts)     #alert is the item (in this case a dictionary), so we need to .get the severity 


# ============================================================================
# EXERCISE 2: Absolute Value for Metrics
# ============================================================================

def calculate_latency_variation(baseline: float, current: float) -> float:
    """
    Calculate the absolute difference between baseline and current latency.
    """
    if not baseline is None and not current is None:        #they can pass in None which when subtracted would cause an error
        return abs(baseline - current)
    else:
        return None


# ============================================================================
# EXERCISE 3: Enumerate for Indexed Iteration
# ============================================================================

def assign_sequential_ips(devices: List[str], base_ip: str) -> Dict[str, str]:
    """
    Assign sequential IP addresses to devices using enumerate.
    """
    result = {}
    for index, device in enumerate(devices, start=1):
        result[device] = f"{base_ip}{index}"
    return result


# ============================================================================
# EXERCISE 4: Zip for Parallel Iteration
# ============================================================================

def pair_devices_with_ips(device_names: List[str], ip_addresses: List[str]) -> List[tuple]:
    """
    Create pairs of device names and IP addresses.
    """
    return list[tuple[str, str]](zip(device_names, ip_addresses))


# ============================================================================
# EXERCISE 5: Filter for Conditional Selection
# ============================================================================

def filter_devices_needing_update(devices: List[Dict[str, Any]], target_version: str) -> List[Dict[str, Any]]:
    """
    Filter devices that need software updates.
    """
    return list[Dict[str, Any]](filter[Dict[str, Any]](lambda d: d["version"] != target_version, devices))

    # we don't need devices.items() here because devices is a list of dictionaries not a dictionary itself
    # filter iterates over any iterable, so it grabs the whole device from devices

    # devices is a list of dictionaries: [dict1, dict2, dict3, ...]
    # d is a single element from that list, so it’s one of those dictionaries.
    # d["version"] uses the key "version" to get its value in that dictionary.

    # if devices were a list of strings instead devices_different = ["r1", "r2", "r3"]
    # you would get at the first element directly: first_string = devices_different[0]   # "r1"
    # if iterating over devices_different, you would get the string in d like:
    # for d in devices_different:
    # # first iteration: d == "r1"
    # # second iteration: d == "r2"
    # ...

# ============================================================================
# EXERCISE 6: Map for Transformations
# ============================================================================

def extract_device_hostnames(devices: List[Dict[str, Any]]) -> List[str]:
    """
    Extract hostnames from device dictionaries.
    """
    return list(map(lambda d: d["hostname"], devices))


# ============================================================================
# EXERCISE 7: Sorted for Ordering
# ============================================================================

def sort_devices_by_priority(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort devices by priority (higher priority first).
    """
    return sorted(devices, key=lambda d: d.get("priority", 0), reverse=True)  # sort the devices based on priority. if priority key doesn't exist, treat it like priority 0   
                                                                            # sorted returns a list already

# ============================================================================
# EXERCISE 8: Min/Max/Sum for Aggregations
# ============================================================================

def find_peak_latency(latencies: List[float]) -> float:
    """
    Find the maximum latency value.
    """
    return max(latencies) if latencies else 0.0


def calculate_total_bandwidth(bandwidths: List[float]) -> float:
    """
    Calculate total bandwidth across all interfaces.
    """
    return sum(bandwidths)


# ============================================================================
# EXERCISE 9: Type Checking with isinstance
# ============================================================================

def validate_api_response(response: Any) -> bool:
    """
    Validate that API response is a dictionary.
    """
    return isinstance(response, dict)


# ============================================================================
# EXERCISE 10: Attribute Checking with hasattr/getattr
# ============================================================================

def safe_get_device_method(device: Any, method_name: str) -> Optional[Any]:
    """
    Safely get a method from a device object if it exists.
    """
    if hasattr(device, method_name):
        return getattr(device, method_name)
    return None


# ============================================================================
# EXERCISE 11: String Formatting and Conversion
# ============================================================================

def format_bandwidth_report(device_name: str, bandwidth_mbps: float) -> str:
    """
    Format a bandwidth report string.
    """
    return f"Device {device_name}: {bandwidth_mbps:.2f} Mbps"


# ============================================================================
# EXERCISE 12: Binary and Hex Conversions
# ============================================================================

def format_mac_address_as_hex(mac_int: int) -> str:
    """
    Format a MAC address integer as hexadecimal string.
    """
    return hex(mac_int)


# ============================================================================
# EXERCISE 13: Round for Precision
# ============================================================================

def format_cpu_usage(cpu_percent: float) -> str:
    """
    Format CPU usage percentage with 2 decimal places.
    """
    rounded = round(cpu_percent, 2)
    return f"{rounded}%"


# ============================================================================
# EXERCISE 14: Length and Range
# ============================================================================

def count_interfaces(interface_list: List[str]) -> int:
    """
    Count the number of interfaces.
    """
    return len(interface_list)


def generate_port_numbers(start: int, end: int) -> List[int]:
    """
    Generate a list of port numbers in a range.
    """
    return list(range(start, end))


# ============================================================================
# EXERCISE 15: Modulo for Bounded, Deterministic Behavior
# ============================================================================

def round_robin_device(devices: List[str], index: int) -> str:
    """
    Pick a device by index, wrapping around when index >= len(devices).
    """
    return devices[index % len(devices)]


def should_throttle(operation_index: int, every_n: int) -> bool:
    """
    Return True when we should pause (e.g. every N operations for rate-limiting).
    """
    return operation_index % every_n == 0  # this works because 0 % 10 = 0 and 10 % 10 = 0 and 20 % 10 = 0
    # 10 % 10 = 0
    # 11 % 10 = 1
    # 12 % 10 = 2
    # 13 % 10 = 3
    # 10 % 10 = 0
    # 20 % 10 = 0


def device_belongs_to_worker(
    device_id: int, worker_id: int, num_workers: int
) -> bool:
    """
    Return True if this worker should process this device (deterministic sharding).
    """
    return device_id % num_workers == worker_id


def backoff_delay_seconds(delays: List[int], attempt: int) -> int:
    """
    Return delay in seconds for this attempt, cycling through delays (bounded backoff).
    """
    return delays[attempt % len(delays)]


def is_start_of_batch(index: int, batch_size: int) -> bool:
    """
    Return True when index starts a new batch (for rollout windows / batching).
    """
    return index % batch_size == 0


def stable_controller_for_device(
    controllers: List[str], device_name: str
) -> str:
    """
    Pick a controller for this device deterministically (same device -> same controller).
    """
    return controllers[hash(device_name) % len(controllers)]    # hash gives the same number for that device on each run. modulo maps it to an index 0 to len(controllers) - 1


if __name__ == "__main__":
    print("01_core_fundamentals – answer key (run exercises.py to practice)")
