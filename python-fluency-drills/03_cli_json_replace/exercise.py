"""
Drill 3: Simple CLI Tool
Fill in the TODOs. See README.md for the problem description.
"""

import argparse
import json
import shutil
from pathlib import Path


def load_json(path: Path) -> dict:
    """Load JSON from file. Raise clear error on failure."""
    # TODO: Implement
    raise NotImplementedError("Implement me")


def save_json(path: Path, data: dict) -> None:
    """Save JSON to file. Create backup at path.bak before overwriting."""
    # TODO: Copy existing file to path.bak if it exists
    # TODO: Write data to path
    raise NotImplementedError("Implement me")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace keys in JSON file")
    # TODO: Add --file (required) and --replace (action='append', for key=value)
    # TODO: Parse args
    # TODO: Load JSON, apply replacements, save with backup
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    main()
