"""
Python Network Automation - Class Scenario Exercise
====================================================

TASK
----
Define a VLAN class and use it in a short script.

- Implement a class VLAN with:
  - __init__(self, vlan_id: int, name: str, status: str) that stores vlan_id,
    name, and status as instance attributes.
  - summary(self) -> str that returns a single line in this form:
    "VLAN <id>: <name> (<status>)"
    e.g. "VLAN 10: users (active)"

Logical inputs to use in your main block:
  - VLAN 1,  name "default", status "active"
  - VLAN 10, name "users",   status "active"
  - VLAN 20, name "servers", status "suspend"

When you run the script (after implementing the class), you should see:

  VLAN 1: default (active)
  VLAN 10: users (active)
  VLAN 20: servers (suspend)

Prerequisites: Module 01 (Core Fundamentals), basic classes (Module 02 exercises_classes).
"""


class VLAN:
    """
    Represents a VLAN (id, name, status) for network automation.

    Attributes:
        vlan_id: VLAN number (e.g. 1, 10, 20)
        name: VLAN name (e.g. "default", "users")
        status: Status string (e.g. "active", "suspend")
    """

    # TODO: Implement __init__(self, vlan_id: int, name: str, status: str).
    #       Store vlan_id, name, and status as self.vlan_id, self.name, self.status.

    def __init__(self, vlan_id: int, name: str, status: str) -> None:
        pass  # replace with your implementation

    # TODO: Implement summary(self) -> str.
    #       Return a string like "VLAN 10: users (active)" using the instance attributes.

    def summary(self) -> str:
        return ""  # replace with your implementation


if __name__ == "__main__":
    # Build three VLAN instances using the logical inputs above, then print each
    # with print(vlan.summary()).

    # v1 = VLAN(1, "default", "active")
    # v10 = VLAN(10, "users", "active")
    # v20 = VLAN(20, "servers", "suspend")
    # for v in [v1, v10, v20]:
    #     print(v.summary())

    # Expected output when you run this (after implementing VLAN):
    #   VLAN 1: default (active)
    #   VLAN 10: users (active)
    #   VLAN 20: servers (suspend)
    pass
