"""
Python Network Automation - Pattern Detection Tools Exercises (Answer Key)

Reference solutions. Try exercises.py first, then compare here.

Expected output when run as __main__ (python exercises_answers.py):

    Pattern Detection Tools – Answer Key (run exercises.py to practice)

    1. Parsed log records: 5
       First: {'timestamp': '2025-02-05 10:00:00', 'level': 'INFO', 'message': 'Server started'}
    2. Count by level: {'INFO': 2, 'WARN': 1, 'ERROR': 2}
    3. Interfaces: ['Ethernet1/1', 'GigabitEthernet0/0']
    4. Table rows: 3
       First: {'name': 'router1', 'ip': '10.0.0.1', 'status': 'up'}
    6. First version: 15.2
"""

import re
from pathlib import Path
from typing import Dict, List


# Pattern for log lines: YYYY-MM-DD HH:MM:SS LEVEL message
LOG_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARN|ERROR|DEBUG)\s+"
    r"(?P<message>.+)$"
)

# (? = “special group”
# P = “Python-style named group”
# <timestamp> = the name of the group
# (?P<timestamp>...) - “a capturing group named timestamp.”
# ^ — start of string/line
# $ — end of string/line
# ?: - “this group is non-capturing”:
# \d+ - one or more digits


def parse_log_lines(log_content: str) -> List[Dict[str, str]]:
    """Parse log content; non-matching lines get level 'UNKNOWN'."""
    records: List[Dict[str, str]] = []              #create empty list of dictionary items
    for line in log_content.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = LOG_LINE_RE.match(line)
        if m:
            records.append({                        # found a match for that pattern, add that to records
                "timestamp": m.group("timestamp"),
                "level": m.group("level"),
                "message": m.group("message").strip(),
            })
        else:                                       # not a match, mark unknown and add the whole string so a human can read it?
            records.append({
                "timestamp": "",
                "level": "UNKNOWN",
                "message": line,
            })
    return records


def count_by_level(records: List[Dict[str, str]]) -> Dict[str, int]:
    """Return dict mapping log level -> count."""   # return the number of each level of log entries
    counts: Dict[str, int] = {}
    for r in records:                               # for that dictionary in the list of dictionaries
        level = r.get("level", "UNKNOWN")           # get the value at the key called level, mark as unknown as a default if that key is not found
        counts[level] = counts.get(level, 0) + 1    # increment the count on the key for that level of log entry type.
    return counts


def extract_interface_names(text: str) -> List[str]:
    """Return unique interface names found in text, sorted."""
    pattern = r"(?:GigabitEthernet|Ethernet|FastEthernet)\d+/\d+"   # raw, non collecting string. has the three possible names, allows for a number of numerical digits a / and more numerical digits. 
    names = re.findall(pattern, text)                               # compare the text to the pattern. if found, add the names it finds to the names string
    return sorted(set(names))


def parse_simple_table(table_text: str) -> List[Dict[str, str]]:
    """Parse table with header and rows; columns separated by whitespace."""
    lines = [ln.strip() for ln in table_text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return []
    header = re.split(r"\s+", lines[0])  
    keys = [k.lower() for k in header]
    rows: List[Dict[str, str]] = []
    for line in lines[1:]:
        values = re.split(r"\s+", line)
        if len(values) >= len(keys):
            row = dict(zip(keys, values[: len(keys)]))
            rows.append(row)
    return rows


def parse_log_file(file_path: str | Path) -> tuple[List[Dict[str, str]], Dict[str, int]]:
    """Read file, parse log lines, return (records, count_by_level). On error return ([], {}).
    Expected for a file with SAMPLE_LOG content: (list of 5 records, {'INFO': 2, 'WARN': 1, 'ERROR': 2})."""
    try:
        path = Path(file_path)
        if not path.is_file():
            return [], {}
        content = path.read_text()
        records = parse_log_lines(content)
        counts = count_by_level(records)
        return records, counts
    except Exception:
        return [], {}


def extract_first_version(text: str) -> str | None:
    """Return first 'version X.Y' or 'Version X.Y' match, or None."""
    m = re.search(r"[Vv]ersion\s+(\d+\.\d+)", text)
    return m.group(1) if m else None


# -----------------------------------------------------------------------------
# Same sample data as exercises.py for running answers
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
    print("Pattern Detection Tools – Answer Key (run exercises.py to practice)\n")

    # 1. Expected: 5 records; first has timestamp, INFO, "Server started"
    records = parse_log_lines(SAMPLE_LOG)
    print(f"1. Parsed log records: {len(records)}")
    if records:
        print(f"   First: {records[0]}")

    # 2. Expected: {'INFO': 2, 'WARN': 1, 'ERROR': 2}
    counts = count_by_level(records)
    print(f"2. Count by level: {counts}")

    # 3. Expected: ['Ethernet1/1', 'GigabitEthernet0/0'] (unique, sorted)
    if_text = "Interface GigabitEthernet0/0 and Ethernet1/1 and GigabitEthernet0/0"
    ifs = extract_interface_names(if_text)
    print(f"3. Interfaces: {ifs}")

    # 4. Expected: 3 rows; first {'name': 'router1', 'ip': '10.0.0.1', 'status': 'up'}
    table_rows = parse_simple_table(SAMPLE_TABLE)
    print(f"4. Table rows: {len(table_rows)}")
    if table_rows:
        print(f"   First: {table_rows[0]}")

    # 6. Expected: '15.2'
    ver_text = "Cisco IOS Software, Version 15.2(4)M6"
    ver = extract_first_version(ver_text)
    print(f"6. First version: {ver}")
