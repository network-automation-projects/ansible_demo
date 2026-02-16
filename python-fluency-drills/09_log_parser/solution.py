"""
Drill 9: Write a Log Parser — Reference solution.
"""

from collections import Counter
from pathlib import Path
from typing import Any


def parse_log_line(line: str) -> dict[str, str] | None:
    """Parse 'LEVEL user=N code=N' into dict. Return None if invalid."""
    line = line.strip()
    if not line:
        return None
    parts = line.split()
    if len(parts) < 3:
        return None
    level = parts[0]
    parsed: dict[str, str] = {"level": level}
    for part in parts[1:]:
        if "=" in part:
            k, _, v = part.partition("=")
            parsed[k] = v
    if "user" not in parsed or "code" not in parsed:
        return None
    return parsed


def parse_log_file(path: Path) -> dict[str, Any]:
    """
    Parse log file. Return error_count, most_common_user, status_distribution.
    """
    error_count = 0
    users: list[str] = []
    codes: list[str] = []
    with open(path) as f:
        for line in f:
            row = parse_log_line(line)
            if row:
                if row["level"] == "ERROR":
                    error_count += 1
                users.append(row["user"])
                codes.append(row["code"])
    status_dist = dict(Counter(codes))
    most_common_user = Counter(users).most_common(1)[0][0] if users else ""
    return {
        "error_count": error_count,
        "most_common_user": most_common_user,
        "status_distribution": status_dist,
    }


def main() -> None:
    log_content = """ERROR user=12 code=500
INFO user=9 code=200
ERROR user=12 code=500
"""
    path = Path("sample.log")
    path.write_text(log_content)
    result = parse_log_file(path)
    print(result)
    path.unlink()


if __name__ == "__main__":
    main()
