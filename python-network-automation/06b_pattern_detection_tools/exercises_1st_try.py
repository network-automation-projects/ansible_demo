"""
Python Network Automation - Pattern Detection Tools Exercises

Interview-style parsing tasks. Use the README and LESSON_derive_patterns.md
to decide HOW to approach each (shape -> method -> pattern -> edge cases),
then implement.

Run with: python exercises.py
"""

import re
from pathlib import Path
from typing import Any, Dict, List


# -----------------------------------------------------------------------------
# EXERCISE 1: Parse log lines from a string
# -----------------------------------------------------------------------------
# TASK: Given a multi-line string, each line format "YYYY-MM-DD HH:MM:SS LEVEL message",
# return a list of dicts with keys "timestamp", "level", "message".
# - Skip blank lines.
# - If a line doesn't match the format, either skip it or set level to "UNKNOWN".
#
# HINT: Shape = line-based, fixed order per line. Use the process:
#   1. Name shape: one line = timestamp, level, message
#   2. Method: loop lines; one regex with groups per line
#   3. Edge: no match -> skip or level "UNKNOWN"



LOG_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}  \d{2}:\d{2}:\d{2})\s+"
    r"^(?P<level>INFO|WARN|ERROR|DEBUG)s+"
    r"^(?P<message>.+)"
)


def parse_log_lines(log_content: str) -> List[Dict[str, str]]:
    """
    Parse log content; each line: YYYY-MM-DD HH:MM:SS LEVEL message.
    Return list of {"timestamp", "level", "message"}. Skip blanks; non-matching -> level "UNKNOWN".
    """
    # TODO: implement using re and a loop over lines
    records: List[Dict[str, str]] = []
    for line in log_content.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = LOG_LINE_RE.match(line)
        if m:
            records.append({
                "timestamp": m.group("timestamp"),
                "level": m.group("level"),
                "message": m.group("message").strip(),
            })
        else:
            records.append({
                "timestamp": "",
                "level": "UNKNOWN",
                "message": line,
            })

    return records


# -----------------------------------------------------------------------------
# EXERCISE 2: Count by log level
# -----------------------------------------------------------------------------
# TASK: Given the list of parsed log records from Exercise 1, return a dict
# mapping each level to its count, e.g. {"INFO": 5, "ERROR": 2}.
#
# HINT: Shape = list of dicts with "level" key. Method: loop and count (or use Counter).


def count_by_level(records: List[Dict[str, str]]) -> Dict[str, int]:
    """Return dict mapping log level -> count."""
    # TODO: implement
    counts: Dict[str, int] = {}
    for r in records:
        level = r.get("level", "UNKNOWN")
        counts[level] = counts(r.get(level, 0)) + 1

    return counts


# -----------------------------------------------------------------------------
# EXERCISE 3: Extract interface names from device output
# -----------------------------------------------------------------------------
# TASK: From text that may contain interface names like GigabitEthernet0/0,
# Ethernet1/1, FastEthernet0/1, return a list of unique interface names found.
#
# HINT: Shape = repeated token. Method: re.findall with a pattern that matches
# GigabitEthernet|Ethernet|FastEthernet followed by digits/slash/digits. Then dedupe (set).


def extract_interface_names(text: str) -> List[str]:
    """Return unique interface names (e.g. GigabitEthernet0/0) found in text."""
    # TODO: implement; return sorted list of unique names
    pattern = r"(?:GigabitEthernet|Ethernet1|FastEthernet)\d+/\d+"
    names = re.findall(pattern, text)
    return sorted(set(names))


# -----------------------------------------------------------------------------
# EXERCISE 4: Parse a simple table (header + rows)
# -----------------------------------------------------------------------------
# TASK: Parse a table where first line is header (e.g. "Name IP Status"),
# remaining lines are rows. Return list of dicts, keys = header names (lowercased),
# values = column values. Assume columns separated by one or more spaces.
#
# HINT: Shape = table. Method: split lines; first line = header (split to get keys);
# rest = rows (split to get values); zip or index by position.


def parse_simple_table(table_text: str) -> List[Dict[str, str]]:
    """
    Parse table with header line and data rows. Columns separated by whitespace.
    Return list of dicts with header names (lowercased) as keys.
    """
    # TODO: implement
    return []


# -----------------------------------------------------------------------------
# EXERCISE 5: Parse log file from path (integration)
# -----------------------------------------------------------------------------
# TASK: Read log file from path; parse each line; return (records, count_by_level).
# If file missing or unreadable, return ([], {}).
#
# HINT: Use pathlib.Path.read_text() or open; reuse parse_log_lines and count_by_level.


def parse_log_file(file_path: str | Path) -> tuple[List[Dict[str, str]], Dict[str, int]]:
    """
    Read file, parse log lines, return (records, count_by_level).
    On error (missing file, etc.) return ([], {}).
    """
    # TODO: implement; use parse_log_lines and count_by_level
    try:
        # ...
        pass
    except Exception:
        pass
    return [], {}


# -----------------------------------------------------------------------------
# EXERCISE 6: Extract first matching group (interview classic)
# -----------------------------------------------------------------------------
# TASK: In text, find the first occurrence of "version X.Y" or "Version X.Y"
# (e.g. "version 15.2" or "Version 16.1") and return the version string (e.g. "15.2").
# If not found, return None.
#
# HINT: Shape = single value. Method: re.search with one capturing group; return m.group(1) if m else None.


def extract_first_version(text: str) -> str | None:
    """Return first 'version X.Y' or 'Version X.Y' match, or None."""
    # TODO: implement
    return None


# -----------------------------------------------------------------------------
# Run exercises (use sample data if no file)
# -----------------------------------------------------------------------------

SAMPLE_LOG = """
2025-02-05 10:00:00 INFO Server started
2025-02-05 10:01:00 WARN High memory usage
2025-02-05 10:02:00 ERROR Connection refused
2025-02-05 10:03:00 INFO Server started
2025-02-05 10:04:00 ERROR Timeout
"""

SAMPLE_TABLE = """
Name          IP             Status
router1        10.0.0.1       up
router2        10.0.0.2       down
switch1        192.168.1.1    up
"""

if __name__ == "__main__":
    print("Pattern Detection Tools - Exercises\n")

    # 1
    records = parse_log_lines(SAMPLE_LOG)
    print(f"1. Parsed log records: {len(records)}")
    if records:
        print(f"   First: {records[0]}")

    # 2
    counts = count_by_level(records)
    print(f"2. Count by level: {counts}")

    # 3
    if_text = "Interface GigabitEthernet0/0 and Ethernet1/1 and GigabitEthernet0/0"
    ifs = extract_interface_names(if_text)
    print(f"3. Interfaces: {ifs}")

    # 4
    table_rows = parse_simple_table(SAMPLE_TABLE)
    print(f"4. Table rows: {len(table_rows)}")
    if table_rows:
        print(f"   First: {table_rows[0]}")

    # 5 (no file by default; would need a path)
    # recs, cnt = parse_log_file(Path("sample.log"))
    # print("5. From file:", len(recs), cnt)

    # 6
    ver_text = "Cisco IOS Software, Version 15.2(4)M6"
    ver = extract_first_version(ver_text)
    print(f"6. First version: {ver}")
