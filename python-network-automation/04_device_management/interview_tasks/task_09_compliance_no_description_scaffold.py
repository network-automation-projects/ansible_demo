"""
INTERVIEW PROMPT (about 30 min)
-------------------------------
Given full config text (e.g. from 'show running-config'), return the list of
interface names that do not have a 'description' line in their interface block.
Parse interface blocks; if a block has no 'description' sub-command, add that
interface name to the result. No device connection. Assume you receive the
config string (e.g. from the interviewer or from a command you ran).
"""

import logging
from typing import List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to find interface blocks in the config (lines starting with "interface "). ---
# --- Step 2: Next I'm going to track whether the current block has a "description " line. ---
# --- Step 3: When an interface block ends (next "interface " or "end"), if no description, add name to list. ---
def compliance_interfaces_no_description(config_text: str) -> List[str]:
    """Return interface names that have no 'description' in their block."""
    # TODO: iterate lines; on "interface X" start new block; if "description " in block, mark; on block end, if no description append name
    raise NotImplementedError("Step 1–3: parse interface blocks, collect those without description")


# --- Step 4: main() — use sample config string (no file), run compliance check, print list. ---
def main() -> None:
    # Sample config; in the interview you may receive this string or get it from a device.
    sample_config = """version 15.2
hostname switch1
!
interface GigabitEthernet0/0
 description Uplink to core
 ip address 192.168.1.1 255.255.255.0
!
interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.0
!
end
"""
    without_desc = compliance_interfaces_no_description(sample_config)
    logger.info("Interfaces without description: %s", without_desc)
    print("Done.")


if __name__ == "__main__":
    main()
