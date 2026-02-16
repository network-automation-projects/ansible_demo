"""
Python Network Automation - Data Structures: Loops Practice
============================================================

Exercises for practicing for loops, nested loops, while loops,
and loop control (break/continue) in a network automation context.
"""

from math import fabs
from typing import List, Dict, Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXERCISE 1: Nested Loops – Device and Interface Pairs
# ============================================================================

"""
Tutorial: Nested loops
----------------------

Use a loop inside another loop when you need to process every combination
of two levels (e.g. every device and each of its interfaces).

In network automation:
- Build (device, interface) pairs for config generation
- Iterate over devices then interfaces for show commands
- Flatten device interface matrices for reporting
"""


def device_interface_pairs(devices: Dict[str, List[str]]) -> List[tuple]:
    """
    Build a flat list of (device, interface) pairs from a device-to-interfaces map.

    Args:
        devices: Map of device hostname -> list of interface names
            e.g. {"r1": ["Eth0", "Eth1"], "r2": ["Eth0"]}

    Returns:
        List of (device, interface) tuples in order

    Example:
        >>> device_interface_pairs({"r1": ["Eth0", "Eth1"], "r2": ["Eth0"]})
        [('r1', 'Eth0'), ('r1', 'Eth1'), ('r2', 'Eth0')]
    """
    # TODO: Use nested loops: for each device, for each interface, append (device, interface)
    result = []
    for device, interface_list in devices.items():
        for interface in interface_list:
            result.append((device, interface))
    return result


# ============================================================================
# EXERCISE 2: While Loop – Retry Until Success or Max Attempts
# ============================================================================

"""
Tutorial: while loops
---------------------

Use while when you repeat until a condition changes (e.g. success or limit).
Always ensure the condition can become false to avoid infinite loops.

In network automation:
- Retry connection or API call until success or max attempts
- Poll device until it becomes reachable
- Read input until sentinel value
"""


def retry_until_success(
    attempt_fn: Callable[[], bool],
    max_attempts: int,
) -> bool:
    attempts = 0
    # TODO: Use a while loop: attempt up to max_attempts, return True on success
    while attempts < max_attempts:
        if attempt_fn():
            return True
        attempts += 1
    return False


    # """
    # Call attempt_fn() repeatedly until it returns True or max_attempts is reached.

    # Args:
    #     attempt_fn: No-argument callable that returns True on success, False otherwise
    #     max_attempts: Maximum number of attempts (must be >= 1)

    # Returns:
    #     True if attempt_fn() returned True on any attempt, False otherwise

    # Example:
    #     >>> n = [0]
    #     >>> def succeed_on_third():
    #     ...     n[0] += 1
    #     ...     return n[0] >= 3
    #     >>> retry_until_success(succeed_on_third, 5)
    #     True
    #     >>> retry_until_success(lambda: False, 3)
    #     False
    # """

    


# ============================================================================
# EXERCISE 3: break – Find First Match
# ============================================================================

"""
Tutorial: break
---------------

break exits the innermost loop immediately. Use it when you only need
the first item that matches a condition.

In network automation:
- Find first interface that is up
- Find first device that responds to ping
- Stop scanning after first match in logs
"""


def first_up_interface(interfaces: List[Dict[str, str]]) -> Optional[str]:
    """
    Return the name of the first interface with status "up", or None if none.

    Args:
        interfaces: List of dicts with "name" and "status" keys

    Returns:
        First interface name with status "up", or None

    Example:
        >>> first_up_interface([
        ...     {"name": "Eth0", "status": "down"},
        ...     {"name": "Eth1", "status": "up"},
        ...     {"name": "Eth2", "status": "up"}
        ... ])
        'Eth1'
        >>> first_up_interface([{"name": "Eth0", "status": "down"}])
        None
    """
    # TODO: Loop over interfaces; when status == "up", return name and break (or return)
    # ...

    for i in interfaces:
        if i.get("status") == "up":
            return i.get("name")
    return None


# ============================================================================
# EXERCISE 4: continue – Skip Comments and Blanks
# ============================================================================

"""
Tutorial: continue
-----------------

continue skips the rest of the current iteration and goes to the next.
Use it to ignore certain items (comments, empty lines, invalid data).

In network automation:
- Skip comment lines when parsing config
- Skip empty or header lines in command output
- Filter out disabled devices in a list
"""


def filter_config_lines(
    lines: List[str],
    comment_prefix: str = "!",
) -> List[str]:

    # TODO: Loop over lines; strip each; use continue to skip empty and comment lines
    result = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line == '':
            if stripped_line.startswith(comment_prefix):
                continue
            result.append(stripped_line)
    return result


"""
Return lines with leading/trailing whitespace stripped, excluding empty
lines and lines that start with comment_prefix (after strip).

Args:
    lines: Raw config or log lines
    comment_prefix: Lines starting with this (after strip) are skipped

Returns:
    Non-empty, non-comment lines, stripped

Example:
    >>> filter_config_lines(["  hostname r1  ", "!", "  ! comment", "  interface Eth0  "])
    ['hostname r1', 'interface Eth0']
"""



# ============================================================================
# Test Cases (Uncomment to test your solutions)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DATA STRUCTURES – LOOPS EXERCISES")
    print("=" * 70)

    # Exercise 1: Nested loops
    out = device_interface_pairs({"r1": ["Eth0", "Eth1"], "r2": ["Eth0"]})
    print("Exercise 1:", out)
    # Expected: [('r1', 'Eth0'), ('r1', 'Eth1'), ('r2', 'Eth0')]

    # Exercise 2: While loop
    n = [0]
    def succeed_on_third():
        n[0] += 1
        return n[0] >= 3
    print("Exercise 2:", retry_until_success(succeed_on_third, 5))  # True
    print("Exercise 2:", retry_until_success(lambda: False, 2))    # False

    # Exercise 3: break
    ifaces = [{"name": "Eth0", "status": "down"}, {"name": "Eth1", "status": "up"}]
    print("Exercise 3:", first_up_interface(ifaces))  # 'Eth1'
    print("Exercise 3:", first_up_interface([{"name": "Eth0", "status": "down"}]))  # None

    # Exercise 4: continue
    lines = ["  hostname r1  ", "!", "  ! comment", "  interface Eth0  "]
    print("Exercise 4:", filter_config_lines(lines))
    # Expected: ['hostname r1', 'interface Eth0']

    print("\nUncomment test cases above to verify your solutions!")
