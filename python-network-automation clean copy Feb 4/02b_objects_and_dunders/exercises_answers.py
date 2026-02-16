"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Any, Iterator, List


class Interface:
    """Represents a network interface (e.g. GigabitEthernet0/1)."""

    def __init__(self, name: str, status: str = "down") -> None:
        self.name = name
        self.status = status

    def __repr__(self) -> str:
        return f"Interface(name={self.name!r}, status={self.status!r})"

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"


class InterfaceList:
    """A list of Interface objects that supports len() and indexing."""

    def __init__(self, interfaces: List[Interface]) -> None:
        self._interfaces = list(interfaces)

    def __len__(self) -> int:
        return len(self._interfaces)

    def __getitem__(self, key: Any) -> Interface:
        if isinstance(key, int):
            return self._interfaces[key]
        for iface in self._interfaces:
            if iface.name == key:
                return iface
        raise KeyError(key)

    def __iter__(self) -> Iterator[Interface]:
        return iter(self._interfaces)


class InterfaceWithEq(Interface):
    """Interface with value equality: two interfaces are equal if name and status match."""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Interface):
            return NotImplemented
        return self.name == other.name and self.status == other.status


if __name__ == "__main__":
    print("02b_objects_and_dunders – answer key (run exercises.py to practice)")
