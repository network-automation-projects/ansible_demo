"""
Python Network Automation - Data Structures Exercises (ANSWER KEY)
===================================================================

Same structure as exercises.py with all blanks filled in.
Use this file to verify your solutions.
"""

from collections import defaultdict, namedtuple, Counter, deque, OrderedDict
from copy import copy, deepcopy
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXERCISE 1: defaultdict for Grouping
# ============================================================================

"""
Tutorial: defaultdict
---------------------

defaultdict(factory_function) creates a dictionary that automatically creates
default values for missing keys using the factory function.

In network automation:
- Group interfaces by status without checking if key exists
- Aggregate statistics by device without key initialization
- Organize devices by vendor or site automatically
"""


def group_interfaces_by_status(interfaces: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Group interface names by their status.

    Args:
        interfaces: List of interface dictionaries with 'name' and 'status' keys

    Returns:
        Dictionary mapping status to list of interface names

    Example:
        >>> interfaces = [
        ...     {'name': 'Eth0', 'status': 'up'},
        ...     {'name': 'Eth1', 'status': 'down'},
        ...     {'name': 'Eth2', 'status': 'up'}
        ... ]
        >>> group_interfaces_by_status(interfaces)
        {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}
    """
    grouped = defaultdict(list) # this creates the dictionary so that it stays grouped and creates a key when you first access that key.
                                # (in general, the value of the item that goes with that existing or new dictionary key can be an int, list or set.)
                                # in this case, we used list, so when we append a string (interface name) to the list that goes with that key.  
    print(grouped)

    for interface in interfaces:
        grouped[interface["status"]].append(interface["name"])  # for this unique status key, add the interface name to the list 
                                                                # so on the first time we find status 'a', it creates that key in the dictionary along with a blank list and then adds the interface name to that list.
                                                                # on the next pass, it finds the key (status a) and adds to the list for that key the interface name provided.  
    return dict(grouped)        # turn this into a plain dict so it won't create defaults later
                                # leaving it as a defaultdict type of dict could allow typo's to turn into empty list (not the desired result of creating KeyError to alert user)


# ============================================================================
# EXERCISE 2: namedtuple for Structured Data
# ============================================================================

"""
Tutorial: namedtuple
---------------------

namedtuple(typename, field_names) creates a tuple subclass with named fields.

In network automation:
- Represent device facts with named fields
- Create structured interface records
- Model network facts immutably
"""


def create_device_facts_tuple() -> type:
    """
    Create a DeviceFacts namedtuple class.

    Returns:
        DeviceFacts namedtuple class with fields: hostname, vendor, model, version

    Example:
        >>> DeviceFacts = create_device_facts_tuple()
        >>> facts = DeviceFacts('router1', 'cisco', 'ASR1000', '15.1')
        >>> facts.hostname
        'router1'
        >>> facts.vendor
        'cisco'
    """
    DeviceFacts = namedtuple(
        "DeviceFacts", ["hostname", "vendor", "model", "version"]
    )
    return DeviceFacts

    # so this would be like coding this by hand:
    # class DeviceFacts():
    #     def __init__(self, hostname, vendor, model, version):
    #         self.hostname = hostname
    #         self.vendor = vendor
    #         self.model = model
    #         self.version = version



# ============================================================================
# EXERCISE 3: Counter for Counting
# ============================================================================

"""
Tutorial: Counter
-----------------

Counter(iterable) creates a dictionary subclass for counting hashable objects.

In network automation:
- Count error types in logs
- Count interface statuses
- Count device types in inventory
"""


def count_interface_statuses(interfaces: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Count how many interfaces are in each status.

    Args:
        interfaces: List of interface dictionaries with 'status' key

    Returns:
        Dictionary mapping status to count

    Example:
        >>> interfaces = [
        ...     {'name': 'Eth0', 'status': 'up'},
        ...     {'name': 'Eth1', 'status': 'down'},
        ...     {'name': 'Eth2', 'status': 'up'}
        ... ]
        >>> count_interface_statuses(interfaces)
        {'up': 2, 'down': 1}
    """
    statuses = [i["status"] for i in interfaces]  #makes a list of each status in the interfaces dict, in order with dups.
    return dict(Counter(statuses))                #Counter counts how many times each status shows up and turns that into a 
                                                    # regular dictionary with the number of items for each of the status as keys



# ============================================================================
# EXERCISE 4: deque for Buffering
# ============================================================================

"""
Tutorial: deque
---------------

deque(iterable, maxlen) creates a double-ended queue with optional max length.

In network automation:
- Buffer recent telemetry data
- Maintain command history
- Store recent events with automatic size limit
"""


def create_telemetry_buffer(max_size: int = 100) -> deque:
    """
    Create a deque buffer for telemetry data.

    Args:
        max_size: Maximum number of items to store

    Returns:
        deque configured with maxlen

    Example:
        >>> buffer = create_telemetry_buffer(max_size=5)
        >>> buffer.append('metric1')
        >>> buffer.append('metric2')
        >>> len(buffer)
        2
    """
    return deque(maxlen=max_size)


def add_to_buffer(buffer: deque, value: Any) -> None:
    """
    Add value to buffer (automatically removes oldest if at max size).

    Args:
        buffer: deque buffer
        value: Value to add

    Example:
        >>> buffer = deque(maxlen=2)
        >>> add_to_buffer(buffer, 'a')
        >>> add_to_buffer(buffer, 'b')
        >>> add_to_buffer(buffer, 'c')  # 'a' is automatically removed
        >>> list(buffer)
        ['b', 'c']
    """
    buffer.append(value)


# ============================================================================
# EXERCISE 5: OrderedDict for Preserving Order
# ============================================================================

"""
Tutorial: OrderedDict
---------------------

OrderedDict() creates a dictionary that remembers insertion order.

In network automation:
- Preserve config application order
- Maintain sequence of operations
- Track order of device processing
"""


def create_config_order() -> OrderedDict:
    """
    Create an OrderedDict to preserve configuration application order.

    Returns:
        OrderedDict with config steps in order

    Example:
        >>> config = create_config_order()
        >>> config['step1'] = 'configure interface'
        >>> config['step2'] = 'configure routing'
        >>> list(config.keys())
        ['step1', 'step2']
    """
    return OrderedDict()


# ============================================================================
# EXERCISE 6: copy vs deepcopy
# ============================================================================

"""
Tutorial: copy.copy() and copy.deepcopy()
------------------------------------------

copy.copy() creates a shallow copy - copies object but references nested objects.
copy.deepcopy() creates a deep copy - recursively copies all nested objects.

In network automation:
- Use copy() for simple config dictionaries
- Use deepcopy() for nested device state objects
- Avoid modifying originals when duplicating
"""


def duplicate_config_shallow(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a shallow copy of configuration dictionary.

    Args:
        config: Configuration dictionary

    Returns:
        Shallow copy of config

    Note: Nested dictionaries/lists are still referenced, not copied!
    """
    return copy(config)


def duplicate_config_deep(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a deep copy of configuration dictionary.

    Args:
        config: Configuration dictionary (may have nested structures)

    Returns:
        Deep copy of config (all nested structures copied)
    """
    return deepcopy(config)


# ============================================================================
# EXERCISE 7: Combining Collections
# ============================================================================

"""
Tutorial: Combining Collections
--------------------------------

Collections can be combined for powerful data processing:
- defaultdict + Counter for grouped counting
- namedtuple + list for structured collections
- deque + Counter for recent event counting
"""


def count_errors_by_device(logs: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """
    Count error types grouped by device.

    Args:
        logs: List of log dictionaries with 'device' and 'error_type' keys

    Returns:
        Dictionary mapping device to Counter of error types

    Example:
        >>> logs = [
        ...     {'device': 'r1', 'error_type': 'timeout'},
        ...     {'device': 'r1', 'error_type': 'timeout'},
        ...     {'device': 'r2', 'error_type': 'connection'}
        ... ]
        >>> count_errors_by_device(logs)
        {'r1': {'timeout': 2}, 'r2': {'connection': 1}}
    """
    device_errors = defaultdict(Counter)            #make a defaultdict w string keys and counter type values
    for log in logs:                                #for each log in logs dict
        device = log["device"]                      #grab device name
        error_type = log["error_type"]              #grab error type
        device_errors[device][error_type] += 1      #if that device and error type entry doesn't exist, add it.  if it exists, increment the counter?
                                                    #If the device is new: defaultdict(Counter) creates a new Counter() for that device, so device_errors[device] is safe.
                                                    #If the error_type is new: Counter treats missing keys as 0, so [error_type] is safe.
                                                    #Then += 1 adds 1 to the current count.
    return {device: dict(counter) for device, counter in device_errors.items()}     
        #device_errors.items() yields (device, counter) pairs, e.g. ("r1", Counter({'timeout': 2})).
        #dict(counter) converts each Counter to a normal dict, e.g. {'timeout': 2}.
        #The dict comprehension builds {device: dict(counter)}, e.g. {'r1': {'timeout': 2}, 'r2': {'connection': 1}}.


# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DATA STRUCTURES EXERCISES (ANSWER KEY)")
    print("=" * 70)

    # Test Exercise 1
    print("\nExercise 1: defaultdict")
    interfaces = [
        {"name": "Eth0", "status": "up"},
        {"name": "Eth1", "status": "down"},
        {"name": "Eth2", "status": "up"},
    ]
    result = group_interfaces_by_status(interfaces)
    print(result)
    # Expected: {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}

    # Test Exercise 2
    print("\nExercise 2: namedtuple")
    DeviceFacts = create_device_facts_tuple()
    facts = DeviceFacts("router1", "cisco", "ASR1000", "15.1")
    print(facts.hostname)
    print(facts.vendor)

    # Test Exercise 3
    print("\nExercise 3: Counter")
    result = count_interface_statuses(interfaces)
    print(result)
    # Expected: {'up': 2, 'down': 1}

    # Test Exercise 4
    print("\nExercise 4: deque")
    buffer = create_telemetry_buffer(max_size=3)
    add_to_buffer(buffer, "metric1")
    add_to_buffer(buffer, "metric2")
    add_to_buffer(buffer, "metric3")
    add_to_buffer(buffer, "metric4")
    print(list(buffer))
    # Expected: ['metric2', 'metric3', 'metric4']

    # Test Exercise 5
    print("\nExercise 5: OrderedDict")
    config = create_config_order()
    config["step1"] = "configure interface"
    config["step2"] = "configure routing"
    print(list(config.keys()))
    # Expected: ['step1', 'step2']

    # Test Exercise 6
    print("\nExercise 6: copy vs deepcopy")
    original = {"device": "r1", "config": {"interface": "Eth0"}}
    shallow = duplicate_config_shallow(original)
    deep = duplicate_config_deep(original)
    shallow["config"]["interface"] = "Eth1"
    print(original["config"]["interface"])
    deep["config"]["interface"] = "Eth2"
    print(original["config"]["interface"])

    # Test Exercise 7
    print("\nExercise 7: Combining Collections")
    logs = [
        {"device": "r1", "error_type": "timeout"},
        {"device": "r1", "error_type": "timeout"},
        {"device": "r2", "error_type": "connection"},
    ]
    result = count_errors_by_device(logs)
    print(result)
    # Expected: {'r1': {'timeout': 2}, 'r2': {'connection': 1}}
