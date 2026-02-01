"""
Exercise: parse show version and show ip interface brief output.
Fill in the TODOs. See README.md for the problem description.
"""

import re
from pathlib import Path


def parse_show_version(output: str) -> dict[str, str]:
    """Extract hostname, uptime, version, model, serial from Cisco-style show version. Use 'Unknown' for missing."""
    result = {"hostname": "Unknown", "uptime": "Unknown", "version": "Unknown", "model": "Unknown", "serial": "Unknown"}
    # TODO: for each line, look for "uptime is" -> hostname (word before uptime), uptime (text after "uptime is ")
    # TODO: look for "Cisco IOS Software" and "Version" -> version line
    # TODO: look for "Processor board ID" -> serial (token after)
    # TODO: look for "Cisco XXXXX (revision" or "Model Number" -> model
    return result


def parse_show_ip_int_brief(output: str) -> list[dict[str, str]]:
    """Extract interface, ip, status, protocol from show ip interface brief table."""
    interfaces = []
    # TODO: skip header line (Interface, IP-Address, OK?, ...)
    # TODO: for each data line: split; first col=interface, second=ip
    # TODO: status can be "up", "down", or "administratively down" (two words)
    # TODO: last col = protocol (up/down)
    # TODO: append {"interface", "ip", "status", "protocol"}
    return interfaces


def main() -> None:
    base = Path(__file__).parent
    version_path = base / "fixtures" / "show_version_ios.txt"
    int_brief_path = base / "fixtures" / "show_ip_int_brief_ios.txt"

    # TODO: version_output = version_path.read_text()
    # TODO: facts = parse_show_version(version_output); print facts
    # TODO: int_output = int_brief_path.read_text()
    # TODO: ifaces = parse_show_ip_int_brief(int_output); print each interface
    pass


if __name__ == "__main__":
    main()
