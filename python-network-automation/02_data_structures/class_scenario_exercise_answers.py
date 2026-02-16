"""
Python Network Automation - Class Scenario Exercise (ANSWER KEY)
=================================================================

TASK (same as class_scenario_exercise.py)
-----------------------------------------
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

Use this file to verify your solution or as a reference.
"""


class VLAN:
    """
    Represents a VLAN (id, name, status) for network automation.

    Attributes:
        vlan_id: VLAN number (e.g. 1, 10, 20)
        name: VLAN name (e.g. "default", "users")
        status: Status string (e.g. "active", "suspend")
    """

    def __init__(self, vlan_id: int, name: str, status: str) -> None:
        self.vlan_id = vlan_id
        self.name = name
        self.status = status

    def summary(self) -> str:
        return f"VLAN {self.vlan_id}: {self.name} ({self.status})"


if __name__ == "__main__":
    v1 = VLAN(1, "default", "active")
    v10 = VLAN(10, "users", "active")
    v20 = VLAN(20, "servers", "suspend")
    for v in [v1, v10, v20]:
        print(v.summary())
