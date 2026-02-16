"""
Python Network Automation - Writing Classes (ANSWER KEY)
=========================================================

Same structure as exercises_classes.py with all implementations filled in.
Use this file to verify your solutions or as a reference.
"""

from typing import Dict, List, Optional


# ============================================================================
# EXERCISE 1: Simple class with __init__ and attributes
# ============================================================================

"""
Tutorial: Defining a class and __init__
---------------------------------------

A class is a blueprint for objects. __init__(self, ...) is the constructor:
Python calls it when you create an instance with MyClass(...). Use self to
store attributes on the instance.

    class Device:
        def __init__(self, hostname, ip):
            self.hostname = hostname   # attribute
            self.ip = ip

    r1 = Device("router1", "10.0.0.1")
    print(r1.hostname)  # "router1"

Parameter order: self first, then your arguments. Assign to self.attribute_name.
"""


class Device:
    """
    Represents a network device (router, switch, etc.).

    Attributes:
        hostname: Device hostname (e.g. "router1")
        ip: Management IP address (e.g. "10.0.0.1")
        vendor: Vendor name (e.g. "cisco"), optional
    """

    def __init__(self, hostname: str, ip: str, vendor: str = "unknown") -> None:
        self.hostname = hostname
        self.ip = ip
        self.vendor = vendor


# another example of creating a class
class Router(Device):
        """Represents a network router.

        Attributes:
            model: Router model (e.g. "ASR1000")
            version: Router version (e.g. "15.1")

        Inherits hostname, ip, and vendor from Device.
        """
        # TODO: Define __init__(self, hostname: str, ip: str, vendor: str = "unknown", model: str = "unknown", version: str = "unknown").

    def __init__(self, hostname: str, ip: str, vendor: str = "unknown", model: str = "unknown", version: str = "unknown") -> None:
        super().__init__(hostname, ip, vendor)
        self.model = model
        self.version = version

    #example after implementing
    #   r1 = Router("router1", "10.0.0.1", "cisco", "ASR1000", "15.1")
    #   r1.model  -> "ASR1000"
    #   r1.version  -> "15.1"


# ============================================================================
# EXERCISE 2: Instance methods
# ============================================================================

"""
Tutorial: Instance methods
--------------------------

Methods are functions defined on the class that take self as the first argument.
They can use self.hostname, self.ip, etc. Call them on an instance: obj.method().
"""


class DeviceWithSummary(Device):
    """
    A Device that can return a one-line summary string.

    (Inherits hostname, ip, vendor from Device. We add one method.)
    """

    def summary(self) -> str:
        return f"{self.hostname} ({self.ip}) [{self.vendor}]"  # the () and [] are just formatting

# ============================================================================
# EXERCISE 3: Class that holds a collection
# ============================================================================

"""
Tutorial: Classes that manage state
-----------------------------------

A class can hold a list or dict and provide methods to add, look up, or list
items. In __init__, initialize the collection (e.g. self._devices = {}).
"""


class DeviceInventory:
    """
    Holds a collection of Device objects, keyed by hostname.
    """

    def __init__(self) -> None:
        self._devices: Dict[str, Device] = {}   # Adds an attribute on this DeviceInventory instance 
                                                # (each instance gets its own dict).
                                                # Type hint: “a dict whose keys are strings 
                                                # (hostnames) and whose values are Device objects.”
                                                # Starts with an empty dict. Nothing is “incoming” yet; 
                                                # devices are added later when you call inv.add(device).
    
    def add(self, device: Device) -> None:
        self._devices[device.hostname] = device  # store Device in dict keyed by hostname 

    def get(self, hostname: str) -> Optional[Device]:
        return self._devices.get(hostname)      #hostname is a paramater. self.hostname would mean an attribute named hostname on the DeviceInventory instance (that's not what we are doing here)

    def all_hostnames(self) -> List[str]:
        return list(self._devices.keys())


# ============================================================================
# EXERCISE 4: __str__ for human-readable print
# ============================================================================

"""
Tutorial: __str__(self)
----------------------

If you define __str__(self) -> str, Python calls it when you print(obj) or
str(obj). Use it to return a short, human-readable description.
"""


class DevicePrintable(Device):
    """
    A Device that prints nicely: print(device) shows a readable line.
    """

    def __str__(self) -> str:
        return f"Device({self.hostname}, {self.ip}, {self.vendor})"


# ============================================================================
# EXERCISE 5: Class from scratch (no inheritance)
# ============================================================================

"""
Tutorial: Writing a small class from scratch
--------------------------------------------

Combine __init__, attributes, and a method.
"""


class Interface:
    """
    Represents a network interface (e.g. GigabitEthernet0/1).

    Attributes:
        name: Interface name (e.g. "GigabitEthernet0/1")
        status: "up" or "down"
        description: Optional description string (default "")
    """

    def __init__(
        self,
        name: str,
        status: str = "down",
        description: str = "",
    ) -> None:
        self.name = name                #not _name since it's part of the public API
        self.status = status
        self.description = description

    def is_up(self) -> bool:
        return self.status == "up"


# ============================================================================
# Run tests to verify solutions
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    r1 = Device("router1", "10.0.0.1", "cisco")
    assert r1.hostname == "router1"
    assert r1.ip == "10.0.0.1"
    assert r1.vendor == "cisco"
    print("Exercise 1 OK:", r1.hostname, r1.ip, r1.vendor)

    # Exercise 2
    r2 = DeviceWithSummary("router2", "10.0.0.2", "juniper")
    assert r2.summary() == "router2 (10.0.0.2) [juniper]"
    print("Exercise 2 OK:", r2.summary())

    # Exercise 3
    inv = DeviceInventory()
    inv.add(Device("r1", "10.0.0.1"))
    inv.add(Device("r2", "10.0.0.2"))
    assert inv.get("r1").ip == "10.0.0.1"
    assert set(inv.all_hostnames()) == {"r1", "r2"}
    assert inv.get("r3") is None
    print("Exercise 3 OK: get(r1).ip =", inv.get("r1").ip, ", hostnames =", inv.all_hostnames())

    # Exercise 4
    r3 = DevicePrintable("router3", "10.0.0.3", "arista")
    assert str(r3) == "Device(router3, 10.0.0.3, arista)"
    print("Exercise 4 OK: str(r3) =", str(r3))

    # Exercise 5
    iface = Interface("Gi0/1", "up", "to core")
    assert iface.name == "Gi0/1"
    assert iface.is_up() is True
    iface_down = Interface("Gi0/2", "down")
    assert iface_down.is_up() is False
    print("Exercise 5 OK:", iface.name, "is_up =", iface.is_up())

    print("\nAll class-writing exercises passed.")
