# Python Network Automation Tutorial

A comprehensive tutorial project for learning Python capabilities in the context of network automation and reliability. This project teaches Python built-ins, standard library modules, and third-party libraries through hands-on exercises and real-world network automation scenarios.

## Overview

This tutorial is organized into 12 modules, each focusing on a specific use case in network automation. Each module contains:

- **README.md** - Learning objectives, prerequisites, and concepts covered
- **exercises.py** - Fill-in-the-blank exercises with tutorial explanations
- **examples.py** - Complete working examples with real-world scenarios

## Learning Path

### Module 01: Core Fundamentals
**Focus:** Essential Python built-ins for data manipulation and validation
- Basic data types and conversions
- Iteration and filtering patterns
- Type checking and introspection
- String and numeric operations

**Prerequisites:** Basic Python knowledge

### Module 01b: Error Handling
**Focus:** Exception handling for reliable automation
- try/except/else/finally and when each runs
- Catching specific exceptions; avoid bare except
- Re-raising and logging in handlers
- Per-device handling so one failure does not kill the batch
- Fail fast with clear messages

**Prerequisites:** Module 01

### Module 02: Data Structures
**Focus:** Advanced collections for managing network device data
- Defaultdict for grouping operations
- Named tuples for structured data
- Counters for statistics
- Deques for buffering

**Prerequisites:** Module 01

### Module 02b: Objects and Special Methods (Dunders)
**Focus:** Python's data model and double-underscore methods
- `__repr__` and `__str__` for logging and display
- `__len__`, `__getitem__`, `__iter__` for container-like types
- `__eq__` for value equality; `__call__` and context managers

**Prerequisites:** Module 01 (Module 02 helpful)

### Module 03: File I/O Operations
**Focus:** Reading and writing configs, logs, and state files
- File operations with `open()`
- JSON serialization
- Path manipulation
- Environment variables

**Prerequisites:** Module 01

### Module 04: Device Management
**Focus:** Connecting to and managing network devices
- Netmiko for SSH connections
- NAPALM for vendor-agnostic operations
- Paramiko for low-level SSH
- Device facts gathering

**Prerequisites:** Modules 01-03

### Module 05: API Integration
**Focus:** Integrating with REST APIs and source of truth systems
- Requests library
- NetBox integration
- Nautobot integration
- Session management

**Prerequisites:** Modules 01-03

### Module 06: Configuration Management
**Focus:** Templating, parsing, and generating configurations
- Jinja2 templating
- YAML parsing
- Regular expressions
- CLI argument parsing

**Prerequisites:** Modules 01-03

### Module 06b: Pattern Detection Tools
**Focus:** Deriving parsing patterns for code challenges and device output
- When to use regex vs line/column parsing vs templates
- Step-by-step process: shape → method → pattern → edge cases
- Interview-style exercises (log parsing, table parsing, extract fields)
- LESSON_derive_patterns.md and examples with thought process

**Prerequisites:** Module 06 (Module 01, 03)

### Module 07: Monitoring & Observability
**Focus:** Logging, metrics, and observability
- Python logging module
- Datetime handling
- Prometheus metrics
- Timestamp management

**Prerequisites:** Modules 01-03

### Module 08: Concurrency & Parallelism
**Focus:** Parallel operations for efficient automation
- Threading for I/O-bound tasks
- Async/await for concurrent operations
- Multiprocessing for CPU-bound tasks
- Thread pools and process pools

**Prerequisites:** Modules 01-04

### Module 09: Data Analysis
**Focus:** Analyzing telemetry and performance metrics
- NumPy for numerical operations
- Pandas for data manipulation
- SciPy for statistical analysis
- Matplotlib for visualization

**Prerequisites:** Modules 01-03

### Module 10: Infrastructure as Code
**Focus:** Integrating Python with IaC tools
- Subprocess execution
- Ansible Python API
- Terraform integration
- CLI automation

**Prerequisites:** Modules 01-03

### Module 11: Cloud & Orchestration
**Focus:** Cloud and container automation
- Docker API
- Kubernetes client
- AWS Boto3
- Container orchestration

**Prerequisites:** Modules 01-05

### Module 12: Advanced Patterns
**Focus:** Advanced Python patterns and frameworks
- Function decorators and caching
- Data validation with Pydantic
- API development (FastAPI/Flask)
- Database operations (SQLAlchemy)

**Prerequisites:** All previous modules

### Module 12b: Data Validation with Pydantic
**Focus:** Pydantic from beginner to advanced
- BaseModel, Field, ValidationError; model_dump / model_validate
- Nested models, field_validator, model_validator
- BaseSettings for config; ValidationReport-style patterns

**Prerequisites:** Module 01 (Module 02 or 02b helpful)

## Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start with Module 01:**
   ```bash
   cd 01_core_fundamentals
   python exercises.py
   ```

## How to Use

### Working Through Exercises

1. **Read the README.md** in each module to understand the learning objectives
2. **Open exercises.py** and read the tutorial sections
3. **Fill in the blanks** marked with `# TODO: Fill in the blank`
4. **Uncomment test cases** to verify your solutions
5. **Review examples.py** for complete working implementations

### Exercise Format

Each exercise follows this pattern:

```python
def example_function() -> str:
    """
    Tutorial explanation of the concept...
    """
    # TODO: Fill in the blank - replace None with the correct code
    return None  # Replace this line
```

### Example Format

Examples show complete, production-ready code:

```python
def example_function() -> str:
    """
    Complete working example with error handling...
    """
    try:
        # Implementation here
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

## Code Style

This project follows the workspace code style guidelines:

- **Formatting:** Black (88 char line length)
- **Type hints:** Added to public functions
- **Naming:** `snake_case` for functions/variables, `UPPER_CASE` for constants
- **Error handling:** Catch specific exceptions with clear messages
- **Logging:** Use `logging` module, avoid `print` in non-CLI code
- **Paths:** Use `pathlib.Path` instead of string paths

## Security Notes

- **Never hardcode credentials** - Use environment variables or config files
- **Validate inputs** - Always validate user input and API responses
- **Handle errors gracefully** - Network operations can fail, plan for it
- **Use secure connections** - Prefer SSH keys, TLS, and secure protocols

## Real-World Scenarios

Each module includes examples based on real network automation scenarios:

- **Device provisioning** - Configuring new network devices
- **Configuration backup** - Backing up device configs
- **Monitoring** - Collecting and analyzing metrics
- **Compliance checking** - Validating configurations
- **Incident response** - Automated troubleshooting
- **Inventory management** - Source of truth integration

## Related Projects

For infrastructure-as-code and tooling practice in the same repo:

- **ansible-lessons/** — Beginner-to-advanced Ansible (inventory, playbooks, roles, Vault, Python driver)
- **terraform-lessons/** — Beginner-to-advanced Terraform (HCL, state, modules, Python integration)

## Contributing

When adding new exercises or examples:

1. Follow the existing format and style
2. Include realistic network automation scenarios
3. Add error handling and logging
4. Include type hints
5. Test your examples before committing

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [NAPALM Documentation](https://napalm.readthedocs.io/)
- [Network Automation Best Practices](https://networktocode.com/)

## License

This tutorial is for educational purposes. Use responsibly in production environments.
