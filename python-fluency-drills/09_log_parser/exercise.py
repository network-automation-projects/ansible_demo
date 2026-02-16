"""
Drill 9: Write a Log Parser
Fill in the TODOs. See README.md for the problem description.
"""

from collections import Counter
from pathlib import Path
from typing import Any


def parse_log_line(line: str) -> dict[str, str] | None:
    """Parse 'LEVEL user=N code=N' into dict. Return None if invalid."""
    # TODO: Split, extract level, user, code
    # TODO: Return {"level": ..., "user": ..., "code": ...} or None
    raise NotImplementedError("Implement me")


def parse_log_file(path: Path) -> dict[str, Any]:
    """
    Parse log file. Return:
    - error_count: int
    - most_common_user: str
    - status_distribution: dict[str, int] (code -> count)
    """
    # TODO: Read lines, parse each, aggregate
    raise NotImplementedError("Implement me")


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
