"""
Drill 3: Simple CLI Tool — Reference solution.
"""

import argparse
import json
import shutil
from pathlib import Path


def load_json(path: Path) -> dict:
    """Load JSON from file. Raise clear error on failure."""
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """Save JSON to file. Create backup at path.bak before overwriting."""
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace keys in JSON file")
    parser.add_argument("--file", required=True, type=Path, help="JSON file path")
    parser.add_argument(
        "--replace",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Replace key with value (can repeat)",
    )
    args = parser.parse_args()

    data = load_json(args.file)
    for item in args.replace:
        if "=" not in item:
            raise ValueError(f"Invalid --replace format: {item!r}. Use key=value")
        key, _, value = item.partition("=")
        data[key] = value
    save_json(args.file, data)
    print(f"Updated {args.file}")


if __name__ == "__main__":
    main()
