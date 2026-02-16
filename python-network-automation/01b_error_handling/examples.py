"""
Python Network Automation - Error Handling Examples
====================================================

Runnable examples: try/except/else/finally, specific exceptions,
re-raise, logging, and per-device handling.
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Load JSON file with specific exceptions
# ============================================================================


def load_json_config(path: Path) -> Dict[str, Any]:
    """
    Load a JSON config file. Return empty dict on missing file or invalid JSON.
    Catch specific exceptions and log; do not swallow silently.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        logger.warning("Config file not found: %s", path)
        return {}
    except OSError as e:
        logger.error("Cannot read file %s: %s", path, e)
        raise

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s at line %s: %s", path, e.lineno, e.msg)
        return {}


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
    """
    result: Dict[str, Any] = {"ok": [], "failed": []}

    for hostname in hostnames:
        try:
            apply_fn(hostname)
            result["ok"].append(hostname)
        except (OSError, ConnectionError, TimeoutError) as e:
            logger.warning("Device %s failed: %s", hostname, e)
            result["failed"].append((hostname, str(e)))
        except Exception as e:
            logger.error("Unexpected error for %s: %s", hostname, e)
            result["failed"].append((hostname, str(e)))

    return result


# ============================================================================
# Example 3: try / else / finally — cleanup and success-only path
# ============================================================================


def load_and_parse_with_cleanup(path: Path) -> Dict[str, Any]:
    """
    Open file, parse JSON. Use else for 'only on success' and finally for cleanup.
    """
    handle = None
    try:
        handle = path.open(encoding="utf-8")
        data = json.load(handle)
    except FileNotFoundError:
        logger.warning("File not found: %s", path)
        return {}
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", path, e.msg)
        return {}
    else:
        # Runs only when try completed without raising
        logger.info("Loaded %s keys from %s", len(data), path)
        return data
    finally:
        if handle is not None:
            handle.close()


# ============================================================================
# Example 4: Re-raise after logging
# ============================================================================


def get_device_config(path: Path, hostname: str) -> Dict[str, Any]:
    """
    Load config for a device from a JSON file. Log and re-raise on parse error
    so the caller can decide whether to abort or continue.
    """
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text)
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
    if not isinstance(devices, list):
        raise TypeError("devices must be a list")
    result = []
    for i, d in enumerate(devices):
        if not isinstance(d, dict):
            raise TypeError(f"devices[{i}] must be a dict")
        hostname = d.get("hostname")
        ip = d.get("ip")
        if not hostname or not ip:
            raise ValueError(
                f"devices[{i}] must have non-empty 'hostname' and 'ip'"
            )
        result.append({"hostname": str(hostname), "ip": str(ip)})
    return result


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
