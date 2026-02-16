"""
INTERVIEW PROMPT (about 30 min)
-------------------------------
Implement a function that connects to a device (Netmiko), runs an operation
(callable that takes the connection and returns a value), and retries on
ConnectionError or TimeoutError with exponential backoff. Disconnect after each
attempt (success or failure). Assume Netmiko is installed; device_info is
provided.
"""

import logging
import time
from typing import Any, Callable, Dict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

from netmiko import ConnectHandler


# --- Step 1: I'm going to connect and run the operation, and catch connection/timeout errors. ---
# --- Step 2: Next I'm going to retry with exponential backoff and disconnect after each attempt. ---
def run_with_retry(
    device_info: Dict[str, str],
    operation: Callable[[Any], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:
    """Connect, run operation(conn), retry on ConnectionError/TimeoutError with backoff."""
    # TODO: loop for attempt in range(max_attempts): try connect_to_device(device_info), operation(conn), return result
    # TODO: except (ConnectionError, TimeoutError, OSError): sleep base_delay * 2**attempt; finally disconnect
    raise NotImplementedError("Step 1–2: retry loop with exponential backoff, disconnect in finally")


# --- Step 3: main() — run a simple operation (e.g. send_command) with retry; device_info provided. ---
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
