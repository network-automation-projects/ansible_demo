"""
INTERVIEW PROMPT (about 30 min)
-------------------------------
Given the raw text output of 'show ip interface brief', parse it into a list of
structured records (interface, IP, status, protocol). Then implement a function
that returns only interfaces that are down or administratively down. No device
connection—work with the string output only. Assume you receive the output
string (e.g. from the interviewer or from a command you ran).
"""

import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to parse the show ip interface brief output into a list of dicts. ---
def parse_show_ip_int_brief(output: str) -> List[Dict[str, str]]:
    """Parse 'show ip interface brief' into list of dicts (interface, ip, status, protocol)."""
    # TODO: skip header line (Interface, IP-Address, OK?, ...). For each data line: split columns;
    # TODO: first col=interface, second=ip; status can be "up", "down", or "administratively down";
    # TODO: last col=protocol (up/down). Append {"interface", "ip", "status", "protocol"}.
    raise NotImplementedError("Step 1: parse table into list of dicts")


# --- Step 2: Next I'm going to filter to interfaces that are down or administratively down. ---
def report_down_interfaces(parsed: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter to interfaces that are down or administratively down."""
    # TODO: return [p for p in parsed if status != "up" or protocol != "up"]
    raise NotImplementedError("Step 2: filter down/administratively down")


# --- Step 3: main() — use sample output (no file), parse, report down, print. ---
def main() -> None:
    # Sample output; in the interview you may receive this string or get it from a device.
    sample_output = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up
GigabitEthernet0/1     10.0.0.1        YES manual up                    up
GigabitEthernet0/2     unassigned      YES unset  administratively down down
Vlan1                  unassigned      YES unset  administratively down down
"""
    parsed = parse_show_ip_int_brief(sample_output)
    down = report_down_interfaces(parsed)
    logger.info("Parsed %s interfaces, down: %s", len(parsed), len(down))
    for d in down:
        logger.info("Down: %s %s %s/%s", d["interface"], d["ip"], d["status"], d["protocol"])
    print("Done.")


if __name__ == "__main__":
    main()
