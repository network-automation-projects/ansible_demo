"""
Python Dates Exercise - Medium Level
======================================

This file builds on the beginner concepts and covers more advanced topics:
- Handling multiple timezones and user preferences
- Locale-aware date formatting
- Relative time display ("2 hours ago", "yesterday")
- Database storage and retrieval patterns

Prerequisites:
- You should understand UTC storage and basic timezone conversion
- Familiarity with datetime.now(timezone.utc) and .astimezone()
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
import locale

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


# ============================================================================
# EXERCISE 1: Handling Multiple Timezones (User Preferences)
# ============================================================================

"""
Tutorial: User Timezone Preferences
------------------------------------

In real applications, users often have timezone preferences stored in their
profile. You need to:
1. Store all timestamps in UTC in your database
2. When displaying to a user, convert from UTC to their preferred timezone
3. Handle cases where the user hasn't set a preference (default to UTC or detect)

Best Practice:
- Store user timezone as IANA timezone name (e.g., 'America/New_York')
- Always validate timezone names (invalid ones will raise exceptions)
- Provide a sensible default (UTC or system timezone)
"""


class UserTimezoneManager:
    """
    Manages timezone conversions for users with different timezone preferences.
    """
    
    def __init__(self, default_timezone: str = "UTC"):
        """
        Initialize with a default timezone.
        
        Args:
            default_timezone: IANA timezone name to use when user hasn't set one
        """
        self.default_timezone = default_timezone
    
    def get_user_timezone(self, user_id: str, user_preferences: Dict[str, str]) -> ZoneInfo:
        """
        Get the timezone for a specific user.
        
        Args:
            user_id: Unique identifier for the user
            user_preferences: Dictionary mapping user_id to timezone name
            
        Returns:
            ZoneInfo object for the user's timezone, or default if not found
            
        Example:
            >>> manager = UserTimezoneManager()
            >>> prefs = {"user123": "America/New_York", "user456": "Europe/London"}
            >>> tz = manager.get_user_timezone("user123", prefs)
            >>> print(tz)
            America/New_York
        """
        # TODO: Fill in the blank
        # Step 1: Check if user_id exists in user_preferences
        # Step 2: If found, return ZoneInfo for that timezone
        # Step 3: If not found, return ZoneInfo for default_timezone
        # Hint: Use ZoneInfo() constructor
        return None  # Replace this line
    
    def convert_to_user_timezone(
        self, 
        utc_dt: datetime, 
        user_id: str, 
        user_preferences: Dict[str, str]
    ) -> datetime:
        """
        Convert a UTC datetime to a user's preferred timezone.
        
        Args:
            utc_dt: Timezone-aware datetime in UTC
            user_id: User identifier
            user_preferences: Dictionary mapping user_id to timezone name
            
        Returns:
            Datetime in the user's timezone
            
        Example:
            >>> utc = datetime(2026, 1, 27, 15, 0, 0, tzinfo=timezone.utc)
            >>> manager = UserTimezoneManager()
            >>> prefs = {"alice": "America/New_York"}
            >>> user_time = manager.convert_to_user_timezone(utc, "alice", prefs)
            >>> print(user_time)
            2026-01-27 10:00:00-05:00
        """
        # TODO: Fill in the blank
        # Step 1: Get the user's timezone using get_user_timezone()
        # Step 2: Convert utc_dt to that timezone using .astimezone()
        # Hint: Use the method you just wrote above
        return None  # Replace this line


# Test your solution:
if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 1: Handling Multiple Timezones")
    print("=" * 70)
    
    manager = UserTimezoneManager(default_timezone="UTC")
    user_prefs = {
        "alice": "America/New_York",
        "bob": "Europe/London",
        "charlie": "Asia/Tokyo",
    }
    
    sample_utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
    
    # Uncomment after implementing:
    # for user_id, expected_tz in user_prefs.items():
    #     user_time = manager.convert_to_user_timezone(sample_utc, user_id, user_prefs)
    #     print(f"{user_id:10} ({expected_tz:20}): {user_time}")
    
    print("\nExpected output:")
    print("alice      (America/New_York   ): 2026-01-27 10:30:00-05:00")
    print("bob        (Europe/London      ): 2026-01-27 15:30:00+00:00")
    print("charlie    (Asia/Tokyo         ): 2026-01-28 00:30:00+09:00")


# ============================================================================
# EXERCISE 2: Locale-Aware Date Formatting
# ============================================================================

"""
Tutorial: Locale-Aware Formatting
---------------------------------

