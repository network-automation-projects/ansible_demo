"""
INTERVIEW PROMPT (about 25 min)
-------------------------------
Using NAPALM, stage a candidate configuration (merge), compute the diff against
the running config, and discard without committing. Return the diff string.
Assume NAPALM is installed; device info and the candidate config string are
provided.
"""

import logging
from typing import Any, Dict

import napalm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to load the merge candidate and get the diff. ---
# --- Step 2: Next I'm going to discard the candidate (no commit) and return the diff. ---
def stage_and_get_diff(conn: Any, new_config: str) -> str:
    """Stage config and return diff; discard so no commit."""
    # TODO: conn.load_merge_candidate(config=new_config)
    # TODO: diff = conn.compare_config() or ""
    # TODO: conn.discard_config()
    # TODO: return diff
    raise NotImplementedError("Step 1–2: load_merge_candidate, compare_config, discard_config")


# --- Step 3: main() — connect (device_info provided), stage snippet, get diff, close. ---
def main() -> None:
    device_info = {
        "hostname": "192.168.1.1",
        "username": "admin",
        "password": "secret",
        "driver": "ios",
    }
    driver = napalm.get_network_driver(device_info.get("driver", "ios"))
    conn = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"],
    )
    conn.open()
    try:
        new_config = "interface GigabitEthernet0/3\ndescription test\n"
        diff = stage_and_get_diff(conn, new_config)
        logger.info("Diff length: %s", len(diff))
        if diff:
            logger.info("Diff:\n%s", diff)
    finally:
        conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
