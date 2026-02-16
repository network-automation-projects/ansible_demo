"""
Python Network Automation - Basic Practice (Sets & File I/O)
============================================================

Short practice for sets and simple file operations. Use after or alongside
lists_dicts_practice.py. Paths use pathlib (no hardcoded absolute paths).

Prerequisites: Module 01 (Core Fundamentals), lists_dicts_practice (optional).
"""

from pathlib import Path
from typing import List, Set

# =============================================================================
# PART 1: SETS
# =============================================================================

# -----------------------------------------------------------------------------
# 1.1 Create set, deduplicate, membership
# -----------------------------------------------------------------------------


def unique_interface_names(interfaces: List[str]) -> Set[str]:
    """
    Return a set of interface names (removes duplicates).
    Use: 

    Example:
        >>> unique_interface_names(['Eth0', 'Eth1', 'Eth0', 'Eth2'])
        {'Eth0', 'Eth1', 'Eth2'}
    """
    # TODO: 
    return  set(interfaces) # replace


def interfaces_in_both(list_a: List[str], list_b: List[str]) -> Set[str]:
    """
    Return the set of names that appear in both lists.

    Example:
        >>> interfaces_in_both(['Eth0', 'Eth1', 'Eth2'], ['Eth1', 'Eth2', 'Eth3'])
        {'Eth1', 'Eth2'}
    """
    # TODO: return 
    return set(list_a) & set(list_b) # replace


def all_interfaces_either_list(list_a: List[str], list_b: List[str]) -> Set[str]:
    """
    Return the set of all names that appear in either list (no duplicates).
    

    Example:
        >>> all_interfaces_either_list(['Eth0', 'Eth1'], ['Eth1', 'Eth2'])
        {'Eth0', 'Eth1', 'Eth2'}
    """
    # TODO: 
    return set(list_a).union(list_b)  # replace

    # or
    return set(list_a) | set(list_b)



def add_interface_to_set(interfaces: Set[str], name: str) -> None:
    """
    Add name to the set in place. 

    Args:
        interfaces: Set to modify
        name: Interface name to add
    """
    # TODO:
    interfaces.add(name)


def discard_interface(interfaces: Set[str], name: str) -> None:
    """
    Remove name from the set if present. Does nothing if name not in set.
    Use:

    Args:
        interfaces: Set to modify
        name: Interface name to remove
    """
    # TODO: 
    interfaces.discard(name)


# =============================================================================
# PART 2: SIMPLE FILE I/O
# =============================================================================

# -----------------------------------------------------------------------------
# 2.1 Read and write text files (use pathlib.Path)
# -----------------------------------------------------------------------------


def read_file_contents(file_path: Path) -> str:
    """
    Read the entire file and return its contents as a string.
    Use:

    Args:
        file_path: Path to the file (pathlib.Path)

    Returns:
        File contents as a single string
    """
    # TODO: 
    with open(file_path, "r") as f:
        return f.read()  # replace


def read_file_lines(file_path: Path) -> List[str]:
    """
    Read the file and return a list of lines (without trailing newlines).

    Example:
        If file has two lines, return ['line1', 'line2'].
    """
    # TODO: 
    with open(file_path, "r") as f:
        return f.read().splitlines()  # replace


def write_file_contents(file_path: Path, content: str) -> None:
    """
    Write content to the file (overwrites if it exists).

    Args:
        file_path: Path to the file
        content: String to write
    """
    # TODO:
    with open(file_path, "w") as f:
        f.write(content)


def append_line_to_file(file_path: Path, line: str) -> None:
    """
    Append a single line to the file. Add a newline if line does not end with one.

    Args:
        file_path: Path to the file
        line: Line to append (add "\\n" if missing)
    """
    # TODO: 
    with open(file_path, "a") as f:
        f.write(line if line.endswith("\n") else line + "\n")


# =============================================================================
# Tests (uncomment to run)
# =============================================================================

if __name__ == "__main__":
    print("Basic Practice (Sets & File I/O) — uncomment tests to run.\n")

    # Part 1: Sets
    assert unique_interface_names(['Eth0', 'Eth1', 'Eth0']) == {'Eth0', 'Eth1'}
    assert interfaces_in_both(['Eth0', 'Eth1'], ['Eth1', 'Eth2']) == {'Eth1'}
    assert all_interfaces_either_list(['Eth0', 'Eth1'], ['Eth1', 'Eth2']) == {'Eth0', 'Eth1', 'Eth2'}
    s = {'Eth0'}; add_interface_to_set(s, 'Eth1'); assert s == {'Eth0', 'Eth1'}
    s = {'Eth0', 'Eth1'}; discard_interface(s, 'Eth1'); assert s == {'Eth0'}

    # Part 2: File I/O (requires a temp file or fixture; run answers file for full tests)
    from pathlib import Path
    p = Path("/tmp/test_basic_practice.txt")
    write_file_contents(p, "hello\nworld\n"); assert read_file_contents(p) == "hello\nworld\n"
    assert read_file_lines(p) == ['hello', 'world']
    append_line_to_file(p, "line3"); assert read_file_lines(p) == ['hello', 'world', 'line3']

    print("Done.")