Different locales have different date formats:
- US: "January 27, 2026" or "01/27/2026"
- UK: "27 January 2026" or "27/01/2026"
- Germany: "27. Januar 2026" or "27.01.2026"

Python's locale module provides locale-aware formatting, but it requires:
1. Setting the locale (can be system-dependent)
2. Using locale-specific format codes
3. Handling cases where locale isn't available

Alternative: Use babel library (more reliable, but external dependency)

Best Practice:
- For production, consider using babel for more reliable locale handling
- Always have a fallback format if locale setting fails
- Test with different locales to ensure your code works globally
"""


def format_date_locale(
    dt: datetime, 
    locale_name: str = "en_US", 
    format_style: str = "full"
) -> str:
    """
    Format a datetime using locale-aware formatting.
    
    Args:
        dt: Timezone-aware datetime
        locale_name: Locale string (e.g., 'en_US', 'de_DE', 'fr_FR')
        format_style: 'full', 'long', 'medium', or 'short'
        
    Returns:
        Locale-formatted date string
        
    Example:
        >>> dt = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
        >>> format_date_locale(dt, 'en_US', 'full')
        'Monday, January 27, 2026 at 3:30:00 PM UTC'
        >>> format_date_locale(dt, 'de_DE', 'long')
        '27. Januar 2026 um 15:30:00 UTC'
    """
    try:
        # TODO: Fill in the blank
        # Step 1: Set the locale using locale.setlocale()
        #   - Use locale.LC_TIME for date/time formatting
        #   - Pass locale_name as the second argument
        # Step 2: Use dt.strftime() with locale-aware format codes
        #   - For full: "%A, %B %d, %Y at %I:%M:%S %p %Z"
        #   - For long: "%B %d, %Y at %I:%M:%S %p %Z"
        #   - For medium: "%b %d, %Y %I:%M %p"
        #   - For short: "%m/%d/%Y %I:%M %p"
        # Hint: The format depends on format_style parameter
        
        # Set locale
        # TODO: Replace None with locale.setlocale() call
        locale.setlocale(locale.LC_TIME, None)  # Replace None
        
        # Choose format based on style
        # TODO: Implement format selection based on format_style
        format_string = ""  # Replace with appropriate format
        
        return dt.strftime(format_string)
        
    except locale.Error:
        # Fallback if locale not available
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def format_date_babel(dt: datetime, locale_name: str = "en_US") -> str:
    """
    Format a datetime using babel library (more reliable than locale module).
    
    This is a bonus exercise - babel provides better locale support.
    Install with: pip install babel
    
    Args:
        dt: Timezone-aware datetime
        locale_name: Locale string
        
    Returns:
        Formatted date string
    """
    try:
        from babel.dates import format_datetime
        
        # TODO: Fill in the blank (if you have babel installed)
        # Use format_datetime() from babel.dates
        # format_datetime(dt, locale=locale_name, format='full')
        return ""  # Replace this line
        
    except ImportError:
        return f"Babel not installed. Install with: pip install babel\nFallback: {dt.isoformat()}"


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 2: Locale-Aware Date Formatting")
    print("=" * 70)
    
    sample_utc = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
    
    # Note: Locale availability depends on system
    # Uncomment after implementing:
    # print("US English (full):", format_date_locale(sample_utc, 'en_US', 'full'))
    # print("US English (short):", format_date_locale(sample_utc, 'en_US', 'short'))
    # 
    # # Try German if available
    # try:
    #     print("German (long):", format_date_locale(sample_utc, 'de_DE', 'long'))
    # except:
    #     print("German locale not available on this system")
    
    print("\nExpected output (may vary by system):")
    print("US English (full): Monday, January 27, 2026 at 03:30:00 PM UTC")
    print("US English (short): 01/27/2026 03:30 PM")


# ============================================================================
# EXERCISE 3: Relative Time Display
# ============================================================================

"""
Tutorial: Relative Time Display
-------------------------------

Users often prefer relative time ("2 hours ago", "yesterday", "in 3 days")
over absolute timestamps. This is common in:
- Social media feeds
- Activity logs
- Notification timestamps
- Chat applications

Rules for relative time:
- < 1 minute: "just now"
- < 1 hour: "X minutes ago"
- < 24 hours: "X hours ago" or "today at HH:MM"
- Yesterday: "yesterday at HH:MM"
- < 7 days: "X days ago" or day name
- Older: Show actual date

