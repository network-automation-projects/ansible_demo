"""
Python Network Automation - Lists & Dictionaries Practice (ANSWERS)
====================================================================

Completed solutions for lists_dicts_practice.py.
Use this to check your work after attempting the exercises.
"""

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
    return ["router1", "router2", "router3"]


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
    return (devices[0], devices[-1])


def first_n_devices(devices: List[str], n: int) -> List[str]:
    """
    Return the first n devices using slicing.
    Slicing: devices[start:stop] or devices[:n] for "first n".

    Example:
        >>> first_n_devices(['r1', 'r2', 'r3', 'r4'], 2)
        ['r1', 'r2']
    """
    return devices[:n]   #first number is the start


def last_n_devices(devices: List[str], n: int) -> List[str]:
    """
    Return the last n devices using slicing.
    Hint: devices[-n:] gives the last n elements.

    Example:
        >>> last_n_devices(['r1', 'r2', 'r3', 'r4'], 2)
        ['r3', 'r4']
    """
    return devices[-n:]     #negative from the end


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
    # !!!

    result = list(initial)
    result.extend(to_add)
    return result               #if you .extend a list (not a copy of it), it would change the original


def add_interface_if_new(interfaces: List[str], name: str) -> None:
    """
    If name is not already in interfaces, append it. Modify the list in place.
    Use: if name not in interfaces: interfaces.append(name)

    Args:
        interfaces: List to modify (may already contain name)
        name: Interface name to add if not present
    """
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
    #!!!
    return list(range(start, end))


def interface_names_with_prefix(prefix: str, count: int) -> List[str]:
    """
    Return a list of interface names: prefix + number for 0..count-1.
    e.g. prefix='Eth', count=3 -> ['Eth0', 'Eth1', 'Eth2'].
    Use a for loop and .append(), or a list comprehension.

    Example:
        >>> interface_names_with_prefix('Eth', 3)
        ['Eth0', 'Eth1', 'Eth2']
    """
    return [f"{prefix}{i}" for i in range(count)]  # for each number in the range of count, grab the prefix and put that number after it. put all those in a list


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
    return {
        "hostname": "router1",
        "vendor": "cisco",
        "os_version": "15.1",       #that's cool, if the input is "15.1" it can be str or float
    }


def get_device_vendor(device: Dict[str, str], key: str = "vendor") -> str:
    """
    Return device[key] if key exists; otherwise return 'unknown'.
    Use: device.get(key, 'unknown').

    Example:
        >>> get_device_vendor({'hostname': 'r1', 'vendor': 'cisco'})
        'cisco'
        >>> get_device_vendor({'hostname': 'r1'}, 'vendor')
        'unknown'
    """
    #***
    return device.get(key, "unknown")           #unknown is the default value if it doens't find that key


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
    return all(key in config for key in required)   # this generator yields True for each key in required that also has a key in config. return true if all are there.



# -----------------------------------------------------------------------------
# 2.2 Dict iteration: keys, values, items
# -----------------------------------------------------------------------------


