"""
Drill 4: Parse and Transform Nested JSON
Fill in the TODOs. See README.md for the problem description.
"""

from typing import Any


def extract_ids(obj: Any) -> list[Any]:
    """
    Extract all values for keys named "id" from deeply nested JSON.
    Return flat list, preserving order of first occurrence.
    No external libraries.
    """
    # TODO: Recursively traverse dicts and lists
    # TODO: When key == "id", append value to result
    # TODO: Handle dict: iterate items; handle list: iterate elements
    raise NotImplementedError("Implement me")


def main() -> None:
    data = {"id": "a", "nested": {"id": "b", "items": [{"id": "c"}]}}
    result = extract_ids(data)
    print("IDs:", result)
    assert result == ["a", "b", "c"]


if __name__ == "__main__":
    main()
