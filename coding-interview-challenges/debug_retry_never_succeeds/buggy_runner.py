"""
Buggy device runner with retry-with-backoff.

The task fails the first 2 attempts and succeeds on the 3rd.
Yet this runner always reports failure. Why?
"""

import time
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Simulates a task that fails twice, then succeeds
_call_count = 0


def run_task(device: str) -> str:
    """Simulated task: fails twice, succeeds on 3rd call."""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ConnectionError(f"Simulated failure (call #{_call_count})")
    return "ok"


def run_with_retry(
    device: str,
    max_attempts: int = 3,
    base_delay: float = 0.1,
    backoff_multiplier: float = 2.0,
) -> str | None:
    """
    Run task on device with retry and exponential backoff.
    Returns result on success, None on failure.
    """
    last_error = None

    for attempt in range(1, max_attempts + 1):
        logger.info(f"Attempt {attempt}/{max_attempts} for {device}")

        try:
            result = run_task(device)
            logger.info(f"Success for {device} on attempt {attempt}")
            return result
        except ConnectionError as e:
            last_error = e
            logger.warning(f"Attempt {attempt} failed: {e}")

        if attempt < max_attempts:
            delay = base_delay * (backoff_multiplier ** (attempt - 1))
            logger.info(f"Waiting {delay:.2f}s before retry...")
            time.sleep(delay)
        return None

    return None


def main() -> None:
    result = run_with_retry("router-1", max_attempts=3)
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED: Task did not succeed after retries")


if __name__ == "__main__":
    main()
