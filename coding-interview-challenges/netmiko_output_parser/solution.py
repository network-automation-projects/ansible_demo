"""
Netmiko output parser: parse show version and show ip interface brief.
"""

import re
from pathlib import Path


def parse_show_version(output: str) -> dict[str, str]:
    """Extract hostname, uptime, version, model, serial from Cisco-style show version."""
    result = {
        "hostname": "Unknown",
        "uptime": "Unknown",
        "version": "Unknown",
        "model": "Unknown",
        "serial": "Unknown",
    }

    for line in output.splitlines():
        line_lower = line.lower()
        # "switch1 uptime is 5 weeks, 2 days, ..."
        if "uptime is" in line_lower:
            match = re.search(r"^(\S+)\s+uptime\s+is\s+(.+)$", line, re.IGNORECASE)
            if match:
                result["hostname"] = match.group(1)
                result["uptime"] = match.group(2).strip()

        # "Processor board ID FCW2140L0BZ"
        if "processor board id" in line_lower:
            parts = line.split()
            if len(parts) >= 4:
                result["serial"] = parts[-1]

        # "Cisco IOS Software, ... Version 15.2(7)E4 ..."
        if "cisco ios software" in line_lower and "version" in line_lower:
            result["version"] = line.strip()

        # "Cisco CISCO2960-24TC-L (revision R0)"
        if "cisco" in line_lower and "revision" in line_lower:
            match = re.search(r"Cisco\s+(\S+)\s+\(revision", line, re.IGNORECASE)
            if match:
                result["model"] = match.group(1)

    return result


def parse_show_ip_int_brief(output: str) -> list[dict[str, str]]:
    """Extract interface, ip, status, protocol from show ip interface brief table."""
    interfaces = []
    lines = output.strip().splitlines()

    for line in lines:
        # Skip header
        if line.lower().startswith("interface") or "IP-Address" in line:
            continue
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) < 5:
            continue

        interface = parts[0]
        ip = parts[1]

        # Status: "up", "down", or "administratively down"
        # Protocol is last column (up/down)
        protocol = parts[-1]
        if len(parts) >= 6 and parts[-3] == "administratively" and parts[-2] == "down":
            status = "administratively down"
        else:
            status = parts[-2]

        interfaces.append(
            {
                "interface": interface,
                "ip": ip,
                "status": status,
                "protocol": protocol,
            }
        )

    return interfaces


def main() -> None:
    base = Path(__file__).parent
    version_path = base / "fixtures" / "show_version_ios.txt"
    int_brief_path = base / "fixtures" / "show_ip_int_brief_ios.txt"

    version_output = version_path.read_text()
    facts = parse_show_version(version_output)
    print("parse_show_version:")
    for k, v in facts.items():
        print(f"  {k}: {v}")

    int_output = int_brief_path.read_text()
    ifaces = parse_show_ip_int_brief(int_output)
    print("\nparse_show_ip_int_brief: {} interfaces".format(len(ifaces)))
    for iface in ifaces:
        print(f"  {iface['interface']}: {iface['ip']} {iface['status']}/{iface['protocol']}")


if __name__ == "__main__":
    main()
