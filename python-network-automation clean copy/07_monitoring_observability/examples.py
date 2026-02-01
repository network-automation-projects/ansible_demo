"""
Python Network Automation - Monitoring & Observability Examples
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AutomationLogger:
    """Structured logging for automation."""
    
    def log_operation(self, operation: str, device: str, success: bool, details: Dict[str, Any] = None):
        """Log automation operation."""
        if success:
            logger.info(f"Operation {operation} on {device} succeeded", extra=details or {})
        else:
            logger.error(f"Operation {operation} on {device} failed", extra=details or {})


class TimestampManager:
    """Manage timestamps with timezone awareness."""
    
    @staticmethod
    def now_utc() -> datetime:
        """Get current UTC time."""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def format_timestamp(dt: datetime) -> str:
        """Format timestamp as ISO string."""
        return dt.isoformat()


if __name__ == "__main__":
    print("Monitoring & Observability Examples")
    logger.info("Test log message")
    ts = TimestampManager.now_utc()
    print(f"Current UTC: {ts.isoformat()}")