Best Practice:
- Always calculate relative to UTC, then convert to user's timezone for display
- Handle edge cases (same second, future dates)
- Consider using libraries like 'humanize' or 'arrow' for production
"""


def format_relative_time(utc_dt: datetime, user_timezone: ZoneInfo) -> str:
    """
    Format a UTC datetime as relative time in the user's timezone.
    
    Args:
        utc_dt: Timezone-aware datetime in UTC
        user_timezone: User's timezone
        
    Returns:
        Relative time string (e.g., "2 hours ago", "yesterday at 3:30 PM")
        
    Example:
        >>> now_utc = datetime.now(timezone.utc)
        >>> two_hours_ago = now_utc - timedelta(hours=2)
        >>> format_relative_time(two_hours_ago, ZoneInfo('America/New_York'))
        '2 hours ago'
    """
    # TODO: Fill in the blanks
    # Step 1: Get current UTC time
    now_utc = datetime.now(timezone.utc)
    
    # Step 2: Convert both times to user's timezone
    # TODO: Convert utc_dt and now_utc to user_timezone
    user_dt = None  # Replace this line
    user_now = None  # Replace this line
    
    # Step 3: Calculate the difference
    # TODO: Calculate timedelta between user_now and user_dt
    delta = None  # Replace this line
    
    # Step 4: Determine the relative time string
    # TODO: Implement logic for:
    #   - Less than 1 minute: "just now"
    #   - Less than 1 hour: "X minutes ago"
    #   - Less than 24 hours: "X hours ago" or "today at HH:MM"
    #   - Yesterday: "yesterday at HH:MM"
    #   - Less than 7 days: "X days ago" or day name
    #   - Older: Use strftime with date
    
    # Hint: Check delta.total_seconds(), delta.days, etc.
    
    if delta.total_seconds() < 60:
        return "just now"
    elif delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    # TODO: Continue with hours, days, etc.
    else:
        # Fallback to formatted date
        return user_dt.strftime("%Y-%m-%d %H:%M")


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 3: Relative Time Display")
    print("=" * 70)
    
    now = datetime.now(timezone.utc)
    test_cases = [
        (now - timedelta(seconds=30), "just now"),
        (now - timedelta(minutes=5), "5 minutes ago"),
        (now - timedelta(hours=2), "2 hours ago"),
        (now - timedelta(days=1), "yesterday"),
        (now - timedelta(days=5), "5 days ago"),
    ]
    
    # Uncomment after implementing:
    # for dt, expected in test_cases:
    #     result = format_relative_time(dt, ZoneInfo('America/New_York'))
    #     print(f"{dt.isoformat()} -> {result}")
    
    print("\nExpected output (approximate):")
    print("2026-01-27T15:29:30+00:00 -> just now")
    print("2026-01-27T15:25:00+00:00 -> 5 minutes ago")
    print("2026-01-27T13:30:00+00:00 -> 2 hours ago")
    print("2026-01-26T15:30:00+00:00 -> yesterday at 10:30 AM")
    print("2026-01-22T15:30:00+00:00 -> 5 days ago")


# ============================================================================
# EXERCISE 4: Timezone-Aware Database Storage/Retrieval
# ============================================================================

"""
Tutorial: Database Storage Patterns
-----------------------------------

When storing datetimes in databases:
1. **Always store UTC** - Convert to UTC before saving
2. **Store as timezone-aware** - Include timezone info (or use UTC timestamp)
3. **Retrieve as UTC** - Database returns UTC, convert to user timezone for display

Common database patterns:
- PostgreSQL: TIMESTAMP WITH TIME ZONE (stores UTC, converts on insert/select)
- MongoDB: ISODate (stores as UTC)
- SQLite: TEXT (store ISO 8601 strings, or INTEGER (Unix timestamp))
- MySQL: DATETIME (naive) or TIMESTAMP (converts to UTC)

