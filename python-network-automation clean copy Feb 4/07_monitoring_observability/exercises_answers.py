"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_logging(log_file: str, level: str = 'INFO') -> None:
    """Configure logging to file and console."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )


def log_device_operation(device_name: str, operation: str, success: bool) -> None:
    """Log device operation with appropriate level."""
    if success:
        logger.info("Device %s: %s succeeded", device_name, operation)
    else:
        logger.error("Device %s: %s failed", device_name, operation)


def create_utc_timestamp() -> datetime:
    """Create UTC timestamp."""
    return datetime.now(timezone.utc)


def calculate_uptime(start_time: datetime, end_time: datetime) -> timedelta:
    """Calculate uptime duration."""
    return end_time - start_time


def create_metric_counter(name: str, description: str):
    """Create Prometheus counter metric (requires prometheus_client)."""
    from prometheus_client import Counter
    return Counter(name, description)


if __name__ == "__main__":
    print("07_monitoring_observability – answer key (run exercises.py to practice)")
