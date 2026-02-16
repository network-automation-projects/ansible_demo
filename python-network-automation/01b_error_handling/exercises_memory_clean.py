# Python Network Automation - Error Handling Examples

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





# ============================================================================
# Example 1: Load JSON file with specific exceptions
# ============================================================================


def load_json_config(path: Path) -> Dict[str, Any]:
    """
    Load a JSON config file. Return empty dict on missing file or invalid JSON.
    Catch specific exceptions and log; do not swallow silently.
    On other I/O errors (e.g. permission denied), log and re-raise.
    """

    #verify file exists


    #grab the data






# ============================================================================
# Example 2: Per-device handling — collect ok and failed
# ============================================================================


def run_batch(
    hostnames: List[str],
    apply_fn: Callable[[str], Any],
) -> Dict[str, Any]:
    """
    Call apply_fn(hostname) for each hostname. On success append to 'ok';
    on exception log and append (hostname, error_message) to 'failed'.
    One failing device does not stop the batch.

    Returns:
        Dict with keys 'ok' (list of hostnames) and 'failed'
        (list of (hostname, error_message)).
    """




# ============================================================================
# Example 3: try / else / finally — cleanup and success-only path
# ============================================================================


def load_and_parse_with_cleanup(path: Path) -> Dict[str, Any]:
    """
    Open file, parse JSON. Use else for 'only on success' path and finally
    to close the file handle.
    """




# ============================================================================
# Example 4: Re-raise after logging
# ============================================================================


def get_device_config(path: Path, hostname: str) -> Dict[str, Any]:
    """
    Load config for a device from a JSON file. Log and re-raise on parse error
    so the caller can decide whether to abort or continue.
    """
    try:
        ...  # TODO: path.read_text(encoding="utf-8"), json.loads(text)
    except FileNotFoundError as e:
        logger.error("Config file not found: %s", path)
        raise
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", path, e.msg)
        raise


# ============================================================================
# Example 5: Fail fast with clear message
# ============================================================================


def normalize_devices(devices: Any) -> List[Dict[str, str]]:
    """
    Validate input: devices must be a list of dicts with 'hostname' and 'ip'.
    Raise early with a clear message if not.
    """
    pass  # TODO: implement


# ============================================================================
# Demo (run when this file is executed)
# ============================================================================


def _mock_apply(hostname: str) -> None:
    """Simulate a device operation: fail for 'core-sw2'."""
    if hostname == "core-sw2":
        raise TimeoutError("Connection timed out")
    logger.info("Applied to %s", hostname)




if __name__ == "__main__":
    # Example 1: load_json_config
    config_path = Path(__file__).parent / "nonexistent.json"
    config = load_json_config(config_path)
    print("Example 1 - load_json_config(nonexistent):", config)

    # Example 2: run_batch with per-device handling
    hosts = ["r1", "core-sw2", "r2"]
    batch_result = run_batch(hosts, _mock_apply)
    print("Example 2 - run_batch:", batch_result)

    # Example 5: fail fast
    try:
        normalize_devices("not a list")
    except TypeError as e:
        print("Example 5 - normalize_devices error:", e)
