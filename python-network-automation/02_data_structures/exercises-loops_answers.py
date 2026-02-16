"""
Answer key for exercises-loops.py in this folder.
Use this file to verify your solutions.
"""

from typing import List, Dict, Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def device_interface_pairs(devices: Dict[str, List[str]]) -> List[tuple]:
    """Build a flat list of (device, interface) pairs from a device-to-interfaces map."""
    result = []
    for device, interface_list in devices.items():
        for interface in interface_list:
            result.append((device, interface))  #outer is the append.  inner makes it a tuple
    return result


# Tutorial: while loops
# ---------------------

# Use while when you repeat until a condition changes (e.g. success or limit).
# Always ensure the condition can become false to avoid infinite loops.

# In network automation:
# - Retry connection or API call until success or max attempts
# - Poll device until it becomes reachable
# - Read input until sentinel value
# """


# def retry_until_success(
#     attempt_fn: Callable[[], bool],
#     max_attempts: int,
# ) -> bool:
#     """
#     Call attempt_fn() repeatedly until it returns True or max_attempts is reached.

#     Args:
#         attempt_fn: No-argument callable that returns True on success, False otherwise
#         max_attempts: Maximum number of attempts (must be >= 1)

#     Returns:
#         True if attempt_fn() returned True on any attempt, False otherwise

#     Example:
#         >>> n = [0]
#         >>> def succeed_on_third():
#         ...     n[0] += 1
#         ...     return n[0] >= 3
#         >>> retry_until_success(succeed_on_third, 5)
#         True
#         >>> retry_until_success(lambda: False, 3)
#         False
#     """
#     # TODO: Use a while loop: attempt up to max_attempts, return True on success
#     # ...
#     return False


def retry_until_success(
    attempt_fn: Callable[[], bool], #the first argument is a function (must be callable (no arg in, returns bool))
    max_attempts: int,              #second arg is max attempts to try
) -> bool:
    """Call attempt_fn() repeatedly until it returns True or max_attempts is reached."""
    attempts = 0
    while attempts < max_attempts:
        if attempt_fn():               #for each attempt, run the function the user passes in
            return True                 # in func returns true, return true and we are done
        attempts += 1
    return False                        #otherwise return false


def first_up_interface(interfaces: List[Dict[str, str]]) -> Optional[str]:
    """Return the name of the first interface with status "up", or None if none."""
    for iface in interfaces:
        if iface.get("status") == "up":
            return iface.get("name")
    return None    #if it never finds one that is up, return none
    


def filter_config_lines(
    lines: List[str],
    comment_prefix: str = "!",
) -> List[str]:
    """Return non-empty, non-comment lines, stripped."""
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:                #if stripped line is empty go to the next line?
            continue
        if stripped.startswith(comment_prefix):
            continue
        result.append(stripped)
    return result


if __name__ == "__main__":
    print("02_data_structures – loops answer key (run exercises-loops.py to practice)")
