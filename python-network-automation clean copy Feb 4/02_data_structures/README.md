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

Work through `exercises.py` to practice these concepts with fill-in-the-blank exercises.

## Examples

Review `examples.py` for complete, production-ready implementations.
