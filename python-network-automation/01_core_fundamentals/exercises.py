"""
Python Network Automation - Core Fundamentals Exercises
=======================================================

Fill-in-the-blank exercises for learning essential Python built-ins
in the context of network automation and reliability engineering.
"""

from typing import Any, Dict, List, Optional
import logging
from webbrowser import get

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
    
    Args:
        interface_statuses: List of interface status strings (e.g., ['up', 'up', 'down'])
        
    Returns:
        True if all interfaces are 'up', False otherwise
        
    Example:
        >>> validate_all_interfaces_up(['up', 'up', 'up'])
        True
        >>> validate_all_interfaces_up(['up', 'down', 'up'])
        False
    """
    # TODO: Fill in the blank - use all() to check if all statuses equal 'up'


                

def check_for_critical_alerts(alerts: List[Dict[str, Any]]) -> bool:
    """
    Check if any critical alerts exist in the monitoring system.
    
    Args:
        alerts: List of alert dictionaries with 'severity' key
        
    Returns:
        True if any alert has severity 'critical', False otherwise
        
    Example:
        >>> alerts = [{'severity': 'warning'}, {'severity': 'critical'}]
        >>> check_for_critical_alerts(alerts)
        True
    """
    # TODO: Fill in the blank - use any() to check if any alert has severity 'critical'



# ============================================================================
# EXERCISE 2: Absolute Value for Metrics
# ============================================================================

"""
Tutorial: abs()
---------------

abs(x) returns the absolute value of a number.

In network automation:
- Calculate absolute latency variations
- Measure differences in metrics regardless of direction
- Handle signed values in calculations
"""


def calculate_latency_variation(baseline: float, current: float) -> float:
    """
    Calculate the absolute difference between baseline and current latency.
    
    Args:
        baseline: Baseline latency in milliseconds
        current: Current latency in milliseconds
        
    Returns:
        Absolute difference between the two values
        
    Example:
        >>> calculate_latency_variation(10.5, 12.3)
        1.8
        >>> calculate_latency_variation(10.5, 8.2)
        2.3
    """
    # TODO: Fill in the blank - use abs() to get absolute difference


    # yes, it is correct.
    # it returns the absolute difference between the baseline and current latency.
    # the abs() function is used to ensure that the difference is always positive.
    # the baseline and current latency are in milliseconds.
    # the difference is in milliseconds.
    # the abs() function returns the absolute value of the difference.
    # the abs() function is used to ensure that the difference is always positive.


# ============================================================================
# EXERCISE 3: Enumerate for Indexed Iteration
# ============================================================================

"""
Tutorial: enumerate()
----------------------

enumerate(iterable, start=0) returns an iterator of (index, value) tuples.
#that sounds like a dictionary since it has a key and a value.
#what is the difference between a dictionary and an iterator?
#a dictionary is a collection of key-value pairs.
#an iterator is a collection of values.
#the difference between a dictionary and an iterator is that a dictionary is a collection of key-value pairs and an iterator is a collection of values.
#but in this case, it is an iterator of (index, value) tuples.
#the index is the position of the value in the iterable.
#the value is the value of the iterable.

In network automation:
- Loop over device lists with indices
- Assign sequential IPs or IDs
- Track position in processing queues
"""


def assign_sequential_ips(devices: List[str], base_ip: str) -> Dict[str, str]:
    """
    Assign sequential IP addresses to devices using enumerate.
    
    Args:
        devices: List of device hostnames
        base_ip: Base IP address (e.g., '192.168.1.')
        
    Returns:
        Dictionary mapping device names to IP addresses
        
    Example:
        >>> devices = ['router1', 'router2', 'router3']
        >>> assign_sequential_ips(devices, '10.0.0.') # so this row demonstrates the input
        {'router1': '10.0.0.1', 'router2': '10.0.0.2', 'router3': '10.0.0.3'} #and this row demonstrates the output?
        #yes, it demonstrates the input and the output.
        
    """
    # TODO: Fill in the blank - use enumerate() to get index and device name
    # Hint: Start enumerate at 1, then format IP as f"{base_ip}{index}"
    result = {}






        #yes, it tells the 'type' of what result is.
        #the type is a dictionary. a dictionary of devices?
        #yes, it is a dictionary of devices.


    # for device, device in enumerate(devices, start=1):  # Fill in the blanks # is this correct?
    #     result[device] = f"{base_ip}{device}"  # Fill in the blanks
    # return result


# ============================================================================
# EXERCISE 4: Zip for Parallel Iteration
# ============================================================================

"""
Tutorial: zip()
----------------
zip(*iterables) creates an iterator that aggregates elements from iterables.

