# Module 03: File I/O Operations

Reading and writing configuration files, logs, and state files in network automation.

## Learning Objectives

By completing this module, you will learn:

- How to read and write files safely
- How to work with JSON for structured data
- How to manipulate file paths
- How to use environment variables for configuration
- How to persist state between automation runs

## Prerequisites

- Module 01: Core Fundamentals
- Module 02: Data Structures (helpful but not required)
- Basic understanding of file systems

## Concepts Covered

### File Operations
- `open()` - Opening files for reading/writing
- File context managers (`with` statements)
- Reading and writing text/binary files

### Path Operations
- `os.path.join()` - Cross-platform path joining
- `os.path.exists()` - Checking file existence
- `os.path.dirname()` - Getting directory name
- `os.path.abspath()` - Getting absolute paths
- `os.getcwd()` - Current working directory

### Directory Operations
- `os.mkdir()` - Creating directories
- `os.rmdir()` - Removing empty directories
- `os.remove()` - Deleting files

### JSON Operations
- `json.loads()` - Parsing JSON strings
- `json.dumps()` - Serializing to JSON strings
- `json.load()` - Reading JSON from files
- `json.dump()` - Writing JSON to files

### Environment Variables
- `os.environ` - Accessing environment variables
- Secure credential handling
- Configuration via environment

### State Persistence
- `pickle.dump()` - Serializing Python objects
- `pickle.load()` - Deserializing Python objects
- When to use JSON vs pickle

## Use Cases in Network Automation

### Configuration Backup
- Save device configurations to files
- Organize backups by device and timestamp
- Restore configurations from backups

### Inventory Management
- Load device inventory from JSON files
- Export inventory to files
- Update inventory files

### Logging
- Write automation logs to files
- Rotate log files
- Parse log files for analysis

### State Management
- Save automation state between runs
- Resume interrupted operations
- Track progress in long-running tasks

## Related Modules

- **Module 01:** Core Fundamentals (prerequisite)
- **Module 06:** Configuration Management (uses file I/O for configs)
- **Module 07:** Monitoring & Observability (uses file I/O for logs)

## Exercises

Work through `exercises.py` to practice these concepts with fill-in-the-blank exercises.

## Examples

Review `examples.py` for complete, production-ready implementations.