Best Practice:
- Use database-native UTC types when available
- If using TEXT, always use ISO 8601 format with timezone
- Never store local time in database
- Always convert to UTC before saving
"""


class DatabaseDateTimeHandler:
    """
    Handles datetime conversion for database storage and retrieval.
    """
    
    @staticmethod
    def prepare_for_storage(dt: datetime) -> str:
        """
        Convert a datetime to a format suitable for database storage.
        
        Always stores in UTC as ISO 8601 string.
        
        Args:
            dt: Timezone-aware datetime (any timezone)
            
        Returns:
            ISO 8601 string in UTC
            
        Example:
            >>> ny_dt = datetime(2026, 1, 27, 10, 0, 0, tzinfo=ZoneInfo('America/New_York'))
            >>> DatabaseDateTimeHandler.prepare_for_storage(ny_dt)
            '2026-01-27T15:00:00+00:00'
        """
        # TODO: Fill in the blank
        # Step 1: Ensure dt is timezone-aware (raise error if naive)
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware for storage")
        
        # Step 2: Convert to UTC
        # TODO: Convert dt to UTC
        utc_dt = None  # Replace this line
        
        # Step 3: Return ISO format string
        # TODO: Return isoformat() of utc_dt
        return ""  # Replace this line
    
    @staticmethod
    def parse_from_storage(stored_string: str) -> datetime:
        """
        Parse a datetime string from database storage.
        
        Assumes the string is in UTC (ISO 8601 format).
        
        Args:
            stored_string: ISO 8601 string from database
            
        Returns:
            Timezone-aware datetime in UTC
            
        Example:
            >>> DatabaseDateTimeHandler.parse_from_storage('2026-01-27T15:00:00+00:00')
            datetime.datetime(2026, 1, 27, 15, 0, tzinfo=timezone.utc)
        """
        # TODO: Fill in the blank
        # Step 1: Parse the ISO string
        # TODO: Use fromisoformat() and handle 'Z' suffix
        normalized = stored_string.replace("Z", "+00:00")
        dt = None  # Replace this line
        
        # Step 2: Ensure it's UTC
        # TODO: Convert to UTC if not already
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        
        return dt
    
    @staticmethod
    def format_for_display(
        stored_string: str, 
        user_timezone: ZoneInfo,
        format_string: str = "%Y-%m-%d %H:%M:%S %Z"
    ) -> str:
        """
        Retrieve from storage and format for user display.
        
        Args:
            stored_string: ISO 8601 string from database (UTC)
            user_timezone: User's timezone
            format_string: strftime format string
            
        Returns:
            Formatted string in user's timezone
            
        Example:
            >>> DatabaseDateTimeHandler.format_for_display(
            ...     '2026-01-27T15:00:00+00:00',
            ...     ZoneInfo('America/New_York')
            ... )
            '2026-01-27 10:00:00 EST'
        """
        # TODO: Fill in the blank
        # Step 1: Parse from storage (returns UTC)
        utc_dt = None  # Replace this line (use parse_from_storage)
        
        # Step 2: Convert to user timezone
        user_dt = None  # Replace this line
        
        # Step 3: Format for display
        return ""  # Replace this line (use strftime)


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 4: Database Storage/Retrieval")
    print("=" * 70)
    
    # Simulate storing a datetime
    ny_dt = datetime(2026, 1, 27, 10, 0, 0, tzinfo=ZoneInfo('America/New_York'))
    
    # Uncomment after implementing:
    # stored = DatabaseDateTimeHandler.prepare_for_storage(ny_dt)
    # print(f"Original (NY):  {ny_dt}")
    # print(f"Stored (UTC):   {stored}")
    # 
    # retrieved = DatabaseDateTimeHandler.parse_from_storage(stored)
    # print(f"Retrieved (UTC): {retrieved}")
    # 
    # displayed = DatabaseDateTimeHandler.format_for_display(
    #     stored, 
    #     ZoneInfo('America/New_York')
    # )
    # print(f"Displayed (NY):  {displayed}")
    
    print("\nExpected output:")
    print("Original (NY):  2026-01-27 10:00:00-05:00")
    print("Stored (UTC):   2026-01-27T15:00:00+00:00")
    print("Retrieved (UTC): 2026-01-27 15:00:00+00:00")
    print("Displayed (NY):  2026-01-27 10:00:00 EST")


# ============================================================================
# SUMMARY: Key Takeaways
# ============================================================================

"""
Congratulations! You've completed the medium exercises. Here's what you learned:

✅ Handle multiple user timezones with a preference system
✅ Format dates according to user's locale
✅ Display relative time ("2 hours ago", "yesterday")
✅ Properly store and retrieve datetimes from databases (always UTC)

Advanced Topics Covered:
- User preference management for timezones
- Locale-aware formatting (locale module and babel)
- Relative time calculations
- Database storage patterns (UTC storage, local display)

Next Steps:
- Move to advanced.py for production patterns and edge cases
- Learn about DST transitions and ambiguous times
- Practice with API design and scheduled tasks
- Learn about testing datetime code

Remember:
    STORE UTC IN DATABASE
    CONVERT TO USER TIMEZONE FOR DISPLAY
    HANDLE LOCALE FOR FORMATTING
"""
