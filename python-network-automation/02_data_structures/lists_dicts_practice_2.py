"""
Python Network Automation - Lists & Dictionaries Practice
==========================================================

Progressive practice from basics to advanced. Complete the TODO sections
to build fluency with lists and dicts for network automation roles.

Prerequisites: Module 01 (Core Fundamentals).
Use alongside: exercises.py (advanced collections).
"""

from hmac import new
from mimetypes import init
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# PART 1: LIST BASICS
# =============================================================================

# -----------------------------------------------------------------------------
# 1.1 Create and index lists
# -----------------------------------------------------------------------------


def make_device_list() -> List[str]:
    """
    Return a list of three device hostnames (strings).

    Returns:
        List of device names, e.g. ['router1', 'router2', 'router3']

    Example:
        >>> make_device_list()
        ['router1', 'router2', 'router3']
    """
    # TODO: return a list literal with 3 device hostnames
    return ["router1", "router2", "router3"]  # replace with your list


def first_and_last_devices(devices: List[str]) -> Tuple[str, str]:
    """
    Return the first and last device from a non-empty list.
    Use indexing: [0] for first, [-1] for last.

    Args:
        devices: List of device hostnames

    Returns:
        (first_device, last_device)

    Example:
        >>> first_and_last_devices(['r1', 'r2', 'r3'])
        ('r1', 'r3')
    """
    # TODO: 
    first = devices[0]
    last = devices[-1]

    return (first,last) # replace


def first_n_devices(devices: List[str], n: int) -> List[str]:
    """
    Return the first n devices using slicing.
    Slicing: 

    Example:
        >>> first_n_devices(['r1', 'r2', 'r3', 'r4'], 2)
        ['r1', 'r2']
    """
    # TODO: return slice of devices for first n items

    return devices[0:n]  # replace


def last_n_devices(devices: List[str], n: int) -> List[str]:
    """
    Return the last n devices using slicing.
    Hint: 

    Example:
        >>> last_n_devices(['r1', 'r2', 'r3', 'r4'], 2)
        ['r3', 'r4']
    """
    # TODO: return slice for last n items
    return devices[-n:]  # replace


# -----------------------------------------------------------------------------
# 1.2 List methods: append, extend, in, not in
# -----------------------------------------------------------------------------


def build_interface_list(initial: List[str], to_add: List[str]) -> List[str]:
    """
    Start with initial list, then add all items from to_add using .extend().
    Do not use + or list concatenation; use the .extend() method.

    Example:
        >>> build_interface_list(['Eth0'], ['Eth1', 'Eth2'])
        ['Eth0', 'Eth1', 'Eth2']
    """
    # TODO:
    newlist = list(initial)
    newlist.extend(to_add) 
    return newlist


def add_interface_if_new(interfaces: List[str], name: str) -> None:
    """
    If name is not already in interfaces, append it. Modify the list in place.
    Use:

    Args:
        interfaces: List to modify (may already contain name)
        name: Interface name to add if not present
    """
    # TODO:
    if name not in interfaces:
        interfaces.append(name)
     
    


def device_in_scope(hostname: str, allowed: List[str]) -> bool:
    """
    Return True if hostname is in the allowed list, else False.
    Use: hostname in allowed

    Example:
        >>> device_in_scope('r1', ['r1', 'r2', 'r3'])
        True
        >>> device_in_scope('r9', ['r1', 'r2', 'r3'])
        False
    """
    # TODO: 
    return hostname in allowed

    


# -----------------------------------------------------------------------------
# 1.3 Lists from ranges and iteration
# -----------------------------------------------------------------------------


def port_numbers_list(start: int, end: int) -> List[int]:
    """
    Return a list of integers from start (inclusive) to end (exclusive).
    Use range(start, end) and list().

    Example:
        >>> port_numbers_list(1, 4)
        [1, 2, 3]
    """
    # TODO: 
    return list(range(start, end))  # replace


def interface_names_with_prefix(prefix: str, count: int) -> List[str]:
    """
    Return a list of interface names: prefix + number for 0..count-1.
    e.g. prefix='Eth', count=3 -> ['Eth0', 'Eth1', 'Eth2'].
    Use a for loop and .append(), or a list comprehension.

    Example:
        >>> interface_names_with_prefix('Eth', 3)
        ['Eth0', 'Eth1', 'Eth2']
    """
    return [f"{prefix}{c}" for c in range(count)]

    #or

    # result = []
    # for i in range(0, count):
    #     result.append(f"{prefix}{i}")

    # return result  # replace


# =============================================================================
# PART 2: DICTIONARY BASICS
# =============================================================================

# -----------------------------------------------------------------------------
# 2.1 Create, access, and check keys
# -----------------------------------------------------------------------------


