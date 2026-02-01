"""
Python Dates Exercise - Beginner Level
=======================================

This file teaches the fundamentals of working with dates and times in Python,
focusing on the critical principle: **Always store UTC internally, convert to
user's timezone only for display**.

Why UTC?
--------
- UTC (Coordinated Universal Time) is the standard time reference worldwide
- Storing UTC prevents Daylight Saving Time (DST) issues
- Ensures consistency across different servers and locations
- Makes it easy to convert to any user's local timezone when needed

Key Concepts:
- Naive datetime: No timezone information (avoid in production!)
- Aware datetime: Has timezone information (required for production)
- Always use timezone-aware datetimes in production code
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


# ============================================================================
# EXERCISE 1: Creating UTC Timestamps
# ============================================================================

"""
Tutorial: Creating UTC Timestamps
----------------------------------

In Python 3.9+, the recommended way to get the current UTC time is:
    datetime.now(timezone.utc)

⚠️  IMPORTANT: Avoid datetime.utcnow() - it's deprecated and returns a naive
    datetime (no timezone info). Always use datetime.now(timezone.utc) instead.

Why timezone.utc instead of utcnow()?
- utcnow() returns a naive datetime (no timezone attached)
- now(timezone.utc) returns an aware datetime (has UTC timezone)
- Aware datetimes are safer and required for production code
"""


def create_utc_timestamp() -> datetime:
    """
    Create a timezone-aware UTC timestamp for the current moment.
    
    Returns:
        A datetime object representing the current time in UTC.
        
    Example:
        >>> dt = create_utc_timestamp()
        >>> print(dt.tzinfo)
        UTC
        >>> print(dt.isoformat())
        2026-01-27T12:34:56.789123+00:00
    """
    # TODO: Fill in the blank - replace None with the correct function call
    # Hint: Use datetime.now() with timezone.utc
    return None  # Replace this line


# Test your solution:
if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 1: Creating UTC Timestamps")
    print("=" * 70)
    
    # Uncomment after implementing:
    # utc_now = create_utc_timestamp()
    # print(f"Current UTC time: {utc_now}")
    # print(f"Timezone info: {utc_now.tzinfo}")
    # print(f"Is timezone-aware? {utc_now.tzinfo is not None}")
    # print(f"ISO format: {utc_now.isoformat()}")
    
    print("\nExpected output:")
    print("Current UTC time: 2026-01-27 12:34:56.789123+00:00")
    print("Timezone info: UTC")
    print("Is timezone-aware? True")
    print("ISO format: 2026-01-27T12:34:56.789123+00:00")


# ============================================================================
# EXERCISE 2: Converting UTC to User's Local Timezone
# ============================================================================

"""
Tutorial: Converting UTC to Local Time
--------------------------------------

Once you have a UTC datetime, you can convert it to any timezone. The process:
1. Start with a UTC datetime (timezone-aware)
2. Use .astimezone() to convert to the target timezone
3. The datetime value automatically adjusts for the timezone offset

Common timezones:
- 'America/New_York' (Eastern Time, handles DST automatically)
- 'America/Los_Angeles' (Pacific Time)
- 'Europe/London' (UK time)
- 'Asia/Tokyo' (Japan Standard Time)

