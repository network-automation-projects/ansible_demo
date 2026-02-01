"""
Python Dates Exercise - Advanced Level
========================================

This file covers production-ready patterns and real-world scenarios:
- API response formatting (REST API best practices)
- Scheduled task timezone handling (cron jobs, background tasks)
- Date range queries across timezones
- Event logging with proper timezone context
- Handling edge cases (DST transitions, ambiguous times)

Prerequisites:
- You should understand UTC storage, timezone conversion, and formatting
- Familiarity with API design and database queries
"""

from datetime import datetime, timezone, timedelta, date
from typing import Optional, Dict, List, Tuple
import json

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


# ============================================================================
# EXERCISE 1: API Response Formatting
# ============================================================================

"""
Tutorial: API Design Best Practices
------------------------------------

When designing REST APIs that return dates:
1. **Always return UTC** - Clients can convert to their timezone
2. **Use ISO 8601 format** - Standard, unambiguous, includes timezone
3. **Include timezone offset** - Even if UTC, show "+00:00" for clarity
4. **Be consistent** - All datetime fields use the same format

Common patterns:
- Single datetime: "2026-01-27T15:30:00+00:00"
- With microseconds: "2026-01-27T15:30:00.123456+00:00"
- Date only: "2026-01-27" (no time component)

Best Practice:
- Never return naive datetimes (always include timezone)
- Always use UTC internally, convert only for display if needed
- Document your API's datetime format in API docs
"""


class APIDateTimeFormatter:
    """
    Formats datetimes for API responses following best practices.
    """
    
    @staticmethod
    def format_for_api_response(dt: datetime, include_microseconds: bool = False) -> str:
        """
        Format a datetime for API response (always UTC, ISO 8601).
        
        Args:
            dt: Timezone-aware datetime (any timezone, will be converted to UTC)
            include_microseconds: Whether to include microseconds in output
            
        Returns:
            ISO 8601 string in UTC
            
        Example:
            >>> ny_dt = datetime(2026, 1, 27, 10, 0, 0, tzinfo=ZoneInfo('America/New_York'))
            >>> APIDateTimeFormatter.format_for_api_response(ny_dt)
            '2026-01-27T15:00:00+00:00'
        """
        # TODO: Fill in the blank
        # Step 1: Ensure dt is timezone-aware
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware for API response")
        
        # Step 2: Convert to UTC
        # TODO: Convert dt to UTC
        utc_dt = None  # Replace this line
        
        # Step 3: Format as ISO 8601
        # TODO: Use isoformat(), optionally removing microseconds
        if not include_microseconds and utc_dt.microsecond:
            # Remove microseconds by replacing with 0
            utc_dt = utc_dt.replace(microsecond=0)
        
        return ""  # Replace this line (use isoformat())
    
    @staticmethod
    def create_api_response(data: Dict, timestamp_field: str = "timestamp") -> Dict:
        """
        Create a standardized API response with UTC timestamp.
        
        Args:
            data: Dictionary of response data
            timestamp_field: Name of the timestamp field to add
            
        Returns:
            Dictionary with added UTC timestamp field
            
        Example:
            >>> response = APIDateTimeFormatter.create_api_response({"user": "alice"})
            >>> print(response["timestamp"])
            2026-01-27T15:30:00+00:00
        """
        # TODO: Fill in the blank
        # Step 1: Get current UTC time
        now_utc = None  # Replace this line
        
        # Step 2: Format it for API
        formatted_time = None  # Replace this line (use format_for_api_response)
        
        # Step 3: Add to data dictionary
        result = data.copy()
        result[timestamp_field] = formatted_time
        
        return result


# Test your solution:
if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 1: API Response Formatting")
    print("=" * 70)
    
    ny_dt = datetime(2026, 1, 27, 10, 0, 0, tzinfo=ZoneInfo('America/New_York'))
    
    # Uncomment after implementing:
    # api_time = APIDateTimeFormatter.format_for_api_response(ny_dt)
    # print(f"API response time: {api_time}")
    # 
    # response = APIDateTimeFormatter.create_api_response({"status": "success", "data": {}})
    # print(f"API response: {json.dumps(response, indent=2)}")
    
    print("\nExpected output:")
    print("API response time: 2026-01-27T15:00:00+00:00")
    print('API response: {')
    print('  "status": "success",')
    print('  "data": {},')
    print('  "timestamp": "2026-01-27T15:30:00+00:00"')
    print('}')


