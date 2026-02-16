"""
Python Network Automation - Pattern Detection Tools Examples

Each example shows the THOUGHT PROCESS first (how to derive the pattern),
then the code. Use this to learn how to come up with patterns on your own.
"""

import re
from typing import Any, Dict, List


# =============================================================================
# Example 1: Log line parsing (single line, fixed order)
# =============================================================================
# Step 1: Shape = one line, fixed order: timestamp, level, message
# Step 2: Method = one regex with named groups, or split (careful: message can have spaces)
# Step 3: Pattern = capture timestamp, then level, then rest as message
# Step 4: Edge case = line doesn't match -> return None or skip

LOG_LINE_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARN|ERROR|DEBUG)\s+"
    r"(?P<message>.+)$"
)


def parse_log_line(line: str) -> Dict[str, str] | None:
    """Parse a single log line into timestamp, level, message. Returns None if no match."""
    line = line.strip()
    if not line:
        return None
    m = LOG_LINE_PATTERN.match(line)
    if not m:
        return None
    return {
        "timestamp": m.group("timestamp"),
        "level": m.group("level"),
        "message": m.group("message").strip(),
    }


# =============================================================================
# Example 2: Extract all IPs (repeated token)
# =============================================================================
# Step 1: Shape = same token (IP) repeated anywhere in text
# Step 2: Method = re.findall with one capturing group
# Step 3: Pattern = simple IPv4 (interview: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} is often enough)
# Step 4: Edge case = no IPs -> return []


def extract_all_ips(text: str) -> List[str]:
    """Extract all IPv4 addresses from text. Returns list (possibly empty)."""
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    return re.findall(pattern, text)


# =============================================================================
# Example 3: Key-value lines (e.g. device info)
# =============================================================================
# Step 1: Shape = key-value per line; key and value separated by colon or space
# Step 2: Method = loop lines; for each line, split once (maxsplit=1) or use regex
# Step 3: Pattern = "key: value" or "key value" (first word = key, rest = value)
# Step 4: Edge case = blank line -> skip; malformed -> skip or use "Unknown"


def parse_key_value_lines(lines: str) -> Dict[str, str]:
    """Parse key-value lines (e.g. 'hostname: R1' or 'version 15.2'). Returns dict."""
    result: Dict[str, str] = {}
    for line in lines.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Try "key: value" first
        if ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                result[parts[0].strip().lower()] = parts[1].strip()
                continue
        # Fallback: first word = key, rest = value
        parts = line.split(maxsplit=1)
        if len(parts) >= 2:
            result[parts[0].lower()] = parts[1].strip()
    return result


# =============================================================================
# Example 4: Table parsing (e.g. show ip interface brief)
# =============================================================================
# Step 1: Shape = header line + data rows; columns separated by whitespace
# Step 2: Method = split lines; skip header; for each data line, split columns
# Step 3: Pattern = assume fixed column order: interface, ip, ok?, method, status, protocol
# Step 4: Edge case = empty table -> []; inconsistent columns -> skip row or use defaults

SAMPLE_INT_BRIEF = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up
GigabitEthernet0/1     unassigned      YES unset  administratively down down
"""


def parse_show_ip_int_brief(output: str) -> List[Dict[str, str]]:
    """
    Parse 'show ip interface brief' style table.
    Returns list of dicts: interface, ip, ok, method, status, protocol.
    """
    rows: List[Dict[str, str]] = []
    lines = output.strip().splitlines()
    if len(lines) < 2:
        return rows
    # Skip header (first line)
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        # Minimal columns: interface, ip, ok?, method, status, protocol (6)
        if len(parts) >= 6:
            rows.append({
                "interface": parts[0],
                "ip": parts[1],
                "ok": parts[2],
                "method": parts[3],
                "status": parts[4],
                "protocol": parts[5],
            })
    return rows


# =============================================================================
# Example 5: One block with multiple fields (show version style)
# =============================================================================
# Step 1: Shape = one block of text; fields appear on different lines in no fixed order
# Step 2: Method = multiple re.search() with named groups; one pattern per field
# Step 3: Pattern = extract hostname, uptime, version, model, serial from sample
# Step 4: Edge case = field missing -> use "Unknown"

def parse_show_version_snippet(output: str) -> Dict[str, str]:
    """
    Parse key fields from Cisco-style 'show version' (snippet).
    Returns dict with hostname, uptime, version, model, serial; "Unknown" if missing.
    """
    result: Dict[str, str] = {
        "hostname": "Unknown",
        "uptime": "Unknown",
        "version": "Unknown",
        "model": "Unknown",
        "serial": "Unknown",
    }
    # Hostname: often "hostname uptime is ..." -> first word is hostname
    m = re.search(r"^(\S+)\s+uptime\s+is\s+(.+)", output, re.MULTILINE | re.IGNORECASE)
    if m:
        result["hostname"] = m.group(1)
        result["uptime"] = m.group(2).strip()

    # Version: line with "Version " then version string
    m = re.search(r"Version\s+(\S+)", output, re.IGNORECASE)
    if m:
        result["version"] = m.group(1)

    # Model: e.g. "Cisco CISCO2960-24TC-L (revision ...)"
    m = re.search(r"Cisco\s+(\S+)\s+\(revision", output, re.IGNORECASE)
    if m:
        result["model"] = m.group(1)

    # Serial: "Processor board ID XXXXX"
    m = re.search(r"Processor board ID\s+(\S+)", output, re.IGNORECASE)
    if m:
        result["serial"] = m.group(1)

    return result


# =============================================================================
# Demonstration
# =============================================================================

if __name__ == "__main__":
    print("Pattern Detection Tools - Examples\n")

    # Example 1: Log line
    line = "2025-02-05 14:30:00 ERROR Connection refused to 10.0.0.1"
    print("1. Parse log line:", parse_log_line(line))

    # Example 2: IPs
    text = "Host 10.0.0.1 and 192.168.1.1 are up."
    print("2. Extract IPs:", extract_all_ips(text))

    # Example 3: Key-value
    kv = "hostname: R1\nversion 15.2\nuptime 5 weeks"
    print("3. Key-value lines:", parse_key_value_lines(kv))

    # Example 4: Table
    print("4. show ip int brief:", parse_show_ip_int_brief(SAMPLE_INT_BRIEF))

    # Example 5: show version snippet
    version_snippet = """
router1 uptime is 5 weeks, 2 days, 3 hours
Cisco IOS Software, Version 15.2(4)M6
Cisco CISCO2960-24TC-L (revision R0)
Processor board ID FCW2140L0BZ
"""
    print("5. show version snippet:", parse_show_version_snippet(version_snippet))