Note: In Python 3.9+, use zoneinfo.ZoneInfo() for timezones.
For older Python, you'd use pytz, but zoneinfo is preferred.
"""

try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    from backports.zoneinfo import ZoneInfo


def convert_utc_to_local(utc_dt: datetime, timezone_name: str) -> datetime:
    """
    Convert a UTC datetime to a specific timezone.
    
    Args:
        utc_dt: A timezone-aware datetime in UTC
        timezone_name: IANA timezone name (e.g., 'America/New_York')
        
    Returns:
        A datetime object in the specified timezone
        
    Example:
        >>> utc = datetime(2026, 1, 27, 12, 0, 0, tzinfo=timezone.utc)
        >>> ny_time = convert_utc_to_local(utc, 'America/New_York')
        >>> print(ny_time)
        2026-01-27 07:00:00-05:00  # 5 hours behind UTC (EST)
    """
    # TODO: Fill in the blank - convert utc_dt to the specified timezone
    # Hint: Use .astimezone() with ZoneInfo()
    # TODO: Replace None with the conversion logic
    return None  # Replace this line


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 2: Converting UTC to Local Timezone")
    print("=" * 70)
    
    # Create a sample UTC datetime
    sample_utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
    
    # Uncomment after implementing:
    # ny_time = convert_utc_to_local(sample_utc, 'America/New_York')
    # la_time = convert_utc_to_local(sample_utc, 'America/Los_Angeles')
    # tokyo_time = convert_utc_to_local(sample_utc, 'Asia/Tokyo')
    # 
    # print(f"UTC:        {sample_utc}")
    # print(f"New York:   {ny_time}")
    # print(f"Los Angeles: {la_time}")
    # print(f"Tokyo:      {tokyo_time}")
    
    print("\nExpected output:")
    print("UTC:        2026-01-27 15:30:00+00:00")
    print("New York:   2026-01-27 10:30:00-05:00")
    print("Los Angeles: 2026-01-27 07:30:00-08:00")
    print("Tokyo:      2026-01-28 00:30:00+09:00")


# ============================================================================
# EXERCISE 3: Formatting Dates for Display
# ============================================================================

"""
Tutorial: Formatting Dates for Display
--------------------------------------

