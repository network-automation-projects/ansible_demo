"""
Buggy parser for "show ip interface brief" output.

Parses the fixture and prints interface, IP, status, protocol.
For lines with "administratively down", status or protocol are wrong. Why?
"""

from pathlib import Path


def parse_show_ip_int_brief(output: str) -> list[dict[str, str]]:
    """
    Parse table: skip header, then for each line extract
    interface, ip, status, protocol.
    """
    lines = output.strip().splitlines()
    results: list[dict[str, str]] = []

    for line in lines:
        if not line.strip() or "Interface" in line and "IP-Address" in line:
            continue
        parts = line.split()
        if len(parts) < 6:
            continue
        # Bug: assume status and protocol are single words at fixed indices.
        # "administratively down" is two words, so indices shift.
        interface = parts[0]
        ip = parts[1]
        status = parts[4]
        protocol = parts[5]
        results.append({
            "interface": interface,
            "ip": ip,
            "status": status,
            "protocol": protocol,
        })

    return results


def main() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "show_ip_int_brief_ios.txt"
    output = fixture_path.read_text()
    rows = parse_show_ip_int_brief(output)

    print("Parsed table:")
    for r in rows:
        print(f"  {r['interface']:25} {r['ip']:15} {r['status']:25} {r['protocol']}")


if __name__ == "__main__":
    main()
