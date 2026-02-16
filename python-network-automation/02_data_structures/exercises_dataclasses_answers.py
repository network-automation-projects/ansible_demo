"""
Python Network Automation - Dataclasses (ANSWER KEY)
====================================================

Same structure as exercises_dataclasses.py with all implementations filled in
and "when to use dataclass vs Pydantic" answers for Exercise 5.
"""

from dataclasses import asdict, dataclass, field, replace
from typing import List


# ============================================================================
# EXERCISE 1: Basic @dataclass
# ============================================================================

@dataclass
class Device:
    """A network device (router, switch)."""

    hostname: str
    ip: str
    vendor: str = "unknown"


# ============================================================================
# EXERCISE 2: default_factory for mutable defaults
# ============================================================================

@dataclass
class CommandResult:
    """
    Result of running a command on a device.
    output: the command output; errors: list of error messages (e.g. from parsing).
    """

    hostname: str
    output: str
    errors: List[str] = field(default_factory=list)   # means: when creating a new instance, 
                                                      # call list() to get a fresh empty list.
                                                      # keeps instances from sharing the same list


# ============================================================================
# EXERCISE 3: dataclasses.replace() for "updating" an instance
# ============================================================================

@dataclass(frozen=True) #frozen means
class Interface:
    """An interface record (immutable)."""

    name: str
    status: str  # "up" or "down"
    description: str = ""


def set_interface_up(iface: Interface) -> Interface:
    """
    Return a new Interface with status="up", keeping name and description.
    """
    return replace(iface, status="up")    #but we aren't just returning the status, we are returning
                                       # a new interface instance


# ============================================================================
# EXERCISE 4: asdict() for serialization
# ============================================================================

def device_to_dict(d: Device) -> dict:
    """
    Return the device as a plain dict (e.g. for json.dumps or logging).
    """
    return asdict(d)


# ============================================================================
# EXERCISE 5: When to use dataclass vs Pydantic (answers)
# ============================================================================

"""
Scenarios (from exercises_dataclasses.py):

  A. Internal struct holding the result of parsing "show version" (hostname,
     version string, uptime seconds). Built in your code from regex/custom parse.
  B. Device inventory loaded from a YAML file. You want to reject invalid
     hostnames or missing required fields with clear errors.
  C. A small holder for (command: str, timeout: int) passed between your own
     functions. No file or API input.
  D. API response from NetBox: you get a JSON blob and need to validate and
     access .name, .id, .device_type, etc. with good error messages.

Answers:

  A. DATACLASS — Data is built entirely inside your code from your own parser.
     No external input to validate; you just need a clean struct.

  B. PYDANTIC — External input (YAML). You need validation (required fields,
     invalid hostnames) and clear ValidationError messages.

  C. DATACLASS — Internal only; passed between your functions. No validation
     from file/API; minimal boilerplate is enough.

  D. PYDANTIC — External API response (JSON). You need validation and good
     error messages when the API returns unexpected or missing fields.
"""


# ============================================================================
# Run tests to verify solutions
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    r1 = Device("router1", "10.0.0.1", "cisco")
    assert r1.vendor == "cisco"
    r2 = Device("router2", "10.0.0.2")
    assert r2.vendor == "unknown"
    print("Exercise 1 OK:", r1, r2.vendor)

    # Exercise 2
    r = CommandResult("r1", "show version...")
    r.errors.append("parse warning")
    assert r.errors == ["parse warning"]
    r2 = CommandResult("r2", "show run")
    assert r2.errors == []  # new list, not shared with r
    print("Exercise 2 OK: errors =", r.errors, "r2.errors =", r2.errors)

    # Exercise 3
    iface = Interface("Gi0/1", "down", "WAN")
    up = set_interface_up(iface)
    assert up.status == "up"
    assert up.name == "Gi0/1"
    assert iface.status == "down"  # original unchanged
    print("Exercise 3 OK: set_interface_up ->", up)

    # Exercise 4
    d = device_to_dict(Device("r1", "10.0.0.1", "cisco"))
    assert d == {"hostname": "r1", "ip": "10.0.0.1", "vendor": "cisco"}
    print("Exercise 4 OK: device_to_dict ->", d)

    print("\nAll dataclasses exercises passed.")