In network automation:
- Pair device names with IPs
- Combine multiple data sources
- Process related data in parallel
"""
def pair_devices_with_ips(device_names: List[str], ip_addresses: List[str]) -> List[tuple]:
    """
    Create pairs of device names and IP addresses.
    
    Args:
        device_names: List of device hostnames
        ip_addresses: List of IP addresses (same length as device_names)
        
    Returns:
        List of (device_name, ip_address) tuples # how many can a tuple have, could it be device name, ip and alt_name?
        # yes, it can be device name, ip and alt_name.
        # the tuple is a collection of values.
        # the values are the device name, ip and alt_name.
        # the device name is the first value, the ip is the second value, and the alt_name is the third value.
        # the tuple is a collection of values.
        #so a tuple could have any number of values.?
        #yes, a tuple could have any number of values.
        
    Example:
        >>> names = ['router1', 'router2']
        >>> ips = ['10.0.0.1', '10.0.0.2']
        >>> pair_devices_with_ips(names, ips)
        [('router1', '10.0.0.1'), ('router2', '10.0.0.2')]
    """
    # TODO: Fill in the blank - use zip() to pair names with IPs



# ============================================================================
# EXERCISE 5: Filter for Conditional Selection
# ============================================================================

"""
Tutorial: filter()
-------------------

filter(function, iterable) constructs an iterator from elements where function returns True.

In network automation:
- Filter devices that need configuration updates
- Find interfaces matching criteria
- Select items based on conditions
"""


def filter_devices_needing_update(devices: List[Dict[str, Any]], target_version: str) -> List[Dict[str, Any]]:
    """
    Filter devices that need software updates.
    
    Args:
        devices: List of device dictionaries with 'version' key
        target_version: Target software version to compare against
        
    Returns:
        List of devices where version != target_version
        
    Example:
        >>> devices = [
        ...     {'name': 'r1', 'version': '15.1'},
        ...     {'name': 'r2', 'version': '15.2'},
        ... ]
        >>> filter_devices_needing_update(devices, '15.2')
        [{'name': 'r1', 'version': '15.1'}]
    """
    # TODO: Fill in the blank - use filter() with a lambda function
    # Hint: lambda d: d['version'] != target_version


    # or
    #return [d for d in devices if d["version"] != target_version]

# ============================================================================
# EXERCISE 6: Map for Transformations
# ============================================================================

"""
Tutorial: map()
----------------

map(function, iterable) applies function to all items and returns an iterator.

In network automation:
- Transform device data formats
- Process configs in parallel
- Convert data types across collections
"""


def extract_device_hostnames(devices: List[Dict[str, Any]]) -> List[str]:
    """
    Extract hostnames from device dictionaries.
    
    Args:
        devices: List of device dictionaries with 'hostname' key
        
    Returns:
        List of hostname strings
        
    Example:
        >>> devices = [{'hostname': 'r1'}, {'hostname': 'r2'}]
        >>> extract_device_hostnames(devices)
        ['r1', 'r2']
    """
    # TODO: Fill in the blank - use map() with a lambda to extract 'hostname'



# ============================================================================
# EXERCISE 7: Sorted for Ordering
# ============================================================================

"""
Tutorial: sorted()
-------------------

sorted(iterable, key=None, reverse=False) returns a new sorted list.

In network automation:
- Sort devices by priority or IP address
- Order interfaces by name or status
- Arrange data for reports
"""


def sort_devices_by_priority(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort devices by priority (higher priority first).
    
    Args:
        devices: List of device dictionaries with 'priority' key
        
    Returns:
        Sorted list of devices (highest priority first)
        
    Example:
        >>> devices = [{'name': 'r1', 'priority': 3}, {'name': 'r2', 'priority': 1}]
        >>> sort_devices_by_priority(devices)
        [{'name': 'r1', 'priority': 3}, {'name': 'r2', 'priority': 1}]
    """
    # TODO: Fill in the blank - use sorted() with key=lambda and reverse=True



