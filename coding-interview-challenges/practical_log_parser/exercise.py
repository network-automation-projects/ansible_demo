"""
Exercise: parse log file, filter by level, count by level.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path
from typing import Any


def parse_log_line(line: str) -> dict[str, str] | None:
    """Parse one line into {timestamp, level, message}. Return None for blank/invalid."""
    # TODO: strip line; if empty, return None
    # TODO: split (e.g. first two parts = date and time, next = level, rest = message)
    # TODO: if not enough parts, return None or dict with level "UNKNOWN"
    return None


def load_log(path: str) -> list[dict[str, str]]:
    """Read log file and return list of parsed records. Skip invalid lines."""
    records = []
    # TODO: open path, loop over lines, call parse_log_line, append if not None
    # TODO: handle FileNotFoundError: print message and return []
    return records


def filter_by_level(
    records: list[dict[str, str]], level: str
) -> list[dict[str, str]]:
    """Return only records where level matches (case-sensitive)."""
    # TODO: return [r for r in records if r.get("level") == level]
    return []


def count_by_level(records: list[dict[str, str]]) -> dict[str, int]:
    """Return dict mapping each level to number of entries."""
    # TODO: loop over records, increment count per level; return dict
    return {}


def main() -> None:
    base = Path(__file__).parent
    path = base / "sample.log"
    records = load_log(str(path))
    if not records:
        print("No records loaded.")
        return
    print("Counts:", count_by_level(records))
    errors = filter_by_level(records, "ERROR")
    print("ERROR entries:", len(errors))
    for r in errors:
        print(" ", r)


if __name__ == "__main__":
    main()
