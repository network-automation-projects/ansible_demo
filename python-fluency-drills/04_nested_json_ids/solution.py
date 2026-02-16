"""
Drill 4: Parse and Transform Nested JSON — Reference solution.
"""

from typing import Any


def extract_ids(obj: Any) -> list[Any]:
    """
    Extract all values for keys named "id" from deeply nested JSON.
    Return flat list, preserving order of first occurrence.
    """
    result: list[Any] = []

    def visit(o: Any) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "id":
                    result.append(v)
                visit(v)
        elif isinstance(o, list):
            for item in o:
                visit(item)

    visit(obj)
    return result


def main() -> None:
    data = {"id": "a", "nested": {"id": "b", "items": [{"id": "c"}]}}
    result = extract_ids(data)
    print("IDs:", result)
    assert result == ["a", "b", "c"]


if __name__ == "__main__":
    main()
