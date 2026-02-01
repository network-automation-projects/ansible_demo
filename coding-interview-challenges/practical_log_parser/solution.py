"""
Log parser: read file, parse lines, filter by level, count by level.
"""

from pathlib import Path
from typing import Any


def parse_log_line(line: str) -> dict[str, str] | None:
    """Parse one line into {timestamp, level, message}. Return None for blank/invalid."""
    line = line.strip()
    if not line:
        return None
    parts = line.split(None, 3)  # max 3 splits: date, time, level, rest
    if len(parts) < 4:
        return {"timestamp": "", "level": "UNKNOWN", "message": line}
    date, time_, level, message = parts
    return {
        "timestamp": f"{date} {time_}",
        "level": level,
        "message": message,
    }


def load_log(path: str) -> list[dict[str, str]]:
    """Read log file and return list of parsed records. Skip invalid lines."""
    records = []
    try:
        with open(path) as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed is not None:
                    records.append(parsed)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    return records


def filter_by_level(
    records: list[dict[str, str]], level: str
) -> list[dict[str, str]]:
    """Return only records where level matches (case-sensitive)."""
    return [r for r in records if r.get("level") == level]


def count_by_level(records: list[dict[str, str]]) -> dict[str, int]:
    """Return dict mapping each level to number of entries."""
    counts: dict[str, int] = {}
    for r in records:
        lev = r.get("level", "UNKNOWN")
        counts[lev] = counts.get(lev, 0) + 1
    return counts


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
