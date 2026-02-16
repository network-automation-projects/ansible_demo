"""
Python Network Automation - Class Scenario Exercise 2: Inheritance (ANSWER KEY)
===============================================================================

TASK (same as class_scenario_exercise_2_inheritance.py)
--------------------------------------------------------
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

Use this file to verify your solution or as a reference.
"""


class Device:
    """
    Base class for a network device (router, switch, etc.).

    Attributes:
        hostname: Device hostname (e.g. "switch1")
        ip: Management IP address (e.g. "192.168.1.1")
        vendor: Vendor name (e.g. "cisco"), optional
    """

    def __init__(self, hostname: str, ip: str, vendor: str = "unknown") -> None:
        self.hostname = hostname
        self.ip = ip
        self.vendor = vendor

    def summary(self) -> str:
        return f"{self.hostname} ({self.ip}) [{self.vendor}]"


class Router(Device):
    """
    A Router is a Device with model and version.

    Inherits hostname, ip, and vendor from Device.
    Adds model (e.g. "ASR1000") and version (e.g. "15.1").
    """

    def __init__(
        self,
        hostname: str,
        ip: str,
        vendor: str = "unknown",
        model: str = "unknown",
        version: str = "unknown",
    ) -> None:
        super().__init__(hostname, ip, vendor)
        self.model = model
        self.version = version

    def summary(self) -> str:
        return (
            f"{self.hostname} ({self.ip}) [{self.vendor}] "
            f"model={self.model} version={self.version}"
        )


if __name__ == "__main__":
    dev = Device("switch1", "192.168.1.1", "cisco")
    rtr = Router("router1", "10.0.0.1", "cisco", "ASR1000", "15.1")
    print(dev.summary())
    print(rtr.summary())
