# Dashboard Netmiko - Learning Stubs

A learning version of the Network Automation Dashboard with stub implementations. This project is designed to help you learn how to build a complete network automation dashboard by implementing the functionality yourself.

## What is This?

This is a **stubbed version** of the `dashboard-netmiko` project. All the structure, templates, and file organization are in place, but the core functionality needs to be implemented. Each file contains detailed TODO comments and learning notes to guide you through the implementation.

## Project Structure

```
dashboard-netmiko-stubs/
├── app.py                  # Flask web application (STUB - needs implementation)
├── config/
│   └── devices.yaml        # Device inventory configuration (complete)
├── core/
│   ├── __init__.py
│   └── netmiko_core.py     # Netmiko connection logic (STUB - needs implementation)
├── utils/
│   ├── __init__.py
│   ├── database.py         # SQLite database operations (STUB - needs implementation)
│   └── backup_manager.py   # Configuration backup management (STUB - needs implementation)
├── templates/              # HTML templates (complete - no changes needed)
│   ├── base.html
│   ├── index.html
│   ├── devices.html
│   ├── device_detail.html
│   ├── 404.html
│   └── 500.html
├── static/                 # CSS styles (complete - no changes needed)
│   └── css/
│       └── style.css
├── tests/                  # Unit tests (STUB - needs implementation)
│   ├── __init__.py
│   └── test_netmiko_core.py
├── backups/                # Configuration backups storage (empty)
├── data/                   # SQLite database location (empty)
├── logs/                   # Application logs (empty)
├── requirements.txt        # Python dependencies (complete)
└── README.md               # This file
```

## Learning Path

### Phase 1: Core Netmiko Operations (Start Here!)

**File: `core/netmiko_core.py`**

1. **`load_inventory()`** - Load device inventory from YAML
   - Learn: YAML file parsing
   - Learn: File I/O and error handling
   - Expected time: 15-30 minutes

2. **`get_credentials()`** - Secure credential handling
   - Learn: Environment variables
   - Learn: User input handling
   - Expected time: 15-20 minutes

3. **`gather_device_facts()`** - Connect to a single device
   - Learn: Netmiko SSH connections
   - Learn: Command execution on network devices
   - Learn: Error handling for network operations
   - Expected time: 1-2 hours

4. **`backup_config()`** - Backup device configuration
   - Learn: File operations
   - Learn: Timestamp generation
   - Expected time: 30-45 minutes

5. **`collect_all_facts()`** - Parallel device connections
   - Learn: Concurrent programming with ThreadPoolExecutor
   - Learn: Asynchronous operations
   - Expected time: 1-2 hours

### Phase 2: Database Operations

**File: `utils/database.py`**

1. **`__init__()` and `_create_tables()`** - Database initialization
   - Learn: SQLite database setup
   - Learn: SQL table creation
   - Expected time: 30-45 minutes

2. **`upsert_device()` and `get_device()`** - Basic CRUD operations
   - Learn: SQL INSERT/REPLACE
   - Learn: SQL SELECT queries
   - Learn: JSON serialization/deserialization
   - Expected time: 45-60 minutes

3. **`get_all_devices()`** - Query all records
   - Learn: SQL SELECT with ORDER BY
   - Expected time: 15-20 minutes

4. **Backup and audit methods** - Related data operations
   - Learn: Foreign keys and relationships
   - Learn: Filtering and limiting results
   - Expected time: 1 hour

5. **`get_device_stats()`** - Aggregation queries
   - Learn: SQL COUNT and GROUP BY
   - Learn: Date/time functions
   - Expected time: 30-45 minutes

### Phase 3: Backup Management

**File: `utils/backup_manager.py`**

1. **`__init__()`** - Initialize backup manager
   - Learn: Directory creation
   - Learn: Dependency injection
   - Expected time: 15 minutes

2. **`backup_device()`** - Single device backup
   - Learn: Integrating multiple modules
   - Learn: File size operations
   - Expected time: 30 minutes

3. **`backup_device_by_ip()` and `backup_all_devices()`** - Batch operations
   - Learn: Finding items in lists
   - Learn: Iteration patterns
   - Expected time: 30-45 minutes

4. **`cleanup_old_backups()`** - Maintenance operations
   - Learn: Date arithmetic
   - Learn: File deletion
   - Expected time: 45-60 minutes

### Phase 4: Flask Web Application

**File: `app.py`**

1. **Route: `index()`** - Dashboard home page
   - Learn: Flask route decorators
   - Learn: Template rendering
   - Learn: Passing data to templates
   - Expected time: 30 minutes

2. **Route: `devices()`** - Device list page
   - Learn: List views in Flask
   - Expected time: 15 minutes

3. **Route: `device_detail()`** - Device detail page
   - Learn: URL parameters
   - Learn: Error handling and redirects
   - Expected time: 30 minutes

4. **Route: `trigger_backup()`** - POST endpoint
   - Learn: Form handling
   - Learn: Flash messages
   - Expected time: 20 minutes

5. **Route: `refresh_devices()`** - AJAX endpoint
   - Learn: JSON responses
   - Learn: AJAX patterns
   - Expected time: 30 minutes

