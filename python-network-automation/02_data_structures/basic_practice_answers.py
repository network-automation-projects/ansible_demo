"""
Python Network Automation - Basic Practice (ANSWERS)
=====================================================

Completed solutions for basic_practice.py (sets and file I/O).
Use this to check your work after attempting the exercises.
"""

from pathlib import Path        # so /folder/filename not C:\users\documents...
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
    Use: set(interfaces).

    Example:
        >>> unique_interface_names(['Eth0', 'Eth1', 'Eth0', 'Eth2'])
        {'Eth0', 'Eth1', 'Eth2'}
    """
    return set(interfaces)


def interfaces_in_both(list_a: List[str], list_b: List[str]) -> Set[str]:
    """
    Return the set of names that appear in both lists.
    Use: set(list_a) & set(list_b) or set(list_a).intersection(list_b).

    Example:
        >>> interfaces_in_both(['Eth0', 'Eth1', 'Eth2'], ['Eth1', 'Eth2', 'Eth3'])
        {'Eth1', 'Eth2'}
    """
    return set(list_a) & set(list_b)

    # or
    # These are alternatives that do the right thing:
    # Set intersection with &:
    # return set(list_a) & set(list_b)
    # .intersection():
    # return set(list_a).intersection(list_b)
    # Set comprehension (if you want to avoid building both sets explicitly):
    # return {x for x in list_a if x in list_b}



def all_interfaces_either_list(list_a: List[str], list_b: List[str]) -> Set[str]:
    """
    Return the set of all names that appear in either list (no duplicates).
    Use: set(list_a) | set(list_b) or set(list_a).union(list_b).

    Example:
        >>> all_interfaces_either_list(['Eth0', 'Eth1'], ['Eth1', 'Eth2'])
        {'Eth0', 'Eth1', 'Eth2'}
    """
    return set(list_a) | set(list_b)


def add_interface_to_set(interfaces: Set[str], name: str) -> None:
    """
    Add name to the set in place. Use: interfaces.add(name).

    Args:
        interfaces: Set to modify
        name: Interface name to add
    """
    interfaces.add(name)


def discard_interface(interfaces: Set[str], name: str) -> None:
    """
    Remove name from the set if present. Does nothing if name not in set.
    Use: interfaces.discard(name). (Unlike .remove(), discard does not raise.)

    Args:
        interfaces: Set to modify
        name: Interface name to remove
    """
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
    Use: with open(file_path, "r") as f: return f.read()

    Args:
        file_path: Path to the file (pathlib.Path)

    Returns:
        File contents as a single string
    """
    with open(file_path, "r") as f:
        return f.read()


def read_file_lines(file_path: Path) -> List[str]:
    """
    Read the file and return a list of lines (without trailing newlines).
    Use: with open(file_path, "r") as f: return f.read().splitlines()
    or: return [line.rstrip("\\n") for line in f]

    Example:
        If file has two lines, return ['line1', 'line2'].
    """
    with open(file_path, "r") as f:
        return f.read().splitlines()


def write_file_contents(file_path: Path, content: str) -> None:
    """
    Write content to the file (overwrites if it exists).
    Use: with open(file_path, "w") as f: f.write(content)

    Args:
        file_path: Path to the file
        content: String to write
    """
    with open(file_path, "w") as f:
        f.write(content)


def append_line_to_file(file_path: Path, line: str) -> None:
    """
    Append a single line to the file. Add a newline if line does not end with one.
    Use: with open(file_path, "a") as f: f.write(line if line.endswith("\\n") else line + "\\n")

    Args:
        file_path: Path to the file
        line: Line to append (add "\\n" if missing)
    """
    with open(file_path, "a") as f:
        f.write(line if line.endswith("\n") else line + "\n")


# =============================================================================
# Tests
# =============================================================================

if __name__ == "__main__":
    print("Basic Practice (Answers) — running tests.\n")

    # Part 1: Sets
    assert unique_interface_names(["Eth0", "Eth1", "Eth0"]) == {"Eth0", "Eth1"}
    assert interfaces_in_both(["Eth0", "Eth1"], ["Eth1", "Eth2"]) == {"Eth1"}
    assert all_interfaces_either_list(["Eth0", "Eth1"], ["Eth1", "Eth2"]) == {
        "Eth0",
        "Eth1",
        "Eth2",
    }
    s = {"Eth0"}
    add_interface_to_set(s, "Eth1")
    assert s == {"Eth0", "Eth1"}
    s = {"Eth0", "Eth1"}
    discard_interface(s, "Eth1")
    assert s == {"Eth0"}

    # Part 2: File I/O (temp file in same directory as script)
    p = Path(__file__).parent / "tmp_test_basic_practice.txt"
    try:
        write_file_contents(p, "hello\nworld\n")  # trailing newline so append adds a new line
        assert read_file_contents(p) == "hello\nworld\n"
        assert read_file_lines(p) == ["hello", "world"]
        append_line_to_file(p, "line3")
        assert read_file_lines(p) == ["hello", "world", "line3"]
    finally:
        p.unlink(missing_ok=True)

    print("All tests passed.")
