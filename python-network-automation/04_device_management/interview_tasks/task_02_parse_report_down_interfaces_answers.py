"""
Task 02: Parse show ip interface brief and report down interfaces — full solution.
No device connection; works on the output string you are given.
"""

import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_show_ip_int_brief(output: str) -> List[Dict[str, str]]:
    """Parse 'show ip interface brief' into list of dicts (interface, ip, status, protocol)."""
    interfaces: List[Dict[str, str]] = []
    for line in output.strip().splitlines():
        if line.lower().startswith("interface") or "IP-Address" in line:
            continue
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        interface, ip = parts[0], parts[1]
        protocol = parts[-1]
        if len(parts) >= 6 and parts[-3] == "administratively" and parts[-2] == "down":
            status = "administratively down"
        else:
            status = parts[-2]
        interfaces.append({
            "interface": interface,
            "ip": ip,
            "status": status,
            "protocol": protocol,
        })
    return interfaces


def report_down_interfaces(parsed: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter to interfaces that are down or administratively down."""
    down = [
        p
        for p in parsed
        if p.get("status") != "up" or p.get("protocol") != "up"
    ]
    for d in down:
        logger.info(
            "Down interface: %s %s %s/%s",
            d["interface"], d["ip"], d["status"], d["protocol"],
        )
    return down


def main() -> None:
    sample_output = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up
GigabitEthernet0/1     10.0.0.1        YES manual up                    up
GigabitEthernet0/2     unassigned      YES unset  administratively down down
Vlan1                  unassigned      YES unset  administratively down down
"""
    parsed = parse_show_ip_int_brief(sample_output)
    down = report_down_interfaces(parsed)
    logger.info("Parsed %s interfaces, down: %s", len(parsed), len(down))
    print("Done.")


if __name__ == "__main__":
    main()
