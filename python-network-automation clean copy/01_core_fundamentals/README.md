# Module 01: Core Fundamentals

Essential Python built-in functions for network automation and reliability engineering.

## Learning Objectives

By completing this module, you will learn:

- How to manipulate and validate data types
- How to iterate over collections efficiently
- How to check types and introspect objects
- How to work with strings, numbers, and collections
- How to filter, map, and transform data

## Prerequisites

- Basic Python knowledge (variables, functions, basic data types)
- Understanding of lists, dictionaries, and tuples
- Familiarity with basic control flow (if/else, loops)

## Concepts Covered

### Data Type Conversions
- `bool()`, `int()`, `float()`, `str()` - Type conversions
- `tuple()`, `list()`, `dict()`, `set()`, `frozenset()` - Collection constructors

### Numeric Operations
- `abs()` - Absolute value for metric differences
- `round()` - Rounding for formatted output
- `pow()` - Exponentiation for calculations
- `divmod()` - Quotient and remainder for pagination
- `min()`, `max()`, `sum()` - Aggregations

### String Operations
- `chr()`, `ord()` - Character code conversions
- `ascii()` - ASCII-safe string representation
- `format()` - String formatting
- `repr()` - Object representation

### Binary/Hex Operations
- `bin()`, `hex()`, `oct()` - Number base conversions
- `bytes()`, `bytearray()` - Binary data handling
- `memoryview()` - Efficient binary operations

### Iteration & Filtering
- `range()` - Number sequences
- `enumerate()` - Indexed iteration
- `zip()` - Parallel iteration
- `filter()` - Conditional filtering
- `map()` - Transform operations
- `iter()`, `next()` - Iterator protocol
- `reversed()` - Reverse iteration
- `sorted()` - Sorting collections

### Type Checking & Introspection
- `isinstance()` - Type checking
- `type()` - Type information
- `callable()` - Function checking
- `hasattr()`, `getattr()`, `setattr()`, `delattr()` - Attribute access
- `dir()`, `vars()`, `globals()`, `locals()` - Namespace inspection
- `id()`, `hash()` - Object identity
- `help()` - Interactive help

### Collection Operations
- `len()` - Collection size
- `slice()` - Slicing operations
- `all()`, `any()` - Boolean aggregations

## Use Cases in Network Automation

### Device Validation
- Use `all()` to verify all interfaces are up before config changes
- Use `any()` to check if any alerts exist
- Use `isinstance()` to validate API response types

### Data Processing
- Use `enumerate()` to assign sequential IPs to devices
- Use `zip()` to pair device names with IPs
- Use `filter()` to find devices needing updates
- Use `map()` to transform device data

### Metrics & Calculations
- Use `abs()` for latency variations
- Use `min()`, `max()` for performance metrics
- Use `sum()` for bandwidth aggregation
- Use `round()` for formatted reports

### Type Safety
- Use `isinstance()` for robust error handling
- Use `callable()` before invoking plugin functions
- Use `hasattr()` for feature detection

## Related Modules

- **Module 02:** Data Structures (builds on collections)
- **Module 03:** File I/O (uses string operations)
- **Module 04:** Device Management (uses validation patterns)

## Exercises

Work through `exercises.py` to practice these concepts with fill-in-the-blank exercises.

## Examples

Review `examples.py` for complete, production-ready implementations.
