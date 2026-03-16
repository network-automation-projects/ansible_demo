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
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )


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
    print("Monitoring & Observability Exercises")