6. **API routes** - RESTful endpoints
   - Learn: API design
   - Learn: JSON serialization
   - Expected time: 45 minutes

### Phase 5: Testing

**File: `tests/test_netmiko_core.py`**

1. **Test structure** - Understanding unittest
   - Learn: Test classes and methods
   - Learn: setUp() and tearDown()
   - Expected time: 30 minutes

2. **Simple tests** - Testing file operations
   - Learn: Assertions
   - Learn: Test data setup
   - Expected time: 45 minutes

3. **Mocking tests** - Testing with mocks
   - Learn: Mock objects
   - Learn: Patching functions
   - Expected time: 1-2 hours

## Installation

### Prerequisites

- Python 3.9 or higher
- Network access to target devices (for testing)
- SSH credentials for network devices

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd dashboard-netmiko-stubs
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure device inventory:**
   Edit `config/devices.yaml` with your network devices (or use the examples provided).

5. **Set up credentials (optional but recommended):**
   ```bash
   export NET_USER=your_username
   export NET_PASS=your_password
   ```

## How to Use This Learning Project

### Step 1: Read the Code

Start by reading through the stub files. Each file has:
- **LEARNING NOTES** at the top explaining the module's purpose
- **TODO comments** explaining what needs to be implemented
- **Example code** showing expected patterns
- **Cross-references** to related files

### Step 2: Implement One Function at a Time

Follow the learning path above. Don't try to implement everything at once. Start with the simplest functions and work your way up.

### Step 3: Test Your Implementation

After implementing each function:
1. Test it in isolation (if possible)
2. Run the tests: `pytest tests/`
3. Try running the Flask app: `python app.py`
4. Check the logs in `logs/` directory

### Step 4: Reference the Original

If you get stuck, you can reference the original `dashboard-netmiko` project to see how it was implemented. But try to implement it yourself first!

## Key Concepts You'll Learn

### Network Automation
- **Netmiko**: Python library for SSH connections to network devices
- **Multi-vendor support**: Cisco IOS, NX-OS, Juniper, Arista
- **Concurrent connections**: Parallel device management
- **Configuration backups**: Automated backup workflows

### Web Development
- **Flask**: Python web framework
- **Jinja2 templates**: Server-side templating
- **RESTful APIs**: JSON endpoints
- **AJAX**: Asynchronous web requests

### Database Operations
- **SQLite**: File-based database
- **SQL queries**: SELECT, INSERT, UPDATE
- **JSON storage**: Serializing complex data
- **Database relationships**: Foreign keys

### Software Engineering
- **Error handling**: Try/except blocks
- **Logging**: Structured logging
- **Testing**: Unit tests with mocks
- **Code organization**: Modular design

## Common Pitfalls and Tips

### Pitfall 1: Not Handling Errors
**Problem**: Code crashes when devices are unreachable  
**Solution**: Always wrap network operations in try/except blocks

### Pitfall 2: Blocking Operations
**Problem**: Web app freezes when connecting to devices  
**Solution**: Use concurrent execution (ThreadPoolExecutor) for device operations

### Pitfall 3: Hardcoding Credentials
**Problem**: Credentials in code or config files  
**Solution**: Use environment variables or secure credential storage

### Pitfall 4: Not Testing
**Problem**: Code works sometimes but fails unpredictably  
**Solution**: Write tests, especially for error cases

### Tip 1: Start Small
Don't try to implement everything at once. Get one function working, then move to the next.

### Tip 2: Use Logging
Add logging statements to understand what your code is doing. Check `logs/` directory.

### Tip 3: Read Error Messages
Python error messages are usually helpful. Read them carefully!

### Tip 4: Test with Real Devices
Once you have basic functionality working, test with real network devices (in a lab environment).

## Troubleshooting

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check that you're in the project root directory

### Database Errors
- Ensure `data/` directory exists and is writable
- Check file permissions
- Delete `data/inventory.db` and let it recreate if corrupted

### Connection Errors
- Verify network connectivity to devices
- Check firewall rules
- Verify SSH is enabled on devices
- Check credentials are correct

### Template Errors
- Make sure Flask can find templates directory
- Check template syntax (Jinja2)
- Verify all required variables are passed to templates

## Next Steps After Completion

Once you've implemented all the stubs:

1. **Add features**: Configuration diff, compliance checking, etc.
2. **Improve parsing**: Use TextFSM for structured output parsing
3. **Add authentication**: User login and authorization
4. **Deploy**: Set up for production use
5. **Documentation**: Write API documentation
6. **CI/CD**: Set up automated testing and deployment

## Resources

- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Threading](https://docs.python.org/3/library/threading.html)

## Getting Help

If you're stuck:
1. Read the TODO comments in the code
2. Check the logs in `logs/` directory
3. Review error messages carefully
4. Reference the original `dashboard-netmiko` project
5. Search for specific error messages online

## License

This learning project is open source and available for educational purposes.

## Good Luck!

Take your time, implement one piece at a time, and don't be afraid to experiment. The best way to learn is by doing!



