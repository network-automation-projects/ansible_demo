"""
Device runner that builds Netmiko-style connection params.

Code review: find where credentials are exposed and fix.
No real connections; mock only.
"""

import logging
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Hardcoded credentials (bug 1): never commit these.
DEFAULT_USER = "admin"
DEFAULT_PASS = "admin123"


def load_devices(config_path: Path) -> list[dict]:
    """Load device list from YAML. File may contain username/password (bug 2: committed secrets)."""
    if yaml is None:
        return []
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])


def build_connection_params(device: dict) -> dict:
    """Build params for ConnectHandler. Prefer device dict, fallback to defaults."""
    params = {
        "host": device.get("host") or device.get("ip"),
        "device_type": device.get("device_type", "cisco_ios"),
        "username": device.get("username") or DEFAULT_USER,
        "password": device.get("password") or DEFAULT_PASS,
    }
    # Bug 3: logging full params including password
    logger.info("Connecting with params: %s", params)
    return params


def run_mock(device: dict) -> str:
    """Mock connect and run; no real SSH."""
    params = build_connection_params(device)
    return f"mock output for {params['host']}"


def main() -> None:
    # Optional: load from devices.yaml (if present). Don't commit real credentials there.
    config_path = Path(__file__).parent / "devices.yaml"
    if config_path.exists() and yaml is not None:
        devices = load_devices(config_path)
    else:
        devices = [
            {"host": "192.168.1.1", "device_type": "cisco_ios"},
            # username/password will use DEFAULT_USER / DEFAULT_PASS
        ]

    for device in devices:
        output = run_mock(device)
        print(output)


if __name__ == "__main__":
    main()