# ============================================================================
# EXERCISE 2: Scheduled Task Timezone Handling
# ============================================================================

"""
Tutorial: Scheduled Tasks and Cron Jobs
---------------------------------------

Scheduled tasks (cron jobs, background workers) often need to run at specific
times in specific timezones. Common scenarios:
- "Run daily at 9 AM Eastern Time"
- "Send email every Monday at 8 AM in user's timezone"
- "Generate report at midnight UTC"

Key considerations:
1. **Server timezone** - Servers often run in UTC, but tasks may need other timezones
2. **DST transitions** - Times can be ambiguous or non-existent (spring forward, fall back)
3. **User timezones** - Tasks for users should run in their timezone

Best Practice:
- Store scheduled times in UTC in your database
- Convert to target timezone only when checking "should run now?"
- Handle DST transitions explicitly
- Use libraries like APScheduler or Celery for complex scheduling
"""


class ScheduledTaskManager:
    """
    Manages scheduled tasks with timezone awareness.
    """
    
    @staticmethod
    def should_run_now(
        scheduled_time_utc: datetime,
        current_time_utc: Optional[datetime] = None
    ) -> bool:
        """
        Check if a scheduled task should run now.
        
        Args:
            scheduled_time_utc: When the task is scheduled (UTC)
            current_time_utc: Current time (UTC), defaults to now()
            
        Returns:
            True if current time is >= scheduled time
            
        Example:
            >>> scheduled = datetime(2026, 1, 27, 15, 0, 0, tzinfo=timezone.utc)
            >>> now = datetime(2026, 1, 27, 15, 30, 0, tzinfo=timezone.utc)
            >>> ScheduledTaskManager.should_run_now(scheduled, now)
            True
        """
        # TODO: Fill in the blank
        if current_time_utc is None:
            current_time_utc = datetime.now(timezone.utc)
        
        # TODO: Compare times (ensure both are UTC and timezone-aware)
        # Return True if current_time_utc >= scheduled_time_utc
        return False  # Replace this line
    
    @staticmethod
    def convert_scheduled_time_to_utc(
        local_time: str,
        timezone_name: str,
        target_date: Optional[date] = None
    ) -> datetime:
        """
        Convert a local time string to UTC for scheduling.
        
        Args:
            local_time: Time string in "HH:MM" format
            timezone_name: IANA timezone name
            target_date: Date to schedule for (defaults to today in that timezone)
            
        Returns:
            UTC datetime when that local time occurs
            
        Example:
            >>> ScheduledTaskManager.convert_scheduled_time_to_utc("09:00", "America/New_York")
            datetime.datetime(2026, 1, 27, 14, 0, tzinfo=timezone.utc)  # 9 AM EST = 2 PM UTC
        """
        # TODO: Fill in the blank
        # Step 1: Parse local_time (HH:MM format)
        hour, minute = map(int, local_time.split(":"))
        
        # Step 2: Get target date in the specified timezone
        if target_date is None:
            # Get today's date in the target timezone
            tz = ZoneInfo(timezone_name)
            now_in_tz = datetime.now(tz)
            target_date = now_in_tz.date()
        
        # Step 3: Create datetime in the target timezone
        # TODO: Create datetime with target_date, hour, minute, and timezone
        local_dt = None  # Replace this line
        
        # Step 4: Convert to UTC
        # TODO: Convert local_dt to UTC
        utc_dt = None  # Replace this line
        
        return utc_dt
    
    @staticmethod
    def handle_dst_transition(
        local_time: str,
        timezone_name: str,
        target_date: date
    ) -> Tuple[datetime, str]:
        """
        Handle DST transitions (ambiguous or non-existent times).
        
        Returns the UTC time and a note about the transition.
        
        Args:
            local_time: Time string in "HH:MM" format
            timezone_name: IANA timezone name
            target_date: Date to check
            
        Returns:
            Tuple of (UTC datetime, transition_note)
            transition_note: "normal", "ambiguous", or "non_existent"
            
        Example:
            During DST fall back, 1:30 AM occurs twice (ambiguous)
            During DST spring forward, 2:30 AM doesn't exist (non-existent)
        """
        # TODO: Fill in the blank (advanced)
        # This is a complex exercise - DST handling requires checking
        # if the time exists and is unique in the target timezone
        
        # Step 1: Try to create the datetime
        try:
            hour, minute = map(int, local_time.split(":"))
            tz = ZoneInfo(timezone_name)
            local_dt = datetime(target_date.year, target_date.month, target_date.day, 
                              hour, minute, tzinfo=tz)
            
            # Step 2: Check if time is ambiguous (occurs twice due to DST fall back)
            # Hint: Try creating the datetime, then check if there are multiple UTC equivalents
            # This is complex - for now, just convert and note if it's during DST transition period
            
            utc_dt = local_dt.astimezone(timezone.utc)
            note = "normal"
            
            # TODO: Implement proper DST transition detection
            # (This is advanced - you'd need to check the timezone's DST rules)
            
            return utc_dt, note
            
        except Exception as e:
            # Handle non-existent time (spring forward)
            return datetime.now(timezone.utc), "non_existent"


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 2: Scheduled Task Timezone Handling")
    print("=" * 70)
    
    # Uncomment after implementing:
    # # Schedule a task for 9 AM Eastern Time
    # utc_scheduled = ScheduledTaskManager.convert_scheduled_time_to_utc(
    #     "09:00", 
    #     "America/New_York"
    # )
    # print(f"9 AM Eastern = {utc_scheduled} UTC")
    # 
    # # Check if it should run
    # should_run = ScheduledTaskManager.should_run_now(utc_scheduled)
    # print(f"Should run now? {should_run}")
    
    print("\nExpected output:")
    print("9 AM Eastern = 2026-01-27 14:00:00+00:00 UTC")
    print("Should run now? True (if current time >= scheduled time)")


