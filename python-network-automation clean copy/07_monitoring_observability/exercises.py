"""
Python Network Automation - Monitoring & Observability Exercises
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In production: from prometheus_client import Counter, Gauge
# from dateutil import parser


def setup_logging(log_file: str, level: str = 'INFO') -> None:
    """Configure logging to file and console."""
    # TODO: Use logging.basicConfig() with file and format
    pass


def log_device_operation(device_name: str, operation: str, success: bool) -> None:
    """Log device operation with appropriate level."""
    # TODO: Use logger.info() for success, logger.error() for failure
    pass


def create_utc_timestamp() -> datetime:
    """Create UTC timestamp."""
    # TODO: Use datetime.now(timezone.utc)
    pass


def calculate_uptime(start_time: datetime, end_time: datetime) -> timedelta:
    """Calculate uptime duration."""
    # TODO: Use end_time - start_time
    pass


def create_metric_counter(name: str, description: str):
    """Create Prometheus counter metric."""
    # TODO: Use Counter(name, description)
    # return Counter(name, description)
    pass


if __name__ == "__main__":
    print("Monitoring & Observability Exercises")