def make_device_config() -> Dict[str, Any]:
    """
    Return a dict with keys: 'hostname', 'vendor', 'os_version'.
    Use a dict literal with string values (hostname and vendor) and a float or str for os_version.

    Example:
        >>> c = make_device_config()
        >>> c['hostname']
        'router1'
    """
    # TODO: Return a dict with keys: 'hostname', 'vendor', 'os_version'.
    # Use a dict literal with string values (hostname and vendor) and a float or str for os_version.

    return {
        'hostname': 'router1', 
        'vendor': 'unkknonwn', 
        'os_version': '111'
    }


def get_device_vendor(device: Dict[str, str], key: str = "vendor") -> str:
    """
    Return device[key] if key exists; otherwise return 'unknown'.
    Use: 

    Example:
        >>> get_device_vendor({'hostname': 'r1', 'vendor': 'cisco'})
        'cisco'
        >>> get_device_vendor({'hostname': 'r1'}, 'vendor')
        'unknown'
    """
    # TODO:  Return
    return device.get(key, "unknown")


def has_required_keys(config: Dict[str, Any], required: List[str]) -> bool:
    """
    Return True if config contains every key in required.
    Use: all(key in config for key in required).

    Example:
        >>> has_required_keys({'a': 1, 'b': 2}, ['a', 'b'])
        True
        >>> has_required_keys({'a': 1}, ['a', 'b'])
        False
    """
    #***
    # TODO: return
    return all(key in config for key in required)


# -----------------------------------------------------------------------------
# 2.2 Dict iteration: keys, values, items
# -----------------------------------------------------------------------------


