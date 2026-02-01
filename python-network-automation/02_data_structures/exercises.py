"""
Python Network Automation - Data Structures Exercises
=====================================================

Fill-in-the-blank exercises for learning advanced Python collections
in the context of network automation.
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
    # TODO: Fill in the blank - use defaultdict(list) to group interfaces
    grouped = None  # Create defaultdict with list factory
    for interface in interfaces:
        # TODO: Append interface name to the list for its status
        # No need to check if key exists - defaultdict handles it!
        None  # Fill in: append interface['name'] to grouped[interface['status']]
    return dict(grouped)  # Convert to regular dict for return


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
    # TODO: Fill in the blank - use namedtuple to create DeviceFacts
    # Fields: hostname, vendor, model, version
    DeviceFacts = None  # Create namedtuple with 4 fields
    return DeviceFacts


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
    # TODO: Fill in the blank - use Counter to count statuses
    # Extract statuses from interfaces, then pass to Counter
    statuses = None  # Extract status values from interfaces
    return dict(None)  # Create Counter from statuses and convert to dict


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
    # TODO: Fill in the blank - create deque with maxlen parameter
    return None  # Create deque with maxlen=max_size


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
    # TODO: Fill in the blank - use append() method
    None  # Append value to buffer


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
    # TODO: Fill in the blank - create OrderedDict
    return None  # Create OrderedDict


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
    # TODO: Fill in the blank - use copy.copy()
    return None  # Create shallow copy


def duplicate_config_deep(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a deep copy of configuration dictionary.
    
    Args:
        config: Configuration dictionary (may have nested structures)
        
    Returns:
        Deep copy of config (all nested structures copied)
    """
    # TODO: Fill in the blank - use copy.deepcopy()
    return None  # Create deep copy


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
    # TODO: Fill in the blank - use defaultdict(Counter) for grouped counting
    device_errors = None  # Create defaultdict with Counter factory
    
    for log in logs:
        device = log['device']
        error_type = log['error_type']
        # TODO: Increment counter for this device and error type
        None  # Increment device_errors[device][error_type]
    
    # Convert to regular dict with Counter values converted to dict
    return {device: dict(counter) for device, counter in device_errors.items()}


# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DATA STRUCTURES EXERCISES")
    print("=" * 70)
    
    # Test Exercise 1
    # print("\nExercise 1: defaultdict")
    # interfaces = [
    #     {'name': 'Eth0', 'status': 'up'},
    #     {'name': 'Eth1', 'status': 'down'},
    #     {'name': 'Eth2', 'status': 'up'}
    # ]
    # result = group_interfaces_by_status(interfaces)
    # print(result)
    # Expected: {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}
    
    # Test Exercise 2
    # print("\nExercise 2: namedtuple")
    # DeviceFacts = create_device_facts_tuple()
    # facts = DeviceFacts('router1', 'cisco', 'ASR1000', '15.1')
    # print(facts.hostname)  # Should be 'router1'
    # print(facts.vendor)  # Should be 'cisco'
    
    # Test Exercise 3
    # print("\nExercise 3: Counter")
    # interfaces = [
    #     {'name': 'Eth0', 'status': 'up'},
    #     {'name': 'Eth1', 'status': 'down'},
    #     {'name': 'Eth2', 'status': 'up'}
    # ]
    # result = count_interface_statuses(interfaces)
    # print(result)
    # Expected: {'up': 2, 'down': 1}
    
    # Test Exercise 4
    # print("\nExercise 4: deque")
    # buffer = create_telemetry_buffer(max_size=3)
    # add_to_buffer(buffer, 'metric1')
    # add_to_buffer(buffer, 'metric2')
    # add_to_buffer(buffer, 'metric3')
    # add_to_buffer(buffer, 'metric4')  # metric1 should be removed
    # print(list(buffer))
    # Expected: ['metric2', 'metric3', 'metric4']
    
    # Test Exercise 5
    # print("\nExercise 5: OrderedDict")
    # config = create_config_order()
    # config['step1'] = 'configure interface'
    # config['step2'] = 'configure routing'
    # print(list(config.keys()))
    # Expected: ['step1', 'step2']
    
    # Test Exercise 6
    # print("\nExercise 6: copy vs deepcopy")
    # original = {'device': 'r1', 'config': {'interface': 'Eth0'}}
    # shallow = duplicate_config_shallow(original)
    # deep = duplicate_config_deep(original)
    # shallow['config']['interface'] = 'Eth1'
    # print(original['config']['interface'])  # Changed! (shallow copy)
    # deep['config']['interface'] = 'Eth2'
    # print(original['config']['interface'])  # Still 'Eth1' (deep copy)
    
    # Test Exercise 7
    # print("\nExercise 7: Combining Collections")
    # logs = [
    #     {'device': 'r1', 'error_type': 'timeout'},
    #     {'device': 'r1', 'error_type': 'timeout'},
    #     {'device': 'r2', 'error_type': 'connection'}
    # ]
    # result = count_errors_by_device(logs)
    # print(result)
    # Expected: {'r1': {'timeout': 2}, 'r2': {'connection': 1}}
    
    print("\nUncomment test cases above to verify your solutions!")
