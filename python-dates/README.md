# Python Dates Exercise - Fill-in-the-Blank Tutorial

A comprehensive tutorial-style exercise project for learning Python datetime handling, focusing on the critical production principle: **Always store UTC internally, convert to user's timezone only for display**.

## Overview

This project contains three progressive exercise files that teach you how to work with dates and times in Python, following production best practices:

- **beginner.py** - Core concepts: UTC storage, timezone conversion, formatting, parsing
- **medium.py** - Advanced topics: Multiple timezones, locale formatting, relative time, database patterns
- **advanced.py** - Production patterns: API design, scheduled tasks, date range queries, logging

## Learning Objectives

By completing these exercises, you will learn:

✅ Why UTC is the standard for internal storage  
✅ How to convert between UTC and user timezones  
✅ Locale-aware date formatting  
✅ Relative time display ("2 hours ago", "yesterday")  
✅ Database storage and retrieval patterns  
✅ API response formatting best practices  
✅ Scheduled task timezone handling  
✅ Date range queries across timezones  
✅ Event logging with timezone context  
✅ Handling edge cases (DST transitions, ambiguous times)  

## Prerequisites

- Python 3.9+ (for `zoneinfo` support)
- Basic understanding of Python datetime module
- Familiarity with timezone concepts

For Python < 3.9, install `backports.zoneinfo`:
```bash
pip install backports.zoneinfo
```

## Setup

1. **Create a virtual environment** (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start with beginner.py**:
```bash
python beginner.py
```

## How to Use

Each file contains:
- **Tutorial explanations** - Learn the concepts before each exercise
- **Fill-in-the-blank exercises** - Marked with `# TODO: Fill in the blank`
- **Test cases** - Uncomment to test your solutions
- **Expected output** - See what your code should produce

### Exercise Structure

Each exercise follows this pattern:

1. **Tutorial section** - Explains the concept and why it matters
2. **Function skeleton** - Code with `# TODO` markers where you fill in
3. **Test section** - Uncomment to test your solution
4. **Expected output** - Shows what correct output looks like

### Example Exercise

```python
def create_utc_timestamp() -> datetime:
    """
    Create a timezone-aware UTC timestamp for the current moment.
    """
    # TODO: Fill in the blank - replace None with the correct function call
    # Hint: Use datetime.now() with timezone.utc
    return None  # Replace this line
```

**Solution:**
```python
def create_utc_timestamp() -> datetime:
    return datetime.now(timezone.utc)
```

## File Guide

### beginner.py

**Exercises:**
1. Creating UTC timestamps (`datetime.now(timezone.utc)`)
2. Converting UTC to user's local timezone (`.astimezone()`)
3. Formatting dates for display (`.strftime()`, `.isoformat()`)
4. Parsing ISO strings and ensuring UTC (`fromisoformat()`)

**Key Concepts:**
- Why UTC internally (consistency, no DST issues)
- `datetime.now(timezone.utc)` vs deprecated `datetime.utcnow()`
- Basic timezone conversion patterns

### medium.py

**Exercises:**
1. Handling multiple timezones (user preferences)
2. Locale-aware date formatting (`locale` module, `babel`)
3. Relative time display ("2 hours ago", "yesterday")
4. Timezone-aware database storage/retrieval

**Key Concepts:**
- `zoneinfo` (Python 3.9+) vs `pytz`
- Locale detection and formatting
- Common timezone pitfalls (DST, ambiguous times)

### advanced.py

**Exercises:**
1. API response formatting (UTC with timezone info)
2. Scheduled task timezone handling (cron jobs, background tasks)
3. Date range queries across timezones
4. Event logging with proper timezone context

**Key Concepts:**
- API design best practices (ISO 8601, timezone offsets)
- Cron jobs and scheduled tasks
- Database query patterns
- Structured logging

## Golden Rules

Remember these principles throughout the exercises:

1. **STORE UTC** - Always store datetimes in UTC in your database
2. **DISPLAY LOCAL** - Convert to user's timezone only when displaying
3. **BE EXPLICIT** - Always use timezone-aware datetimes in production
4. **HANDLE EDGE CASES** - DST transitions, ambiguous times, leap seconds

## Common Patterns

### Pattern 1: Store UTC, Display Local

```python
# Store in UTC
utc_dt = datetime.now(timezone.utc)
database.save(utc_dt)

# Display in user's timezone
user_tz = ZoneInfo('America/New_York')
user_dt = utc_dt.astimezone(user_tz)
display(user_dt.strftime("%Y-%m-%d %H:%M:%S %Z"))
```

### Pattern 2: Parse and Normalize to UTC

```python
def parse_to_utc(date_string: str) -> datetime:
    # Handle 'Z' suffix
    normalized = date_string.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    
    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Convert to UTC
    return dt.astimezone(timezone.utc)
```

### Pattern 3: Date Range Query

```python
def get_utc_range(local_date: date, user_tz: ZoneInfo) -> Tuple[datetime, datetime]:
    # Start of day in user's timezone
    start_local = datetime.combine(local_date, time.min, tzinfo=user_tz)
    # End of day in user's timezone
    end_local = datetime.combine(local_date, time.max, tzinfo=user_tz)
    
    # Convert to UTC
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)
```

## Testing Your Solutions

1. **Uncomment test sections** in each file
2. **Run the file**: `python beginner.py`
3. **Compare output** with expected results
4. **Fix any errors** and re-run

Example:
```python
# Uncomment after implementing:
utc_now = create_utc_timestamp()
print(f"Current UTC time: {utc_now}")
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'zoneinfo'"

**Solution:** You're using Python < 3.9. Install backports:
```bash
pip install backports.zoneinfo
```

Then update imports:
```python
from backports.zoneinfo import ZoneInfo
```

### "locale.Error: unsupported locale setting"

**Solution:** Locale exercises may fail if your system doesn't have the locale installed. This is expected - the exercises include fallback handling.

### "ValueError: Datetime must be timezone-aware"

**Solution:** You're trying to use a naive datetime (no timezone). Always ensure datetimes are timezone-aware:
```python
# Wrong (naive):
dt = datetime.now()

# Right (aware):
dt = datetime.now(timezone.utc)
```

## Best Practices Summary

### ✅ DO:

- Use `datetime.now(timezone.utc)` for current UTC time
- Always store UTC in databases
- Convert to user timezone only for display
- Use ISO 8601 format for APIs
- Use `zoneinfo` (Python 3.9+) for timezones
- Handle DST transitions explicitly
- Test with multiple timezones

### ❌ DON'T:

- Use `datetime.utcnow()` (deprecated, returns naive datetime)
- Store local time in databases
- Use naive datetimes in production
- Assume server timezone
- Ignore DST transitions
- Mix UTC and local time in calculations

## Additional Resources

- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [zoneinfo documentation](https://docs.python.org/3/library/zoneinfo.html)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [ISO 8601 standard](https://en.wikipedia.org/wiki/ISO_8601)
- [Babel documentation](https://babel.pocoo.org/) (for locale formatting)

## Next Steps

After completing these exercises:

1. **Practice with real projects** - Apply these patterns to your own code
2. **Explore libraries** - Check out `arrow`, `pendulum`, or `dateutil` for additional features
3. **Read production code** - See how real applications handle datetime
4. **Test edge cases** - Try DST transition dates, leap years, etc.

## License

This is an educational exercise project. Feel free to use and modify as needed.

## Contributing

Found an issue or want to improve an exercise? Feel free to submit improvements!

---

**Remember:** The most important rule is **STORE UTC, DISPLAY LOCAL**. Everything else follows from this principle.