When displaying dates to users, you want them in a readable format. Common formats:
- ISO 8601: "2026-01-27T15:30:00+00:00" (good for APIs, technical)
- Human-readable: "January 27, 2026 at 3:30 PM" (good for UI)
- Short date: "01/27/2026" (compact)
- Relative time: "2 hours ago" (we'll cover this in medium.py)

Methods:
- .strftime(): Format datetime as string (you control the format)
- .isoformat(): Standard ISO 8601 format (good default for APIs)
- .strftime() with locale: Locale-aware formatting (covered in medium.py)

Best Practice: Always format the timezone-aware datetime in the user's timezone,
not in UTC. Users don't think in UTC!
"""


def format_date_for_display(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Format a datetime for display to users.
    
    Args:
        dt: A timezone-aware datetime
        format_string: strftime format string (default shows timezone)
        
    Returns:
        Formatted date string
        
    Example:
        >>> utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
        >>> ny = utc.astimezone(ZoneInfo('America/New_York'))
        >>> format_date_for_display(ny, "%B %d, %Y at %I:%M %p")
        'January 27, 2026 at 03:30 PM'
    """
    # TODO: Fill in the blank - format the datetime using strftime
    # Hint: Use the .strftime() method on the datetime object
    return ""  # Replace this line


def format_date_iso(dt: datetime) -> str:
    """
    Format a datetime in ISO 8601 format (standard for APIs).
    
    Args:
        dt: A timezone-aware datetime
        
    Returns:
        ISO 8601 formatted string (e.g., "2026-01-27T15:30:00+00:00")
        
    Example:
        >>> utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
        >>> format_date_iso(utc)
        '2026-01-27T15:30:00+00:00'
    """
    # TODO: Fill in the blank - use isoformat() method
    # Hint: Datetime objects have an .isoformat() method
    return ""  # Replace this line


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 3: Formatting Dates for Display")
    print("=" * 70)
    
    sample_utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
    ny_time = sample_utc.astimezone(ZoneInfo('America/New_York'))
    
    # Uncomment after implementing:
    # print(f"ISO format: {format_date_iso(sample_utc)}")
    # print(f"User-friendly: {format_date_for_display(ny_time, '%B %d, %Y at %I:%M %p %Z')}")
    # print(f"Short format: {format_date_for_display(ny_time, '%m/%d/%Y %H:%M')}")
    
    print("\nExpected output:")
    print("ISO format: 2026-01-27T15:30:00+00:00")
    print("User-friendly: January 27, 2026 at 03:30 PM EST")
    print("Short format: 01/27/2026 10:30")


# ============================================================================
# EXERCISE 4: Parsing ISO Strings and Ensuring UTC
# ============================================================================

"""
Tutorial: Parsing Date Strings
-------------------------------

When receiving date strings (from APIs, databases, user input), you need to:
1. Parse the string into a datetime object
2. Ensure it's timezone-aware
3. Convert to UTC if it's not already

Common scenarios:
- ISO 8601 strings: "2026-01-27T15:30:00Z" or "2026-01-27T15:30:00+00:00"
- Strings with timezone: "2026-01-27T15:30:00-05:00" (EST)
- Naive strings: "2026-01-27 15:30:00" (no timezone - assume UTC or raise error)

Best Practice:
- Always assume incoming strings without timezone are UTC (or raise an error)
- Use datetime.fromisoformat() for ISO strings (Python 3.7+)
- Always convert to UTC for internal storage
"""


def parse_and_normalize_to_utc(date_string: str) -> datetime:
    """
    Parse an ISO date string and ensure it's in UTC.
    
    Handles:
    - "2026-01-27T15:30:00Z" (Z means UTC)
    - "2026-01-27T15:30:00+00:00" (explicit UTC offset)
    - "2026-01-27T15:30:00-05:00" (converts to UTC)
    - "2026-01-27T15:30:00" (naive, assumes UTC)
    
    Args:
        date_string: ISO 8601 formatted date string
        
    Returns:
        A timezone-aware datetime in UTC
        
    Example:
        >>> parse_and_normalize_to_utc("2026-01-27T15:30:00Z")
        datetime.datetime(2026, 1, 27, 15, 30, tzinfo=timezone.utc)
        
        >>> parse_and_normalize_to_utc("2026-01-27T15:30:00-05:00")
        datetime.datetime(2026, 1, 27, 20, 30, tzinfo=timezone.utc)  # +5 hours
    """
    # TODO: Fill in the blanks
    # Step 1: Replace 'Z' with '+00:00' if present (Python's fromisoformat doesn't handle Z)
    normalized = date_string.replace("Z", "+00:00")
    
    # Step 2: Parse the string using fromisoformat()
    # TODO: Replace None with the parsing logic
    dt = None  # Replace this line
    
    # Step 3: If the datetime is naive (no timezone), assume UTC
    # TODO: Check if dt.tzinfo is None, and if so, set it to UTC
    # Hint: Use timezone.utc
    
    # Step 4: Convert to UTC if it's not already
    # TODO: Convert dt to UTC using .astimezone(timezone.utc)
    # Hint: If already UTC, this is a no-op, but it's safe to always do it
    
    return dt  # This should be a UTC datetime


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 4: Parsing ISO Strings and Ensuring UTC")
    print("=" * 70)
    
    test_cases = [
        "2026-01-27T15:30:00Z",           # UTC with Z
        "2026-01-27T15:30:00+00:00",      # UTC with offset
        "2026-01-27T15:30:00-05:00",      # EST (should become 20:30 UTC)
        "2026-01-27T15:30:00",            # Naive (should assume UTC)
    ]
    
    # Uncomment after implementing:
    # for test_str in test_cases:
    #     result = parse_and_normalize_to_utc(test_str)
    #     print(f"Input:  {test_str}")
    #     print(f"Output: {result} (UTC: {result.tzinfo == timezone.utc})")
    #     print()
    
    print("\nExpected output:")
    print("Input:  2026-01-27T15:30:00Z")
    print("Output: 2026-01-27 15:30:00+00:00 (UTC: True)")
    print()
    print("Input:  2026-01-27T15:30:00+00:00")
    print("Output: 2026-01-27 15:30:00+00:00 (UTC: True)")
    print()
    print("Input:  2026-01-27T15:30:00-05:00")
    print("Output: 2026-01-27 20:30:00+00:00 (UTC: True)")
    print()
    print("Input:  2026-01-27T15:30:00")
    print("Output: 2026-01-27 15:30:00+00:00 (UTC: True)")


# ============================================================================
# SUMMARY: Key Takeaways
# ============================================================================

"""
Congratulations! You've completed the beginner exercises. Here's what you learned:

✅ Always use datetime.now(timezone.utc) for current UTC time (not utcnow())
✅ Convert UTC to user's timezone only when displaying (using .astimezone())
✅ Format dates in the user's timezone, not UTC
✅ Always parse and normalize incoming date strings to UTC
✅ Always work with timezone-aware datetimes in production

Next Steps:
- Move to medium.py to learn about locale-aware formatting and relative times
- Learn about handling DST transitions and ambiguous times
- Practice with database storage patterns

Remember the golden rule:
    STORE UTC, DISPLAY LOCAL
"""