# ============================================================================
# EXERCISE 8: Min/Max/Sum for Aggregations
# ============================================================================

"""
Tutorial: min(), max(), sum()
------------------------------

min(iterable) returns the smallest item.
max(iterable) returns the largest item.
sum(iterable, start=0) sums all items.

In network automation:
- Find peak latency in metrics
- Calculate total bandwidth
- Detect minimum uptime for maintenance
"""


def find_peak_latency(latencies: List[float]) -> float:
    """
    Find the maximum latency value.
    
    Args:
        latencies: List of latency values in milliseconds
        
    Returns:
        Maximum latency value
        
    Example:
        >>> find_peak_latency([10.5, 12.3, 8.7, 15.2])
        15.2
    """
    # TODO: Fill in the blank - use max() to find peak latency
    return float(max(latencies)) if latencies else 0.0

def calculate_total_bandwidth(bandwidths: List[float]) -> float:
    """
    Calculate total bandwidth across all interfaces.
    
    Args:
        bandwidths: List of bandwidth values in Mbps
        
    Returns:
        Sum of all bandwidth values
        
    Example:
        >>> calculate_total_bandwidth([100, 1000, 100])
        1200.0
    """
    # TODO: Fill in the blank - use sum() to calculate total




# ============================================================================
# EXERCISE 9: Type Checking with isinstance
# ============================================================================

"""
Tutorial: isinstance()
-----------------------

isinstance(object, classinfo) returns True if object is an instance of classinfo.

In network automation:
- Validate API response types
- Type checking for robust error handling
- Ensure data structures match expectations
"""


def validate_api_response(response: Any) -> bool:
    """
    Validate that API response is a dictionary.
    
    Args:
        response: API response object
        
    Returns:
        True if response is a dict, False otherwise
        
    Example:
        >>> validate_api_response({'status': 'ok'})
        True
        >>> validate_api_response('error')
        False
    """
    # TODO: Fill in the blank - use isinstance() to check if response is dict



# ============================================================================
# EXERCISE 10: Attribute Checking with hasattr/getattr
# ============================================================================

"""
Tutorial: hasattr(), getattr()
-------------------------------

hasattr(object, name) returns True if object has attribute name.
getattr(object, name, default) returns attribute value or default.

In network automation:
- Feature detection on network libraries
- Dynamic attribute access in generic handlers
- Checking for optional methods before calling
"""


def safe_get_device_method(device: Any, method_name: str) -> Optional[Any]:
    """
    Safely get a method from a device object if it exists.
    
    Args:
        device: Device object
        method_name: Name of the method to retrieve
        
    Returns:
        Method if it exists, None otherwise
        
    Example:
        >>> class Device:
        ...     def get_facts(self): return {}
        >>> d = Device()
        >>> safe_get_device_method(d, 'get_facts')
        <bound method Device.get_facts...>
    """
    # TODO: Fill in the blank - use hasattr() to check, then getattr() to retrieve






# ============================================================================
# EXERCISE 11: String Formatting and Conversion
# ============================================================================

"""
Tutorial: str(), format(), repr()
-----------------------------------

str(object) converts object to string.
format(value, format_spec) formats value using format specifier.
repr(object) returns printable representation.

In network automation:
- Convert data to strings for API payloads
- Format metrics for reports
- Generate debug output
"""


def format_bandwidth_report(device_name: str, bandwidth_mbps: float) -> str:
    """
    Format a bandwidth report string.
    
    Args:
        device_name: Device hostname
        bandwidth_mbps: Bandwidth in Mbps
        
    Returns:
        Formatted report string
        
    Example:
        >>> format_bandwidth_report('router1', 1000.5)
        'Device router1: 1000.50 Mbps'
    """
    # TODO: Fill in the blank - use format() or f-string to format the report




# ============================================================================
# EXERCISE 12: Binary and Hex Conversions
# ============================================================================

