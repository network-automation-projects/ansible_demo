"""
Python Network Automation - Dataclasses (Practice)
==================================================

Fill-in-the-blank exercises for using dataclasses in network automation,
plus when to choose dataclasses vs Pydantic.

WHEN TO USE DATACLASSES VS PYDANTIC
------------------------------------

Use DATACLASSES when:
- Data is created inside your code (internal structs, function results, parsed
  objects you build yourself). No need to validate arbitrary input.
- You want minimal boilerplate: no manual __init__, automatic __repr__/__eq__.
- You're fine with mutable instances (or use frozen=True for immutable).
- No need for JSON/dict validation, error messages, or env/config loading.

Use PYDANTIC when:
- Data comes from outside: config files, APIs, env vars, user input. You need
  validation (types, ranges, required vs optional) and clear ValidationError.
- You need model_dump()/model_validate(), model_dump_json(), or BaseSettings.
- You're building APIs (e.g. FastAPI request/response models) or strict config
  schemas.

Rule of thumb: dataclasses for "internal data holders"; Pydantic for "validated
external data and config".

Prerequisites: Module 02 exercises_classes.py (or basic class/__init__).
Related: Module 12b Pydantic (validation, API/config).
"""

from dataclasses import asdict, dataclass, field, replace
from typing import List


# ============================================================================
# EXERCISE 1: Basic @dataclass
# ============================================================================

"""
Tutorial: @dataclass
-------------------

@dataclass generates __init__, __repr__, __eq__ from class attributes with
type annotations. Use field() for defaults that must not be shared (e.g. list).
"""


# TODO: Add @dataclass above the class. Add fields: hostname (str), ip (str),
#       vendor (str) with default "unknown".

@dataclass
class Device:
    """A network device (router, switch)."""

    hostname: str  # replace with: hostname: str, ip: str, vendor: str = "unknown"
    ip: str
    vendor: str = "unknown"

    # Example (after you add the decorator and fields):
    #   r1 = Device("router1", "10.0.0.1", "cisco")
    #   r1.vendor  -> "cisco"
    #   r2 = Device("router2", "10.0.0.2")   # vendor defaults to "unknown"
    #   print(r1)  -> Device(hostname='router1', ip='10.0.0.1', vendor='cisco')


# ============================================================================
# EXERCISE 2: default_factory for mutable defaults
# ============================================================================

"""
Tutorial: field(default_factory=...)
------------------------------------

Never use a mutable default as a literal: wrong: errors: List[str] = []  # shared!
Use field(default_factory=list) so each instance gets its own list.
"""


@dataclass
class CommandResult:
    """
    Result of running a command on a device.
    output: the command output; errors: list of error messages (e.g. from parsing).
    """
    # TODO: Add field 'errors' with type List[str] and default_factory=list
    #       so each instance has its own empty list, not a shared one.
    # errors: List[str] = field(default_factory=list)

    hostname: str
    output: str
    errors: List[str] = field(default_factory=list)


    # Example:
    #   r = CommandResult("r1", "show version...")
    #   r.errors.append("parse warning")
    #   r2 = CommandResult("r2", "show run")  # r2.errors is a new [], not shared with r


# ============================================================================
# EXERCISE 3: dataclasses.replace() for "updating" an instance
# ============================================================================

"""
Tutorial: replace()
-------------------

replace(instance, **changes) returns a new instance with the given fields
updated. Useful for frozen dataclasses or when you want to keep the original
unchanged.
"""


@dataclass(frozen=True)
class Interface:
    """An interface record (immutable)."""

    name: str
    status: str  # "up" or "down"
    description: str = ""


def set_interface_up(iface: Interface) -> Interface:
    """
    Return a new Interface with status="up", keeping name and description.
    """
    # TODO: return 
    return replace(iface, status = "up")


# ============================================================================
# EXERCISE 4: asdict() for serialization
# ============================================================================

"""
Tutorial: asdict()
------------------

asdict(instance) returns a dict of the dataclass fields (recursively for nested
dataclasses). Useful for JSON serialization or logging.
"""


def device_to_dict(d: Device) -> dict:
    """
    Return the device as a plain dict (e.g. for json.dumps or logging).
    Use 
    """
    # TODO: return asdict(d)
    return asdict(d)


# ============================================================================
# EXERCISE 5: When to use dataclass vs Pydantic (concept)
# ============================================================================

"""
Tutorial: Choosing the right tool
---------------------------------

See the "WHEN TO USE DATACLASSES VS PYDANTIC" block at the top of this file.
Exercise: For each scenario below, decide: dataclass or Pydantic? (Answers in
exercises_dataclasses_answers.py.)

  A. Internal struct holding the result of parsing "show version" (hostname,
     version string, uptime seconds). Built in your code from regex/custom parse.
  B. Device inventory loaded from a YAML file. You want to reject invalid
     hostnames or missing required fields with clear errors.
  C. A small holder for (command: str, timeout: int) passed between your own
     functions. No file or API input.
  D. API response from NetBox: you get a JSON blob and need to validate and
     access .name, .id, .device_type, etc. with good error messages.
"""

# Write your answers as comments (or check the answers file):
# A: Dataclasses
# B: Pydantic
# C: Dataclasses
# D: Pydantic


# ============================================================================
# Run tests (uncomment after implementing)
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    r1 = Device("router1", "10.0.0.1", "cisco")
    print(r1.vendor)

    # Exercise 2
    r = CommandResult("r1", "output")
    r.errors.append("warn")
    print(r.errors)

    # Exercise 3
    iface = Interface("Gi0/1", "down")
    up = set_interface_up(iface)
    print(up.status)  # "up"

    # Exercise 4
    d = device_to_dict(Device("r1", "10.0.0.1"))
    print(d)

    print("Uncomment the test blocks above to verify your solutions.")