# ============================================================================
# EXERCISE 3: Date Range Queries Across Timezones
# ============================================================================

"""
Tutorial: Date Range Queries
-----------------------------

When users query for data in a date range, they think in their local timezone:
- "Show me all events on January 27" (in their timezone)
- "Get orders from last week" (week boundaries in their timezone)

But your database stores UTC. You need to:
1. Convert user's date range to UTC range
2. Query database with UTC range
3. Return results, converting back to user's timezone for display

Common pitfalls:
- User says "January 27" but means "January 27 in my timezone"
- "Today" means different things in different timezones
- Date boundaries shift when converting to UTC

Best Practice:
- Always convert user's local date range to UTC range before querying
- Be explicit about what "today" means (in which timezone)
- Handle date boundaries carefully (start of day, end of day)
"""


class DateRangeQueryBuilder:
    """
    Builds UTC date ranges from user's local date queries.
    """
    
    @staticmethod
    def local_date_to_utc_range(
        local_date: date,
        user_timezone: ZoneInfo
    ) -> Tuple[datetime, datetime]:
        """
        Convert a local date to UTC datetime range (start and end of day).
        
        Args:
            local_date: Date in user's timezone
            user_timezone: User's timezone
            
        Returns:
            Tuple of (start_utc, end_utc) covering the entire day in user's timezone
            
        Example:
            >>> DateRangeQueryBuilder.local_date_to_utc_range(
            ...     date(2026, 1, 27),
            ...     ZoneInfo('America/New_York')
            ... )
            (datetime(2026, 1, 27, 5, 0, tzinfo=timezone.utc),  # Start of day EST
             datetime(2026, 1, 28, 4, 59, 59, tzinfo=timezone.utc))  # End of day EST
        """
        # TODO: Fill in the blank
        # Step 1: Create start of day in user's timezone (00:00:00)
        # TODO: Create datetime at midnight in user_timezone
        start_local = None  # Replace this line
        
        # Step 2: Create end of day in user's timezone (23:59:59.999999)
        # TODO: Create datetime at end of day in user_timezone
        end_local = None  # Replace this line
        
        # Step 3: Convert both to UTC
        start_utc = None  # Replace this line
        end_utc = None  # Replace this line
        
        return start_utc, end_utc
    
    @staticmethod
    def build_query_for_date_range(
        start_date: date,
        end_date: date,
        user_timezone: ZoneInfo
    ) -> Dict[str, datetime]:
        """
        Build a database query filter for a date range in user's timezone.
        
        Args:
            start_date: Start date (inclusive) in user's timezone
            end_date: End date (inclusive) in user's timezone
            user_timezone: User's timezone
            
        Returns:
            Dictionary with 'start' and 'end' UTC datetimes for database query
            
        Example:
            >>> query = DateRangeQueryBuilder.build_query_for_date_range(
            ...     date(2026, 1, 27),
            ...     date(2026, 1, 28),
            ...     ZoneInfo('America/New_York')
            ... )
            >>> # Use query['start'] and query['end'] in database WHERE clause
        """
        # TODO: Fill in the blank
        # Step 1: Get UTC range for start date (start of day)
        start_utc, _ = None  # Replace this line (use local_date_to_utc_range)
        
        # Step 2: Get UTC range for end date (end of day)
        _, end_utc = None  # Replace this line (use local_date_to_utc_range)
        
        return {
            "start": start_utc,
            "end": end_utc
        }
    
    @staticmethod
    def get_today_range(user_timezone: ZoneInfo) -> Tuple[datetime, datetime]:
        """
        Get UTC range for "today" in user's timezone.
        
        Args:
            user_timezone: User's timezone
            
        Returns:
            Tuple of (start_utc, end_utc) for today in user's timezone
        """
        # TODO: Fill in the blank
        # Step 1: Get today's date in user's timezone
        now_in_tz = None  # Replace this line (datetime.now() in user_timezone)
        today = None  # Replace this line (extract date)
        
        # Step 2: Convert to UTC range
        return None  # Replace this line (use local_date_to_utc_range)


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 3: Date Range Queries Across Timezones")
    print("=" * 70)
    
    # Uncomment after implementing:
    # start_utc, end_utc = DateRangeQueryBuilder.local_date_to_utc_range(
    #     date(2026, 1, 27),
    #     ZoneInfo('America/New_York')
    # )
    # print(f"January 27, 2026 in New York:")
    # print(f"  Start (UTC): {start_utc}")
    # print(f"  End (UTC):   {end_utc}")
    # 
    # query = DateRangeQueryBuilder.build_query_for_date_range(
    #     date(2026, 1, 27),
    #     date(2026, 1, 28),
    #     ZoneInfo('America/New_York')
    # )
    # print(f"\nQuery range: {query['start']} to {query['end']}")
    
    print("\nExpected output:")
    print("January 27, 2026 in New York:")
    print("  Start (UTC): 2026-01-27 05:00:00+00:00")
    print("  End (UTC):   2026-01-28 04:59:59.999999+00:00")


