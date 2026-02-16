"""
Task 09: Compliance — interfaces without description — full solution.
No device connection; works on the config string you are given.
"""

import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def compliance_interfaces_no_description(config_text: str) -> List[str]:
    """Return interface names that have no 'description' in their block (simple check)."""
    without_desc: List[str] = []
    current: Optional[str] = None
    has_description = False
    for line in config_text.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("interface "):
            if current is not None and not has_description:
                without_desc.append(current)
            current = line_stripped.split(maxsplit=1)[-1].strip()
            has_description = False
        elif current is not None and line_stripped.startswith("description "):
            has_description = True
        elif current is not None and line_stripped and not line_stripped.startswith("!"):
            if line_stripped == "end":
                if not has_description:
                    without_desc.append(current)
                current = None
    if current is not None and not has_description:
        without_desc.append(current)
    return without_desc


def main() -> None:
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
