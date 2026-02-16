"""
Buggy config loader.

Works when run from the script's directory.
Fails with FileNotFoundError when run from project root or another directory.
Why?
"""

import json


def load_config(config_path: str = "config.json") -> dict:
    """Load config from JSON file."""
    with open(config_path) as f:
        return json.load(f)


def main() -> None:
    config = load_config()
    print("Loaded config:")
    for device in config.get("devices", []):
        print(f"  - {device['hostname']}: {device['ip']}")


if __name__ == "__main__":
    main()
