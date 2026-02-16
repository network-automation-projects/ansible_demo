"""
Python Network Automation - Writing Classes (Practice)
======================================================

Fill-in-the-blank exercises for learning how to write classes
in the context of network automation. Builds from __init__ and
attributes to instance methods and __str__.

Prerequisites: Module 01 (Core Fundamentals), basic dict/list.
Leads into: 02b Objects and Dunders (__repr__, __eq__, etc.).
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

    # TODO: Define __init__(self, hostname: str, ip: str, vendor: str = "unknown").
    #       Store hostname, ip, and vendor as self.hostname, self.ip, self.vendor.

    def __init__(self, hostname: str, ip: str, vendor: str = "unknown") -> None:
        self.hostname = hostname
        self.ip = ip
        self.vendor = vendor

    # Example (after you implement):
    #   r1 = Device("router1", "10.0.0.1", "cisco")
    #   r1.hostname  -> "router1"
    #   r1.ip        -> "10.0.0.1"
    #   r1.vendor    -> "cisco"


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

    def summary(self) -> str:
        return f"{self.hostname} ({self.ip})"
"""


class DeviceWithSummary(Device):
    """
    A Device that can return a one-line summary string.

    (Inherits hostname, ip, vendor from Device. We add one method.)
    """

    # TODO: Implement summary(self) -> str that returns a string like:
    #       "router1 (10.0.0.1) [cisco]"

    def summary(self) -> str:
        return f"{self.hostname} {(self.ip)} [{self.vendor}]"  # return a string using self.hostname, self.ip, self.vendor

    # Example:
    #   r1 = DeviceWithSummary("router1", "10.0.0.1", "cisco")
    #   r1.summary()  -> "router1 (10.0.0.1) [cisco]"


# ============================================================================
# EXERCISE 3: Class that holds a collection
# ============================================================================

"""
Tutorial: Classes that manage state
-----------------------------------

A class can hold a list or dict and provide methods to add, look up, or list
items. In __init__, initialize the collection (e.g. self._devices = {}).
Use a leading underscore (_devices) to suggest "internal" to the instance.
"""


class DeviceInventory:
    """
    Holds a collection of Device objects, keyed by hostname.

    - add(device): add a Device; use device.hostname as the key.
    - get(hostname): return the Device with that hostname or None.
    - all_hostnames(): return a list of all hostnames (any order).
    """

    # TODO: In __init__(self), set self._devices to an empty dict.
    def __init__(self) -> None:
        self._devices: Dict[str, Device] = {}

    # TODO: Implement add(self, device: Device) -> None.
    #       Store device in self._devices under device.hostname.
    def add(self, device: Device) -> None:
        self._devices[device.hostname] = device

    # TODO: Implement get(self, hostname: str) -> Optional[Device].
    #       Return the device with that hostname
    def get(self, hostname: str) -> Optional[Device]:
        return self._devices.get(hostname)

    # TODO: Implement all_hostnames(self) -> List[str].
    #       return the hostnames (the keys of the dict), not the Device objects. 
    def all_hostnames(self) -> List[str]:
        return [i for i,v in self._devices.items()]


        #return list(self._devices.keys())

    # Example:
    #   inv = DeviceInventory()
    #   inv.add(Device("r1", "10.0.0.1"))
    #   inv.add(Device("r2", "10.0.0.2"))
    #   inv.get("r1").ip  -> "10.0.0.1"
    #   inv.all_hostnames()  -> ["r1", "r2"] (or ["r2", "r1"])


# ============================================================================
# EXERCISE 4: __str__ for human-readable print
# ============================================================================

"""
Tutorial: __str__(self)
----------------------

If you define __str__(self) -> str, Python calls it when you print(obj) or
str(obj). Use it to return a short, human-readable description.

    def __str__(self) -> str:
        return f"Device(hostname={self.hostname}, ip={self.ip})"
"""


class DevicePrintable(Device):
    """
    A Device that prints nicely: print(device) shows a readable line.
    """

    # TODO: Implement __str__(self) -> str.
    #       Return a string like: "Device(router1, 10.0.0.1, cisco)"
    def __str__(self) -> str:
        return f"Device({self.hostname},{self.ip}, {self.vendor})"

    # Example:
    #   r1 = DevicePrintable("router1", "10.0.0.1", "cisco")
    #   print(r1)  -> Device(router1, 10.0.0.1, cisco)


# ============================================================================
# EXERCISE 5: Class from scratch (no inheritance)
# ============================================================================

"""
Tutorial: Writing a small class from scratch
--------------------------------------------

Combine __init__, attributes, and a method. Good practice for interviews
and real code.
"""


class Interface:
    """
    Represents a network interface (e.g. GigabitEthernet0/1).

    Attributes:
        name: Interface name (e.g. "GigabitEthernet0/1")
        status: "up" or "down"
        description: Optional description string (default "")

    Method:
        is_up() -> bool: True if status == "up".
    """

    # TODO: __init__(self, name: str, status: str = "down", description: str = "")
    def __init__(
        self,
        name: str,
        status: str = "down",
        description: str = "",
    ) -> None:
        self.name = name
        self.status = status
        self.description = description

    # TODO: is_up(self) -> bool: return self.status == "up"
    def is_up(self) -> bool:
        return self.status == "up"

    # Example:
    #   iface = Interface("GigabitEthernet0/1", "up", "WAN link")
    #   iface.name  -> "GigabitEthernet0/1"
    #   iface.is_up()  -> True


# ============================================================================
# Run tests (uncomment after implementing)
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    # r1 = Device("router1", "10.0.0.1", "cisco")
    # print(r1.hostname, r1.ip, r1.vendor)

    # Exercise 2
    # r2 = DeviceWithSummary("router2", "10.0.0.2", "juniper")
    # print(r2.summary())

    # Exercise 3
    # inv = DeviceInventory()
    # inv.add(Device("r1", "10.0.0.1"))
    # inv.add(Device("r2", "10.0.0.2"))
    # print(inv.get("r1").ip)
    # print(inv.all_hostnames())

    # Exercise 4
    # r3 = DevicePrintable("router3", "10.0.0.3", "arista")
    # print(r3)

    # Exercise 5
    # iface = Interface("Gi0/1", "up", "to core")
    # print(iface.name, iface.is_up())

    print("Uncomment the test blocks above to verify your solutions.")