# ============================================================================
# EXERCISE 4: Event Logging with Timezone Context
# ============================================================================

"""
Tutorial: Logging with Timezone Context
---------------------------------------

When logging events, you need to:
1. **Log in UTC** - Consistent across all servers and timezones
2. **Include timezone info** - Make it clear the time is UTC
3. **Store user context** - If relevant, log user's timezone for debugging
4. **Use structured logging** - JSON format with explicit timezone fields

Best Practice:
- Always log timestamps in UTC with explicit timezone indicator
- Include both UTC and user's local time if user action triggered the log
- Use ISO 8601 format for log timestamps
- Make logs searchable and parseable
"""


class TimezoneAwareLogger:
    """
    Logger that includes proper timezone context in log entries.
    """
    
    @staticmethod
    def create_log_entry(
        event_type: str,
        message: str,
        user_id: Optional[str] = None,
        user_timezone: Optional[ZoneInfo] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a structured log entry with timezone context.
        
        Args:
            event_type: Type of event (e.g., "user_login", "order_created")
            message: Log message
            user_id: Optional user identifier
            user_timezone: Optional user timezone (for user-triggered events)
            metadata: Optional additional metadata
            
        Returns:
            Dictionary with structured log data
            
        Example:
            >>> log = TimezoneAwareLogger.create_log_entry(
            ...     "user_login",
            ...     "User logged in",
            ...     user_id="alice",
            ...     user_timezone=ZoneInfo('America/New_York')
            ... )
            >>> print(json.dumps(log, indent=2))
        """
        # TODO: Fill in the blank
        # Step 1: Get current UTC time
        utc_now = None  # Replace this line
        
        # Step 2: Format UTC time for logging
        utc_timestamp = None  # Replace this line (use isoformat())
        
        # Step 3: Build log entry
        log_entry = {
            "timestamp_utc": utc_timestamp,
            "timezone": "UTC",
            "event_type": event_type,
            "message": message,
        }
        
        # Step 4: Add user context if provided
        if user_id:
            log_entry["user_id"] = user_id
        
        if user_timezone:
            # TODO: Add user's local time for context
            user_local_time = None  # Replace this line (convert utc_now to user_timezone)
            log_entry["user_timezone"] = str(user_timezone)
            log_entry["user_local_time"] = None  # Replace this line (format user_local_time)
        
        # Step 5: Add metadata if provided
        if metadata:
            log_entry["metadata"] = metadata
        
        return log_entry
    
    @staticmethod
    def log_event(
        event_type: str,
        message: str,
        user_id: Optional[str] = None,
        user_timezone: Optional[ZoneInfo] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Log an event (prints to console, but in production would write to log file).
        
        Args:
            Same as create_log_entry()
        """
        log_entry = TimezoneAwareLogger.create_log_entry(
            event_type, message, user_id, user_timezone, metadata
        )
        # In production, you'd write to a log file or logging service
        print(json.dumps(log_entry, indent=2, default=str))


# Test your solution:
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXERCISE 4: Event Logging with Timezone Context")
    print("=" * 70)
    
    # Uncomment after implementing:
    # TimezoneAwareLogger.log_event(
    #     "user_action",
    #     "User created order",
    #     user_id="alice",
    #     user_timezone=ZoneInfo('America/New_York'),
    #     metadata={"order_id": "12345", "amount": 99.99}
    # )
    
    print("\nExpected output (JSON):")
    print("{")
    print('  "timestamp_utc": "2026-01-27T15:30:00+00:00",')
    print('  "timezone": "UTC",')
    print('  "event_type": "user_action",')
    print('  "message": "User created order",')
    print('  "user_id": "alice",')
    print('  "user_timezone": "America/New_York",')
    print('  "user_local_time": "2026-01-27T10:30:00-05:00",')
    print('  "metadata": {')
    print('    "order_id": "12345",')
    print('    "amount": 99.99')
    print('  }')
    print('}')


# ============================================================================
# BONUS: Edge Cases and Gotchas
# ============================================================================

"""
Common Edge Cases and How to Handle Them
----------------------------------------

1. **DST Spring Forward (Non-existent time)**
   - Example: 2:30 AM doesn't exist on DST transition day
   - Solution: Use `fold` parameter or handle exception, adjust to next valid time

2. **DST Fall Back (Ambiguous time)**
   - Example: 1:30 AM occurs twice (before and after DST change)
   - Solution: Use `fold=0` for first occurrence, `fold=1` for second

3. **Leap Seconds**
   - Rare, but can cause issues with precise timing
   - Solution: Most applications can ignore, but be aware for high-precision systems

4. **Timezone Database Updates**
   - Timezone rules change (countries change DST rules)
   - Solution: Keep timezone database updated, use system's zoneinfo

5. **Server Timezone Mismatch**
   - Server might not be in UTC
   - Solution: Always explicitly use UTC, never rely on server's default timezone

6. **Date Arithmetic Across DST**
   - Adding 24 hours might not give you "tomorrow at same time" due to DST
   - Solution: Use date arithmetic, then set time, or use timedelta carefully

Best Practice Summary:
- Always use UTC for storage and internal operations
- Convert to user timezone only for display
- Use timezone-aware datetimes everywhere
- Handle DST transitions explicitly when scheduling
- Test with different timezones and DST transition dates
- Document your timezone assumptions
"""


# ============================================================================
# SUMMARY: Key Takeaways
# ============================================================================

"""
Congratulations! You've completed the advanced exercises. Here's what you learned:

✅ Format datetimes for API responses (UTC, ISO 8601)
✅ Handle scheduled tasks with timezone awareness
✅ Build date range queries that work across timezones
✅ Create structured logs with proper timezone context
✅ Understand edge cases (DST, ambiguous times, leap seconds)

Production Patterns Covered:
- API design with UTC timestamps
- Scheduled task timezone handling
- Database query patterns for date ranges
- Structured logging with timezone context
- Edge case handling (DST transitions)

Final Checklist for Production Code:
□ Always store UTC in database
□ Always use timezone-aware datetimes
□ Convert to user timezone only for display
□ Use ISO 8601 format for APIs
□ Handle DST transitions explicitly
□ Test with multiple timezones
□ Document timezone assumptions
□ Keep timezone database updated

Remember the golden rules:
    STORE UTC
    DISPLAY LOCAL
    BE EXPLICIT ABOUT TIMEZONES
    HANDLE EDGE CASES
"""
