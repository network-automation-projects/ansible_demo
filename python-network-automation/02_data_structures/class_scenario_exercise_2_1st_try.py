"""
Python Network Automation - Class Scenario Exercise 2: Inheritance
==================================================================

TASK
----
Implement a base Device class and a Router(Device) subclass. The subclass
adds model and version, and overrides summary() to include them.

Concepts: inheritance (Router inherits from Device), super().__init__() to
call the base constructor, and method override (Router.summary() replaces
Device.summary() for Router instances).

- Device (base class):
  - __init__(self, hostname: str, ip: str, vendor: str = "unknown")
  - summary(self) -> str returning "hostname (ip) [vendor]"
    e.g. "switch1 (192.168.1.1) [cisco]"

- Router(Device):
  - __init__(self, hostname, ip, vendor="unknown", model="unknown", version="unknown")
    Call super().__init__(hostname, ip, vendor), then set self.model and self.version.
  - Override summary(self) -> str to add model and version at the end:
    "hostname (ip) [vendor] model=... version=..."
    e.g. "router1 (10.0.0.1) [cisco] model=ASR1000 version=15.1"

Logical inputs to use in your main block:
  - Device("switch1", "192.168.1.1", "cisco")
  - Router("router1", "10.0.0.1", "cisco", "ASR1000", "15.1")

When you run the script (after implementing the classes), you should see:

  switch1 (192.168.1.1) [cisco]
  router1 (10.0.0.1) [cisco] model=ASR1000 version=15.1

Prerequisites: class_scenario_exercise (VLAN), or Module 02 exercises_classes.
"""


class Device:
    """
    Base class for a network device (router, switch, etc.).

    Attributes:
        hostname: Device hostname (e.g. "switch1")
        ip: Management IP address (e.g. "192.168.1.1")
        vendor: Vendor name (e.g. "cisco"), optional
    """

    # TODO: Implement __init__(self, hostname: str, ip: str, vendor: str = "unknown").
    #       Store hostname, ip, and vendor as instance attributes.

    def __init__(self, hostname: str, ip: str, vendor: str = "unknown") -> None:
        self._hostname = hostname
        self._ip = ip
        self._vendor = vendor

    # TODO: Implement summary(self) -> str.
    #       Return "hostname (ip) [vendor]", e.g. "switch1 (192.168.1.1) [cisco]"

    def summary(self) -> str:
        return f"{self._hostname} ({self._ip}) [{self._vendor}]"



class Router(Device):
    """
    A Router is a Device with model and version.

    Inherits hostname, ip, and vendor from Device.
    Adds model (e.g. "ASR1000") and version (e.g. "15.1").
    """

    # TODO: Implement __init__ with hostname, ip, vendor="unknown", model="unknown", version="unknown".
    #       Call super().__init__(hostname, ip, vendor), then set self.model and self.version.

    def __init__(
        self,
        hostname: str,
        ip: str,
        vendor: str = "unknown",
        model: str = "unknown",
        version: str = "unknown",
    ) -> None:
        super().__init__(hostname, ip, vendor)  # replace: super().__init__(...), then self.model, self.version
        self._model = model
        self._version = version

    # TODO: Override summary(self) -> str to include model and version.
    #       Return "hostname (ip) [vendor] model=... version=..."

    def summary(self) -> str:
        return f"{self._hostname} ({self._ip}) [{self._vendor}] model={self._model} version={self._version}"  # replace with your implementation


if __name__ == "__main__":
    # Create one Device and one Router using the logical inputs above,
    # then print each with print(obj.summary()).

    dev = Device("switch1", "192.168.1.1", "cisco")
    rtr = Router("router1", "10.0.0.1", "cisco", "ASR1000", "15.1")
    print(dev.summary())
    print(rtr.summary())

    # Expected output when you run this (after implementing Device and Router):
    #   switch1 (192.168.1.1) [cisco]
    #   router1 (10.0.0.1) [cisco] model=ASR1000 version=15.1
    pass
