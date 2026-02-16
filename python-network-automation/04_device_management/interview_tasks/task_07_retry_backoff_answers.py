"""
Task 07: Retry with exponential backoff — full solution.
Assume Netmiko is installed; device_info is provided.
"""

import logging
import time
from typing import Any, Callable, Dict, Optional

from netmiko import ConnectHandler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def connect_to_device(device_info: Dict[str, str]) -> Any:
    """Connect to device via Netmiko."""
    return ConnectHandler(**device_info)


def run_with_retry(
    device_info: Dict[str, str],
    operation: Callable[[Any], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:
    """Connect, run operation(conn), retry on ConnectionError/TimeoutError with backoff."""
    last_exc: Optional[Exception] = None
    conn = None
    for attempt in range(max_attempts):
        try:
            conn = connect_to_device(device_info)
            return operation(conn)
        except (ConnectionError, TimeoutError, OSError) as e:
            last_exc = e
            if attempt < max_attempts - 1:
                delay = min(base_delay * (2 ** attempt), 30.0)
                time.sleep(delay)
        finally:
            if conn is not None and hasattr(conn, "disconnect"):
                try:
                    conn.disconnect()
                except Exception:
                    pass
            conn = None
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("Max retries exceeded")


def main() -> None:
    device_info = {
        "host": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }

    def op(conn: Any) -> str:
        return conn.send_command("show version")

    result = run_with_retry(device_info, op, max_attempts=2)
    logger.info("Result length: %s", len(result))
    print("Done.")


if __name__ == "__main__":
    main()
