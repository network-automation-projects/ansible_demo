"""
Python Network Automation - Error Handling Exercises
=====================================================

Fill-in-the-blank exercises for learning exception handling
in the context of network automation.
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXERCISE 1: Catch FileNotFoundError and return empty dict
# ============================================================================

"""
Tutorial: Catching specific exceptions
--------------------------------------

Use try/except to handle expected failures. Catch specific exception types
(e.g. FileNotFoundError, json.JSONDecodeError) so you only handle what you
intend. Always log when you catch; never swallow silently.

In network automation:
- Missing config or inventory file → catch FileNotFoundError, return default or exit with message.
- Invalid JSON → catch json.JSONDecodeError, log and return empty dict or re-raise.
"""


def load_inventory(path: Path) -> Dict[str, Any]:
    """
    Load a JSON inventory from path. If the file does not exist, log a warning
    and return an empty dict. If the file exists but is invalid JSON, log an
    error and return an empty dict.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed dict or {} on missing file or invalid JSON.
    """
    # TODO: Use try/except to catch FileNotFoundError when calling path.read_text().
    #       On FileNotFoundError, log with logger.warning and return {}.
    # TODO: Use a second try/except (or nested) to catch json.JSONDecodeError
    #       when calling json.loads(text). On JSONDecodeError, log with logger.error and return {}.
    #       Remember to use path.read_text(encoding="utf-8").
    return {}  # Replace with your implementation


# ============================================================================
# EXERCISE 2: Per-device handling — append failures to a list
# ============================================================================

"""
Tutorial: Per-device (or per-item) exception handling
-----------------------------------------------------

When processing multiple devices in a loop, wrap the work for each device
in try/except inside the loop. On exception, log and record that device
as failed (e.g. append to a failed list), then continue. One failing device
should not stop the whole batch.
"""


def run_on_devices(
    hostnames: List[str],
    run_fn: Callable[[str], Any],
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    For each hostname, call run_fn(hostname). Collect successful hostnames
    in ok_list and failures as (hostname, error_message) in failed_list.

    Args:
        hostnames: List of device hostnames.
        run_fn: Callable that takes one hostname; may raise OSError or others.

    Returns:
        (ok_list, failed_list) where failed_list is [(hostname, str(exception)), ...].
    """
    ok_list: List[str] = []
    failed_list: List[Tuple[str, str]] = []

    for hostname in hostnames:
        # TODO: try: run_fn(hostname); on success append hostname to ok_list.
        # TODO: except OSError as e: log with logger.warning, append (hostname, str(e)) to failed_list.
        # TODO: except Exception as e: log with logger.error, append (hostname, str(e)) to failed_list.
        pass  # Replace with your implementation

    return (ok_list, failed_list)


# ============================================================================
# EXERCISE 3: Log and re-raise
# ============================================================================

"""
Tutorial: Re-raising after logging
----------------------------------

Sometimes you catch an exception to log it (or add context) but then want
the caller to handle it. Use 'raise' with no arguments to re-raise the
current exception and preserve the traceback.
"""


def parse_device_config(path: Path) -> Dict[str, Any]:
    """
    Read path as JSON and return the parsed dict. If the file is missing or
    invalid JSON, log the error and re-raise the same exception so the caller
    can decide what to do.

    Args:
        path: Path to the JSON config file.

    Returns:
        Parsed dict.

    Raises:
        FileNotFoundError: If path does not exist (after logging).
        json.JSONDecodeError: If content is not valid JSON (after logging).
    """
    # TODO: try: read path with path.read_text(encoding="utf-8"), then json.loads(text).
    # TODO: except FileNotFoundError as e: logger.error("Config not found: %s", path); raise
    # TODO: except json.JSONDecodeError as e: logger.error("Invalid JSON in %s: %s", path, e); raise
    return {}  # Replace with your implementation


# ============================================================================
# EXERCISE 4: Fail fast with clear message
# ============================================================================

"""
Tutorial: Fail fast with clear messages
--------------------------------------

For invalid input or preconditions, raise early with a clear message
(ValueError or TypeError). This makes debugging easier and keeps invalid
state from propagating.
"""


def validate_hostname(hostname: Any) -> str:
    """
    Ensure hostname is a non-empty string. If not, raise ValueError or
    TypeError with a clear message.

    Args:
        hostname: Should be a non-empty string.

    Returns:
        The hostname as str.

    Raises:
        TypeError: If hostname is not a str.
        ValueError: If hostname is empty or whitespace-only.
    """
    # TODO: If hostname is not isinstance(hostname, str), raise TypeError("hostname must be a string").
    # TODO: If hostname stripped is empty, raise ValueError("hostname must be non-empty").
    # TODO: Return hostname stripped (or as-is) as str.
    return ""  # Replace with your implementation


# ============================================================================
# Optional: Uncomment to run simple checks
# ============================================================================

# if __name__ == "__main__":
#     # Exercise 1
#     p = Path(__file__).parent / "nonexistent.json"
#     inv = load_inventory(p)
#     assert inv == {}
#
#     # Exercise 4
#     try:
#         validate_hostname(123)
#     except TypeError as e:
#         assert "string" in str(e).lower()