def all_device_hostnames(devices: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    devices maps hostname -> device info dict. Return sorted list of hostnames.
    Use: sorted(devices.keys()) or sorted(devices).

    Example:
        >>> all_device_hostnames({'r2': {}, 'r1': {}})
        ['r1', 'r2']
    """
        
    #***

    return sorted(devices.keys())

    # return sorted(devices)           # dicts iterate over keys by default
    # # or
    # return sorted(devices.keys())    # explicit


def config_key_value_pairs(config: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Return list of (key, value) tuples for config, in sorted key order.
    Use: sorted(config.items()).

    Example:
        >>> config_key_value_pairs({'b': '2', 'a': '1'})
        [('a', '1'), ('b', '2')]
    """
    return sorted(config.items())   #items provides the key and value pairs


def set_default_version(device: Dict[str, str], version: str = "1.0") -> None:
    """
    If device does not have key 'version', set device['version'] = version.
    Modify device in place. Use: device.setdefault('version', version).

    Args:
        device: Dict to possibly update
        version: Default version if 'version' missing
    """
    device.setdefault("version", version)   # If the key doesn’t exist: setdefault("version", version) creates device["version"] = version (and returns version).
                                            # so if key 'version' exists it will update. 
                                            # If the key already exists: nothing is changed. 
                                            # The existing value is left as-is and returned. It does not update the value.

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
    return dict(zip(hostnames, ips))


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
    return [
        {"hostname": "r1", "vendor": "cisco"},
        {"hostname": "r2", "vendor": "juniper"},    #why the comma even though it's the last one?
    ]


def hostnames_from_devices(devices: List[Dict[str, Any]]) -> List[str]:
    """
    Extract 'hostname' from each device dict. Use a list comprehension.

    Example:
        >>> hostnames_from_devices([{'hostname': 'r1'}, {'hostname': 'r2'}])
        ['r1', 'r2']
    """
    return [d["hostname"] for d in devices]


def interfaces_up_only(interfaces: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Return only interfaces where 'status' == 'up'. Use a list comprehension.

    Example:
        >>> interfaces_up_only([{'name': 'Eth0', 'status': 'up'}, {'name': 'Eth1', 'status': 'down'}])
        [{'name': 'Eth0', 'status': 'up'}]
    """
    return [i for i in interfaces if i.get("status") == "up"]   
    
    # this also works:
    # return [i for i in interfaces if i['status']=='up']  # replace



def dict_comprehension_lower_keys(config: Dict[str, str]) -> Dict[str, str]:
    """
    Return a new dict with the same values but keys lowercased.
    Use: {k.lower(): v for k, v in config.items()}.

    Example:
        >>> dict_comprehension_lower_keys({'Hostname': 'r1', 'Vendor': 'cisco'})
        {'hostname': 'r1', 'vendor': 'cisco'}
    """
    return {k.lower(): v for k, v in config.items()}    #so this means - for each item in the config dictionary,
                                                        #grab the key and value but before putting them into the new dictionary, lower the case of the key


def merge_two_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dict: all keys from base, then override overwrites for same keys.
    Use: {**base, **override} or base.copy() then .update(override).

    Example:
        >>> merge_two_configs({'a': 1, 'b': 2}, {'b': 20, 'c': 3})
        {'a': 1, 'b': 20, 'c': 3}
    """
    return {**base, **override}   # called unpacking, this creates a new dict that combines the 
                                # first dict with the second dict.  the second dict (if the same key exists) value overrides the first value
                                # later changes made to the new dict values affect the original dictionary values
                                # and later changes made to the values inside the base and override dict values would show up in the new merged dict
                                # since they are pointing to the same place in memory
                                # gotcha: One small precision: this applies to mutating the value in place (e.g. merged["a"].append(1) or base["a"].append(1)). If you reassign a key in the merged dict (e.g. merged["a"] = [99]), 
                                # you’re just making that key in merged point to a new object; base and override are unchanged. So “changes to the values” = mutating the object (append, delete, etc.), not reassigning the key.

    # or
    # merged = base.copy()
    # merged.update(override)
    # return merged
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
    return {"r1": {"interfaces": ["Eth0", "Eth1"]}}


def safe_nested_get(data: Dict[str, Any], *keys: str) -> Any:
                                                                # varargs (variable-length positional arguments).
                                                                # The * in the parameter list means: “take all extra positional arguments and collect them into one name.”
                                                                # So *keys: str means: “after data, accept zero or more positional arguments, each a str, and pack them into a tuple named keys.”
    """
    Safely get a value from nested dict using a sequence of keys.
    Return None if any level is missing. Use a loop and .get().

    Example:
        >>> safe_nested_get({'a': {'b': {'c': 1}}}, 'a', 'b', 'c')
        1
        >>> safe_nested_get({'a': {}}, 'a', 'b', 'c')
        None
    """
    current = data                          # assign data dictionary to current
    for k in keys:
        if not isinstance(current, dict):   # if 'current' is not a dict at this point, 
                                            #  then return none because we can't keep searching since it's not a dict
            return None
        current = current.get(k)            # either way, get the value for key k and put it in current variable, 
                                            # so whichever is the deepest nested value (or 'None') will be in current after all loops are complete
    return current


def flatten_interface_list(devices: List[Dict[str, Any]], key: str = "interfaces") -> List[str]:
    """
    Each device dict has a key (default 'interfaces') whose value is a list of strings.
    Return one flat list of all those strings. Use nested loops or a list comprehension.

    Example:
        >>> flatten_interface_list([{'interfaces': ['Eth0']}, {'interfaces': ['Eth1', 'Eth2']}])
        ['Eth0', 'Eth1', 'Eth2']
    """
    return [iface for d in devices for iface in d.get(key, [])]  # for each d in devices, get its interface list with the d.get(key,[]). so for each iface in that list, add the iface to the result 

    #OR

    # flatlist = []
    # for d in devices:               # for each device, 
    #     for item in d[key]:         # check each item (string) in the value list for that key
    #         flatlist.append(item)   # append the item 
    # return flatlist


def sort_devices_by_key(devices: List[Dict[str, Any]], sort_key: str) -> List[Dict[str, Any]]:
    """
    Return a new list of device dicts sorted by sort_key (ascending).
    Use: sorted(devices, key=lambda d: d.get(sort_key, '')).

    Example:
        >>> sort_devices_by_key([{'hostname': 'r2', 'vendor': 'juniper'}, {'hostname': 'r1', 'vendor': 'cisco'}, {'hostname': 'r4', 'vendor': 'juniper'}, {'hostname': 'r3', 'vendor': 'cisco'}], 'hostname')
        [
            {'hostname': 'r1', 'vendor': 'cisco'},
            {'hostname': 'r2', 'vendor': 'juniper'},
            {'hostname': 'r3', 'vendor': 'cisco'},
            {'hostname': 'r4', 'vendor': 'juniper'}
        ]
    """
    return sorted(devices, key=lambda d: d.get(sort_key, ""))   # so we read this: return the sorted list of devices 
                    # lambda d takes each device d and returns the value for that key. 
                    # OR
                    # the lamba gets the value for the sort_key for each d in devices and then the sorted function sorts the new list based on that


def group_interfaces_by_status_manual(interfaces: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Group interface names by their 'status'. Build the dict manually (no defaultdict):
    use status in result or result[status] = []; then result[status].append(name).

    Example:
        >>> group_interfaces_by_status_manual([
        ...     {'name': 'Eth0', 'status': 'up'},
        ...     {'name': 'Eth1', 'status': 'down'},
        ...     {'name': 'Eth2', 'status': 'up'}
        ... ])
        {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}
    """
    result = {}
    for i in interfaces:
        status = i["status"]
        name = i["name"]
        result.setdefault(status, []).append(name)
    return result


def merge_list_of_configs(configs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge a list of config dicts into one. Later dicts override earlier for same keys.
    Use a loop: result = {}; for c in configs: result.update(c); return result.

    Example:
        >>> merge_list_of_configs([{'a': 1}, {'b': 2}, {'a': 10}])
        {'a': 10, 'b': 2}
    """
    result = {}
    for c in configs:
        result.update(c)    # update works on dictionaries only.  Here, it takes the dictionary, c, 
                            # and merges it with the dictionary, result. (newest overriding)
    return result


def invert_mapping(device_to_ip: Dict[str, str]) -> Dict[str, str]:
    """
    Return a new dict mapping IP -> hostname (inverse of device_to_ip).
    Assume values are unique. Use: {v: k for k, v in device_to_ip.items()}.

    Example:
        >>> invert_mapping({'r1': '10.0.0.1', 'r2': '10.0.0.2'})
        {'10.0.0.1': 'r1', '10.0.0.2': 'r2'}
    """
    return {v: k for k, v in device_to_ip.items()} #this dictionary comprehension takes each item (which means the key value pair)
                                                    # in device_to_ip and creates a new dictionary 
                                                    # where the new key is the old value v (IP) and the new value is the old key k (hostname).


# =============================================================================
# Tests (run this file to verify all answers)
# =============================================================================

if __name__ == "__main__":
    print("Lists & Dicts Practice — running tests...\n")

    # Part 1
    assert make_device_list() == ["router1", "router2", "router3"]
    assert first_and_last_devices(["r1", "r2", "r3"]) == ("r1", "r3")
    assert first_n_devices(["r1", "r2", "r3", "r4"], 2) == ["r1", "r2"]
    assert last_n_devices(["r1", "r2", "r3", "r4"], 2) == ["r3", "r4"]
    assert build_interface_list(["Eth0"], ["Eth1", "Eth2"]) == ["Eth0", "Eth1", "Eth2"]
    ifaces = ["Eth0"]
    add_interface_if_new(ifaces, "Eth1")
    add_interface_if_new(ifaces, "Eth0")
    assert ifaces == ["Eth0", "Eth1"]
    assert device_in_scope("r1", ["r1", "r2"]) is True
    assert device_in_scope("r9", ["r1"]) is False
    assert port_numbers_list(1, 4) == [1, 2, 3]
    assert interface_names_with_prefix("Eth", 3) == ["Eth0", "Eth1", "Eth2"]

    # Part 2
    c = make_device_config()
    assert "hostname" in c and "vendor" in c
    assert get_device_vendor({"vendor": "cisco"}) == "cisco"
    assert get_device_vendor({}) == "unknown"
    assert has_required_keys({"a": 1, "b": 2}, ["a", "b"]) is True
    assert has_required_keys({"a": 1}, ["a", "b"]) is False
    assert all_device_hostnames({"r2": {}, "r1": {}}) == ["r1", "r2"]
    assert config_key_value_pairs({"b": "2", "a": "1"}) == [("a", "1"), ("b", "2")]
    d = {}
    set_default_version(d, "2.0")
    assert d == {"version": "2.0"}
    set_default_version(d, "3.0")
    assert d["version"] == "2.0"
    assert devices_to_ips(["r1", "r2"], ["10.0.0.1", "10.0.0.2"]) == {
        "r1": "10.0.0.1",
        "r2": "10.0.0.2",
    }

    # Part 3
    assert list_of_device_dicts() == [
        {"hostname": "r1", "vendor": "cisco"},
        {"hostname": "r2", "vendor": "juniper"},
    ]
    assert hostnames_from_devices([{"hostname": "r1"}, {"hostname": "r2"}]) == ["r1", "r2"]
    assert interfaces_up_only(
        [{"name": "Eth0", "status": "up"}, {"name": "Eth1", "status": "down"}]
    ) == [{"name": "Eth0", "status": "up"}]
    assert dict_comprehension_lower_keys({"Hostname": "r1"}) == {"hostname": "r1"}
    assert merge_two_configs({"a": 1, "b": 2}, {"b": 20, "c": 3}) == {"a": 1, "b": 20, "c": 3}

    # Part 4
    assert nested_device_interfaces() == {"r1": {"interfaces": ["Eth0", "Eth1"]}}
    assert safe_nested_get({"a": {"b": {"c": 1}}}, "a", "b", "c") == 1
    assert safe_nested_get({"a": {}}, "a", "b") is None
    assert flatten_interface_list(
        [{"interfaces": ["Eth0"]}, {"interfaces": ["Eth1", "Eth2"]}]
    ) == ["Eth0", "Eth1", "Eth2"]
    assert sort_devices_by_key(
        [{"hostname": "r2"}, {"hostname": "r1"}], "hostname"
    ) == [{"hostname": "r1"}, {"hostname": "r2"}]
    assert group_interfaces_by_status_manual([
        {"name": "Eth0", "status": "up"},
        {"name": "Eth1", "status": "down"},
        {"name": "Eth2", "status": "up"},
    ]) == {"up": ["Eth0", "Eth2"], "down": ["Eth1"]}
    assert merge_list_of_configs([{"a": 1}, {"b": 2}, {"a": 10}]) == {"a": 10, "b": 2}
    assert invert_mapping({"r1": "10.0.0.1", "r2": "10.0.0.2"}) == {
        "10.0.0.1": "r1",
        "10.0.0.2": "r2",
    }

    print("All tests passed.")