"""
Tutorial: bin(), hex(), oct()
------------------------------

bin(x) converts integer to binary string with '0b' prefix.
hex(x) converts integer to hexadecimal string with '0x' prefix.
oct(x) converts integer to octal string with '0o' prefix.

In network automation:
- Debug binary flags in network protocols
- Format MAC addresses in hex
- Work with IP masks and subnet calculations
"""


def format_mac_address_as_hex(mac_int: int) -> str:
    """
    Format a MAC address integer as hexadecimal string.
    
    Args:
        mac_int: MAC address as integer
        
    Returns:
        Hexadecimal string representation
        
    Example:
        >>> format_mac_address_as_hex(281474976710655)
        '0xffffffffffff'
    """
    # TODO: Fill in the blank - use hex() to convert integer to hex string



# ============================================================================
# EXERCISE 13: Round for Precision
# ============================================================================

"""
Tutorial: round()
-----------------

round(number, ndigits) rounds number to ndigits decimal places.

In network automation:
- Format floating-point metrics for reports
- Round CPU usage percentages
- Display latency with appropriate precision
"""


def format_cpu_usage(cpu_percent: float) -> str:
    """
    Format CPU usage percentage with 2 decimal places.
    
    Args:
        cpu_percent: CPU usage as float (e.g., 45.6789)
        
    Returns:
        Formatted string with 2 decimal places
        
    Example:
        >>> format_cpu_usage(45.6789)
        '45.68%'
    """
    # TODO: Fill in the blank - use round() to round to 2 decimal places





# ============================================================================
# EXERCISE 14: Length and Range
# ============================================================================

"""
Tutorial: len(), range()
-------------------------

len(container) returns the number of items.
range(start, stop, step) creates an immutable sequence of numbers.

In network automation:
- Count interfaces or routes
- Generate sequences for iteration
- Create numbered lists
"""


def count_interfaces(interface_list: List[str]) -> int:
    """
    Count the number of interfaces.
    
    Args:
        interface_list: List of interface names
        
    Returns:
        Number of interfaces
        
    Example:
        >>> count_interfaces(['Eth0', 'Eth1', 'Eth2'])
        3
    """
    # TODO: Fill in the blank - use len() to count interfaces



def generate_port_numbers(start: int, end: int) -> List[int]:
    """
    Generate a list of port numbers in a range.
    
    Args:
        start: Starting port number
        end: Ending port number (exclusive)
        
    Returns:
        List of port numbers
        
    Example:
        >>> generate_port_numbers(8000, 8003)
        [8000, 8001, 8002]
    """
    # TODO: Fill in the blank - use range() and list() to generate port numbers
    # mylist = []
    # for i in range(start, end, 1):
    #     #add to list
    #     mylist.append(i)

    # return list(mylist)




# ============================================================================
# EXERCISE 15: Modulo for Bounded, Deterministic Behavior
# ============================================================================

"""
Tutorial: Modulo (%)
--------------------

Modulo gives bounded, repeatable, evenly-distributed behavior instead of
unbounded growth or special-case logic. Same idea as wrapping from 'z' back to 'a'.

In network automation:
- Round-robin across devices, NTP servers, or API endpoints
- Rate-limit or throttle every N operations (avoid API bans, CPU spikes)
- Shard/partition work across workers without shared state or locks
- Retry with bounded backoff (fixed list of delays, no index errors)
- Change batching / rollout windows (clear phases, pause points, rollback boundaries)
- Stable selection: same device -> same controller every time, even distribution

Interview framing: "Modulo lets me enforce periodic guardrails and keep behavior
predictable without tracking extra state."
"""


def round_robin_device(devices: List[str], index: int) -> str:
    """
    Pick a device by index, wrapping around when index >= len(devices).

    Args:
        devices: List of device hostnames (e.g. ["r1", "r2", "r3"])
        index: Arbitrary counter (can grow forever)

    Returns:
        expression to select the device, wrapping at the end

    Example:
        >>> round_robin_device(["r1", "r2", "r3"], 0)
        'r1'
        >>> round_robin_device(["r1", "r2", "r3"], 5)
        'r3'
    """
    # TODO: Fill in the blank - use index % len(devices) to keep index in range