def all_device_hostnames(devices: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    devices maps hostname -> device info dict. Return sorted list of hostnames.
    Use: 

    Example:
        >>> all_device_hostnames({'r2': {}, 'r1': {}})
        ['r1', 'r2']
    """
    #***

    # TODO: Return sorted list of hostnames. 
    return sorted(devices["hostname"])


def config_key_value_pairs(config: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Return list of (key, value) tuples for config, in sorted key order.
    Use: sorted()

    Example:
        >>> config_key_value_pairs({'b': '2', 'a': '1'})
        [('a', '1'), ('b', '2')]
    """
    # TODO:  
    return sorted(config.items())


def set_default_version(device: Dict[str, str], version: str = "1.0") -> None:
    """
    If device does not have key 'version', set device['version'] = version.
    Modify device in place. Use: device.setdefault()

    Args:
        device: Dict to possibly update
        version: Default version if 'version' missing
    """
    # TODO:   If device does not have key 'version', set device['version'] = version.

    device.setdefault(version)


# -----------------------------------------------------------------------------
# 2.3 Build dict from lists (zip)
# -----------------------------------------------------------------------------


def devices_to_ips(hostnames: List[str], ips: List[str]) -> Dict[str, str]:
    """
    Build a dict mapping each hostname to the IP at the same index.
    Assume both lists have the same length. Use zip(hostnames, ips) and dict().

    Example:
        >>> devices_to_ips(['r1', 'r2'], ['10.0.0.1', '10.0.0.2'])
        {'r1': '10.0.0.1', 'r2': '10.0.0.2'}
    """
    # TODO:   Build a dict mapping each hostname to the IP at the same index.
    
    return dict(zip(hostnames, ips ))


# =============================================================================
# PART 3: INTERMEDIATE — Lists and dicts together
# =============================================================================


def list_of_device_dicts() -> List[Dict[str, Any]]:
    """
    Return a list of two device dicts. Each dict has 'hostname' and 'vendor'.
    Use a list literal containing two dict literals.

    Example:
        >>> list_of_device_dicts()
        [{'hostname': 'r1', 'vendor': 'cisco'}, {'hostname': 'r2', 'vendor': 'juniper'}]
    """
    # TODO: Return a list of two device dicts. Each dict has 'hostname' and 'vendor'.
    
    return [{'hostname': 'r1', 'vendor': 'cisco'}, {'hostname': 'r2', 'vendor': 'juniper'}]


def hostnames_from_devices(devices: List[Dict[str, Any]]) -> List[str]:
    """
    Extract 'hostname' from each device dict. Use a list comprehension.

    Example:
        >>> hostnames_from_devices([{'hostname': 'r1'}, {'hostname': 'r2'}])
        ['r1', 'r2']
    """
    # TODO: Extract 'hostname' from each device dict. Use a list comprehension.

    
    return [d["hostname"] for d in devices]


def interfaces_up_only(interfaces: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Return only interfaces where 'status' == 'up'. Use a list comprehension.

    Example:
        >>> interfaces_up_only([{'name': 'Eth0', 'status': 'up'}, {'name': 'Eth1', 'status': 'down'}])
        [{'name': 'Eth0', 'status': 'up'}]
    """
    # TODO: Return only interfaces where 'status' == 'up'. Use a list comprehension.


    return [i for i in interfaces if i.get('status') == 'up']


def dict_comprehension_lower_keys(config: Dict[str, str]) -> Dict[str, str]:
    """
    Return a new dict with the same values but keys lowercased.
    

    Example:
        >>> dict_comprehension_lower_keys({'Hostname': 'r1', 'Vendor': 'cisco'})
        {'hostname': 'r1', 'vendor': 'cisco'}
    """
    # TODO:  Return a new dict with the same values but keys lowercased.
    
    return {k.lower(): v for k,v in config.items()}


def merge_two_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dict: all keys from base, then override overwrites for same keys.
    Use: {**base, **override} or base.copy() then .update(override).

    Example:
        >>> merge_two_configs({'a': 1, 'b': 2}, {'b': 20, 'c': 3})
        {'a': 1, 'b': 20, 'c': 3}
    """
    # TODO:  Return a new dict: all keys from base, then override overwrites for same keys.
    
    return {**base, **override}


# =============================================================================
# PART 4: ADVANCED — Nested structures and automation patterns
# =============================================================================


def nested_device_interfaces() -> Dict[str, Dict[str, Any]]:
    """
    Return a nested dict: device hostname -> dict with key 'interfaces'
    mapping to a list of interface names. Example: {'r1': {'interfaces': ['Eth0', 'Eth1']}}.

    Example:
        >>> nested_device_interfaces()
        {'r1': {'interfaces': ['Eth0', 'Eth1']}}
    """
    # TODO:  Return a nested dict: device hostname -> dict with key 'interfaces'
    # mapping to a list of interface names. Example: {'r1': {'interfaces': ['Eth0', 'Eth1']}}.

    return {
        
        "hostname" : "r1",
        "interfaces" : ['Eth1', 'Eth2'] 
        
    }


def safe_nested_get(data: Dict[str, Any], *keys: str) -> Any:
    """
    Safely get a value from nested dict using a sequence of keys.
    Return None if any level is missing. Use a loop and .get().

    Example:
        >>> safe_nested_get({'a': {'b': {'c': 1}}}, 'a', 'b', 'c')
        1
        >>> safe_nested_get({'a': {}}, 'a', 'b', 'c')
        None
    """
    # TODO:     Safely get a value from nested dict using a sequence of keys.
    # Return None if any level is missing. Use a loop and .get().

    current = data
    for key in keys:
        if not isinstance(c, dict):
            return None
        current = current.get(key)
    return current # replace


def flatten_interface_list(devices: List[Dict[str, Any]], key: str = "interfaces") -> List[str]:
    """
    Each device dict has a key (default 'interfaces') whose value is a list of strings.
    Return one flat list of all those strings. Use nested loops or a list comprehension.

    Example:
        >>> flatten_interface_list([{'interfaces': ['Eth0']}, {'interfaces': ['Eth1', 'Eth2']}])
        ['Eth0', 'Eth1', 'Eth2']
    """
    # TODO: Each device dict has a key (default 'interfaces') whose value is a list of strings.
    # Return one flat list of all those strings. Use nested loops or a list comprehension.

    # flatlist = []
    # for d in devices:
    #     for i in d[key]:
    #         flatlist.append(i)    

    # return flatlist

    return (lambda d: d[key] for d in devices)

    return (iface for d in devices for iface in d.get(key, []))



def sort_devices_by_key(devices: List[Dict[str, Any]], sort_key: str) -> List[Dict[str, Any]]:
    """
    Return a new list of device dicts sorted by sort_key (ascending).
    Use: 

    Example:
        >>> sort_devices_by_key([{'hostname': 'r2'}, {'hostname': 'r1'}], 'hostname')
        [{'hostname': 'r1'}, {'hostname': 'r2'}]
    """
    # TODO: Return a new list of device dicts sorted by sort_key (ascending).

    return sorted(devices, key=lambda d: d.get(sort_key,''))


def group_interfaces_by_status_manual(interfaces: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Group interface names by their 'status'. Build the dict manually (no defaultdict):
    

    Example:
        >>> group_interfaces_by_status_manual([
        ...     {'name': 'Eth0', 'status': 'up'},
        ...     {'name': 'Eth1', 'status': 'down'},
        ...     {'name': 'Eth2', 'status': 'up'}
        ... ])
        {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}
    """
    # TODO:  Group interface names by their 'status'. 
    # Build the dict manually (no defaultdict):
  
    newdict = {}
    for i in interfaces:
        name = i["name"]
        status = i["status"]
        newdict.setdefault(status, []).append(name)
    
    return newdict # replace


def merge_list_of_configs(configs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge a list of config dicts into one. Later dicts override earlier for same keys.
    Use a loop

    Example:
        >>> merge_list_of_configs([{'a': 1}, {'b': 2}, {'a': 10}])
        {'a': 10, 'b': 2}
    """
    # TODO: Merge a list of config dicts into one. Later dicts override earlier for same keys.
    
    newdict = {}
    for c in configs:
        newdict.update(c)
    
    return newdict


def invert_mapping(device_to_ip: Dict[str, str]) -> Dict[str, str]:
    """
    Return a new dict mapping IP -> hostname (inverse of device_to_ip).
    Assume values are unique. 

    Example:
        >>> invert_mapping({'r1': '10.0.0.1', 'r2': '10.0.0.2'})
        {'10.0.0.1': 'r1', '10.0.0.2': 'r2'}
    """
    # TODO:     Return a new dict mapping IP -> hostname (inverse of device_to_ip).


   
    return {v : k for k,v in device_to_ip.items()}


# =============================================================================
# Tests (uncomment to run)
# =============================================================================

if __name__ == "__main__":
    print("Lists & Dicts Practice — uncomment tests to run.\n")

    # Part 1
    assert make_device_list() == ['router1', 'router2', 'router3']
    assert first_and_last_devices(['r1', 'r2', 'r3']) == ('r1', 'r3')
    assert first_n_devices(['r1', 'r2', 'r3', 'r4'], 2) == ['r1', 'r2']
    assert last_n_devices(['r1', 'r2', 'r3', 'r4'], 2) == ['r3', 'r4']
    assert build_interface_list(['Eth0'], ['Eth1', 'Eth2']) == ['Eth0', 'Eth1', 'Eth2']
    ifaces = ['Eth0']; add_interface_if_new(ifaces, 'Eth1'); add_interface_if_new(ifaces, 'Eth0'); assert ifaces == ['Eth0', 'Eth1']
    assert device_in_scope('r1', ['r1', 'r2']) is True and device_in_scope('r9', ['r1']) is False
    assert port_numbers_list(1, 4) == [1, 2, 3]
    assert interface_names_with_prefix('Eth', 3) == ['Eth0', 'Eth1', 'Eth2']

    # Part 2
    c = make_device_config(); assert 'hostname' in c and 'vendor' in c
    assert get_device_vendor({'vendor': 'cisco'}) == 'cisco' and get_device_vendor({}) == 'unknown'
    assert has_required_keys({'a': 1, 'b': 2}, ['a', 'b']) is True and has_required_keys({'a': 1}, ['a', 'b']) is False
    assert all_device_hostnames({'r2': {}, 'r1': {}}) == ['r1', 'r2']
    assert config_key_value_pairs({'b': '2', 'a': '1'}) == [('a', '1'), ('b', '2')]
    d = {}; set_default_version(d, '2.0'); assert d == {'version': '2.0'}; set_default_version(d, '3.0'); assert d['version'] == '2.0'
    assert devices_to_ips(['r1', 'r2'], ['10.0.0.1', '10.0.0.2']) == {'r1': '10.0.0.1', 'r2': '10.0.0.2'}

    # Part 3
    assert hostnames_from_devices([{'hostname': 'r1'}, {'hostname': 'r2'}]) == ['r1', 'r2']
    assert interfaces_up_only([{'name': 'Eth0', 'status': 'up'}, {'name': 'Eth1', 'status': 'down'}]) == [{'name': 'Eth0', 'status': 'up'}]
    assert dict_comprehension_lower_keys({'Hostname': 'r1'}) == {'hostname': 'r1'}
    assert merge_two_configs({'a': 1, 'b': 2}, {'b': 20, 'c': 3}) == {'a': 1, 'b': 20, 'c': 3}

    # Part 4
    assert safe_nested_get({'a': {'b': {'c': 1}}}, 'a', 'b', 'c') == 1 and safe_nested_get({'a': {}}, 'a', 'b') is None
    assert flatten_interface_list([{'interfaces': ['Eth0']}, {'interfaces': ['Eth1', 'Eth2']}]) == ['Eth0', 'Eth1', 'Eth2']
    assert sort_devices_by_key([{'hostname': 'r2'}, {'hostname': 'r1'}], 'hostname') == [{'hostname': 'r1'}, {'hostname': 'r2'}]
    assert group_interfaces_by_status_manual([{'name': 'Eth0', 'status': 'up'}, {'name': 'Eth1', 'status': 'down'}, {'name': 'Eth2', 'status': 'up'}]) == {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}
    assert merge_list_of_configs([{'a': 1}, {'b': 2}, {'a': 10}]) == {'a': 10, 'b': 2}
    assert invert_mapping({'r1': '10.0.0.1', 'r2': '10.0.0.2'}) == {'10.0.0.1': 'r1', '10.0.0.2': 'r2'}

    print("Done.")
