"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from prometheus_client import Counter

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

_metric_cache: dict = {}

def create_metric_counter(name: str, description: str):
    """Get or create a Prometheus counter (created once per name)."""
    if name not in _metric_cache:
        _metric_cache[name] = Counter(name, description)
    return _metric_cache[name]


def main() -> None:
    """Demonstrate monitoring/observability helpers in action."""
    log_path = Path(__file__).parent / "monitoring_demo.log"
    setup_logging(str(log_path), level="INFO")
    logger.info("Demo started")

    # Device operations (success and failure)
    log_device_operation("router-01", "config backup", success=True)
    log_device_operation("switch-02", "firmware upgrade", success=False)

    # UTC timestamps and uptime
    start = create_utc_timestamp()
    # Simulate some work (e.g. a short "operation")
    end = create_utc_timestamp()
    uptime = calculate_uptime(start, end)
    logger.info("Uptime sample: %s", uptime)

    # Prometheus counter (optional; skip if not installed)
    try:
        counter = create_metric_counter(
            "device_operations_total",
            "Total number of device operations",
        )
        counter.inc(3)
        logger.info("Metric counter created and incremented")
    except ImportError:
        logger.info("prometheus_client not installed; skipping metric demo")

    logger.info("Demo finished – check %s for log output", log_path)
    print("Done. See", log_path, "for log output.")


if __name__ == "__main__":
    main()
