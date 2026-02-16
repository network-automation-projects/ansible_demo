# Module 02b: Objects and Special Methods (Dunders)

Python's data model and double-underscore methods for network automation types.

## Learning Objectives

By completing this module, you will learn:

- What "dunders" (special methods) are and when Python calls them
- How to implement `__repr__` and `__str__` for clear logging and display
- How to make your types support `len()`, indexing, and iteration
- How to implement equality (`__eq__`) and use in sets/dicts safely
- How to make instances callable (`__call__`) or usable in `with` blocks (`__enter__`/`__exit__`)

## Prerequisites

- Module 01: Core Fundamentals
- Module 02: Data Structures (helpful but not required)
- Basic familiarity with classes and `__init__`

## Concepts Covered

### What Are Dunders?

**Dunder** = "double underscore" (`__name__`). These are **special method names** that Python's data model reserves. When you use built-in operations like `len(obj)`, `str(obj)`, or `obj[key]`, Python looks for and calls the corresponding dunder on your object. They are not reserved keywords—you must use the exact names for the behavior to work.

### Construction and Representation

| Dunder | When Python calls it | Use in network automation |
|--------|----------------------|----------------------------|
| `__init__(self, ...)` | When the object is created | Set up device/connection state (hostname, credentials, etc.) |
| `__repr__(self) -> str` | `repr(obj)`, debugger, REPL | Unambiguous representation, e.g. `Device(host='r1', vendor='cisco')` |
| `__str__(self) -> str` | `str(obj)`, `print(obj)` | Human-friendly string for logs and reports |

### Container-Like Behavior

| Dunder | When Python calls it | Use in network automation |
|--------|----------------------|----------------------------|
| `__len__(self) -> int` | `len(obj)` | Number of devices, interfaces, or config lines |
| `__getitem__(self, key)` | `obj[key]` | Index device list, get interface by name |
| `__iter__(self)` | `for x in obj`, `iter(obj)` | Iterate over devices or interfaces |
| `__contains__(self, item) -> bool` | `item in obj` | Check if device or interface is in collection |

### Comparison and Hashing

| Dunder | When Python calls it | Use in network automation |
|--------|----------------------|----------------------------|
| `__eq__(self, other)` | `obj == other` | Value equality for device/interface records |
| `__hash__(self) -> int` | `hash(obj)`, sets, dict keys | Only for immutable value types; must match `__eq__` |

### Callable and Context Manager

| Dunder | When Python calls it | Use in network automation |
|--------|----------------------|----------------------------|
| `__call__(self, ...)` | `obj(...)` | Instance used as a function (e.g. retry runner) |
| `__enter__(self)`, `__exit__(self, ...)` | `with obj:` | Connection setup/teardown, config session |

### Other Useful Dunders

| Dunder | When Python calls it |
|--------|----------------------|
| `__bool__(self) -> bool` | `bool(obj)`, `if obj:` |
| `__format__(self, spec)` | `f"{obj:spec}"` |

## Use Cases in Network Automation

### Device and Interface Types

- Implement `__repr__` so logs and errors show `Device(host='r1')` instead of `<Device object at 0x...>`.
- Implement `__str__` for user-facing reports (e.g. "Router r1 (Cisco)").
- Implement `__eq__` to compare devices or interfaces by hostname/facts for deduplication.

### Collections of Devices or Config

- Implement `__len__` and `__getitem__` on a wrapper so `len(device_list)` and `device_list[0]` work.
- Implement `__iter__` so `for device in device_list` works.
- Implement `__contains__` to check `if device in inventory` by hostname.

### Connections and Sessions

- Use `__enter__` and `__exit__` for a connection or config-session context manager so `with device.connect():` handles connect/disconnect cleanly.
- Use `__call__` when an object should be invoked like a function (e.g. a runner or retry helper).

## Related Modules

- **Module 01:** Core Fundamentals (built-ins like `len()`, `repr()`, `str()`)
- **Module 02:** Data Structures (collections that implement these protocols)
- **Module 04:** Device Management (classes that benefit from good `__repr__` and context managers)

## Exercises

Work through `exercises.py` to practice implementing dunders with fill-in-the-blank exercises.

## Examples

Review `examples.py` for complete, network automation–flavored implementations of the data model.
