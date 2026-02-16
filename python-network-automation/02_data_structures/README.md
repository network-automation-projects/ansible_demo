# Module 02: Data Structures

Advanced Python collections for managing network device data and state.

## Learning Objectives

By completing this module, you will learn:

- How to use defaultdict for grouping operations without key checks
- How to create named tuples for structured data
- How to count occurrences with Counter
- How to use deque for efficient buffering
- How to preserve insertion order with OrderedDict
- How to safely copy objects (shallow vs deep)

## Prerequisites

- Module 01: Core Fundamentals
- Understanding of basic Python collections (list, dict, tuple)

## Lists & Dictionaries Practice (Basics → Advanced)

If you want focused practice on **lists and dicts** before or alongside this module, use `lists_dicts_practice.py`. It covers:

- **Part 1 — List basics:** indexing, slicing, append/extend, `in`/`not in`, building lists from ranges
- **Part 2 — Dict basics:** creation, `.get()`, `.setdefault()`, `.keys()`/`.values()`/`.items()`, building dicts from lists
- **Part 3 — Intermediate:** list of dicts, list/dict comprehensions, filtering, merging configs
- **Part 4 — Advanced:** nested dicts, safe nested access, flattening, grouping, sorting, inverting mappings

Complete the TODO sections and uncomment the test block at the bottom to verify. Good preparation for network automation interviews and day-to-day scripting. **Answers:** `lists_dicts_practice_answers.py` (run it to confirm all tests pass).

## Concepts Covered

### collections.defaultdict
- Automatic default values for missing keys
- Grouping operations without key existence checks
- Common use: Grouping interfaces by status, devices by vendor

### collections.namedtuple
- Tuple subclass with named fields
- Immutable structured data
- Common use: Device facts, interface records, network facts

### collections.Counter
- Dictionary subclass for counting hashable objects
- Counting occurrences efficiently
- Common use: Error type counting, interface status counting

### collections.deque
- Double-ended queue with O(1) appends/pops
- Efficient for buffering recent data
- Common use: Recent telemetry buffer, command history

### collections.OrderedDict
- Dictionary that remembers insertion order
- Preserves order of operations
- Common use: Config application order, sequenced operations

### copy.copy and copy.deepcopy
- Shallow copy: Copies object, references nested objects
- Deep copy: Recursively copies all nested objects
- Common use: Duplicating configs, cloning device state

## Use Cases in Network Automation

### Device Inventory Management
- Use defaultdict to group devices by site or vendor
- Use namedtuple for structured device facts
- Use Counter to count device types

### Interface Statistics
- Use Counter to count interface statuses
- Use defaultdict to group interfaces by VLAN
- Use namedtuple for interface records

### Configuration Management
- Use OrderedDict to preserve config application order
- Use deepcopy to clone device state safely
- Use deque to buffer recent config changes

### Monitoring and Telemetry
- Use deque to buffer recent telemetry data
- Use Counter to count error types
- Use defaultdict to aggregate metrics by device

## Related Modules

- **Module 01:** Core Fundamentals (prerequisite)
- **Module 03:** File I/O (uses collections for data structures)
- **Module 04:** Device Management (uses collections for device data)

## Exercises

- **`lists_dicts_practice.py`** — Lists and dictionaries from basics to advanced (optional refresher or prep).
- **`basic_practice.py`** — Sets (dedupe, intersection, union, add/discard) and simple file I/O (read/write/append with pathlib). **Answers:** `basic_practice_answers.py`.
- **`exercises.py`** — Fill-in-the-blank exercises for defaultdict, namedtuple, Counter, deque, OrderedDict, and copy.
- **`exercises-loops.py`** — Practice for loops: nested loops, `while` (retry), and loop control (`break`/`continue`) in a network automation context.
- **`exercises_classes.py`** — Practice writing classes: `__init__` and attributes, instance methods, a class that holds a collection, `__str__`, and a small class from scratch (Device, Interface). **Answers:** `exercises_classes_answers.py`.
- **`exercises_dataclasses.py`** — Practice with `@dataclass`, `field(default_factory=...)`, `replace()`, `asdict()`, and when to use dataclasses vs Pydantic. **Answers:** `exercises_dataclasses_answers.py`.

## Examples

Review `examples.py` for complete, production-ready implementations.