def should_throttle(operation_index: int, every_n: int) -> bool:
    """
    Return True when we should pause (e.g. every N operations for rate-limiting).

    Args:
        operation_index: 0-based index of the current operation
        every_n: Pause when operation_index is divisible by this (e.g. 10)

    Returns:
        True when we should pause (e.g. every N operations for rate-limiting).

    Example:
        >>> should_throttle(10, 10)
        True
        >>> should_throttle(11, 10)
        False
    """
    # TODO: Fill in the blank - use modulo to detect every Nth operation





def device_belongs_to_worker(
    device_id: int, worker_id: int, num_workers: int
) -> bool:
    """
    Return True if this worker should process this device when work is split across
    num_workers (deterministic sharding). Each device is assigned to exactly one
    worker to give each worker a bucket 0..num_workers-1;
    this worker should process the device only when that bucket equals worker_id.

    Worker 0 gets devices 0, num_workers, 2*num_workers, ...
    Worker 1 gets 1, num_workers+1, ...
    No coordination or shared state needed.

    Args:
        device_id: Integer device id (e.g. from enumerate or DB id)
        worker_id: This worker's id (0 to num_workers - 1)
        num_workers: Total number of workers

    Returns:
        True if device_id % num_workers == worker_id

    Example:
        >>> device_belongs_to_worker(6, 2, 4)
        True
        >>> device_belongs_to_worker(5, 2, 4)
        False
    """
    # TODO: Fill in the blank with the correct modulo to spread out the workload





def backoff_delay_seconds(delays: List[int], attempt: int) -> int:
    """
    Return delay in seconds for this attempt, cycling through delays (bounded backoff).

    Args:
        delays: List of delay values in seconds (e.g. [1, 2, 4, 8])
        attempt: 0-based attempt number (can be large; no index error)

    Returns:
        delays[attempt % len(delays)]

    Example:
        >>> backoff_delay_seconds([1, 2, 4, 8], 0)
        1
        >>> backoff_delay_seconds([1, 2, 4, 8], 6)
        4
    """
    # TODO: Fill in the blank - use attempt % len(delays) to index into delays





def is_start_of_batch(index: int, batch_size: int) -> bool:
    """
    Return True when index starts a new batch (for rollout windows / batching).

    Args:
        index: 0-based index of current item
        batch_size: Size of each batch (e.g. 10)

    Returns:
        True if index % batch_size == 0

    Example:
        >>> is_start_of_batch(0, 10)
        True
        >>> is_start_of_batch(20, 10)
        True
        >>> is_start_of_batch(15, 10)
        False
    """
    # TODO: Fill in the blank - use index % batch_size == 0





def stable_controller_for_device(
    controllers: List[str], device_name: str
) -> str:
    """
    Pick a controller for this device deterministically (same device -> same controller).

    Even distribution without stored mapping. In production you might use a
    stable hash (e.g. consistent hashing) if controller set changes.

    Args:
        controllers: List of controller hostnames
        device_name: Device identifier (e.g. hostname)

    Returns:
        controllers[hash(device_name) % len(controllers)]

    Example:
        >>> stable_controller_for_device(["ctrl1", "ctrl2"], "router1")
        'ctrl1' or 'ctrl2' (deterministic for same router1)
    """
    # TODO: Fill in the blank - use hash(device_name) % len(controllers)



# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CORE FUNDAMENTALS EXERCISES")
    print("=" * 70)
    
    # Test Exercise 1
    print("\nExercise 1: all() and any()")
    print(validate_all_interfaces_up(['up', 'up', 'up']))  # Should be True
    print(validate_all_interfaces_up(['up', 'down', 'up']))  # Should be False
    alerts = [{'severity': 'warning'}, {'severity': 'critical'}]
    print(check_for_critical_alerts(alerts))  # Should be True
    
    # Test Exercise 2
    # print("\nExercise 2: abs()")
    # print(calculate_latency_variation(10.5, 12.3))  # Should be 1.8
    
    # Test Exercise 3
    # print("\nExercise 3: enumerate()")
    # devices = ['router1', 'router2', 'router3']
    # print(assign_sequential_ips(devices, '10.0.0.'))
    # Expected: {'router1': '10.0.0.1', 'router2': '10.0.0.2', 'router3': '10.0.0.3'}
    
    # Test Exercise 4
    # print("\nExercise 4: zip()")
    # names = ['router1', 'router2']
    # ips = ['10.0.0.1', '10.0.0.2']
    # print(pair_devices_with_ips(names, ips))
    # Expected: [('router1', '10.0.0.1'), ('router2', '10.0.0.2')]
    
    # Test Exercise 5
    # print("\nExercise 5: filter()")
    # devices = [{'name': 'r1', 'version': '15.1'}, {'name': 'r2', 'version': '15.2'}]
    # print(filter_devices_needing_update(devices, '15.2'))
    # Expected: [{'name': 'r1', 'version': '15.1'}]
    
    # Test Exercise 6
    # print("\nExercise 6: map()")
    # devices = [{'hostname': 'r1'}, {'hostname': 'r2'}]
    # print(extract_device_hostnames(devices))
    # Expected: ['r1', 'r2']
    
    # Test Exercise 7
    # print("\nExercise 7: sorted()")
    # devices = [{'name': 'r1', 'priority': 3}, {'name': 'r2', 'priority': 1}]
    # print(sort_devices_by_priority(devices))
    # Expected: [{'name': 'r1', 'priority': 3}, {'name': 'r2', 'priority': 1}]
    
    # Test Exercise 8
    # print("\nExercise 8: min/max/sum()")
    # print(find_peak_latency([10.5, 12.3, 8.7, 15.2]))  # Should be 15.2
    # print(calculate_total_bandwidth([100, 1000, 100]))  # Should be 1200.0
    
    # Test Exercise 9
    # print("\nExercise 9: isinstance()")
    # print(validate_api_response({'status': 'ok'}))  # Should be True
    # print(validate_api_response('error'))  # Should be False
    
    # Test Exercise 10
    # print("\nExercise 10: hasattr/getattr()")
    # class Device:
    #     def get_facts(self): return {}
    # d = Device()
    # print(safe_get_device_method(d, 'get_facts') is not None)  # Should be True
    # print(safe_get_device_method(d, 'nonexistent') is None)  # Should be True
    
    # Test Exercise 11
    # print("\nExercise 11: str/format()")
    # print(format_bandwidth_report('router1', 1000.5))
    # Expected: 'Device router1: 1000.50 Mbps'
    
    # Test Exercise 12
    # print("\nExercise 12: hex()")
    # print(format_mac_address_as_hex(281474976710655))
    # Expected: '0xffffffffffff'
    
    # Test Exercise 13
    # print("\nExercise 13: round()")
    # print(format_cpu_usage(45.6789))  # Should be '45.68%'
    
    # Test Exercise 14
    # print("\nExercise 14: len() and range()")
    # print(count_interfaces(['Eth0', 'Eth1', 'Eth2']))  # Should be 3
    print(generate_port_numbers(8000, 8003))  # Should be [8000, 8001, 8002]

    # Test Exercise 15
    # print("\nExercise 15: Modulo")
    # print(round_robin_device(["r1", "r2", "r3"], 0))   # Should be r1
    # print(round_robin_device(["r1", "r2", "r3"], 5))   # Should be r3
    # print(should_throttle(10, 10))   # Should be True
    # print(should_throttle(11, 10))   # Should be False
    # print(device_belongs_to_worker(6, 2, 4))   # Should be True
    # print(device_belongs_to_worker(5, 2, 4))   # Should be False
    # print(backoff_delay_seconds([1, 2, 4, 8], 0))   # Should be 1
    # print(backoff_delay_seconds([1, 2, 4, 8], 6))   # Should be 4
    # print(is_start_of_batch(0, 10))   # Should be True
    # print(is_start_of_batch(20, 10))   # Should be True
    # print(is_start_of_batch(15, 10))   # Should be False
    # print(stable_controller_for_device(["ctrl1", "ctrl2"], "router1"))  # Deterministic

    print("\nUncomment test cases above to verify your solutions!")
