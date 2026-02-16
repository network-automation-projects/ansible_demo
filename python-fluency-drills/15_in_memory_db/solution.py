"""
Drill 15: Build a Minimal In-Memory Database — Reference solution.
"""

from typing import Any


class InMemoryDB:
    """
    Minimal in-memory DB: insert, update, delete, query.
    Backed by dict. Simple filtering in query().
    """

    def __init__(self) -> None:
        self._records: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def insert(self, record: dict[str, Any]) -> int:
        """Insert record, assign id. Return id."""
        rec = record.copy()
        rec["id"] = self._next_id
        self._records[self._next_id] = rec
        id_val = self._next_id
        self._next_id += 1
        return id_val

    def update(self, id: int, **kwargs: Any) -> None:
        """Update record by id."""
        if id in self._records:
            self._records[id].update(kwargs)

    def delete(self, id: int) -> None:
        """Remove record by id."""
        self._records.pop(id, None)

    def query(self, **filters: Any) -> list[dict[str, Any]]:
        """Return records matching all filters."""
        return [
            r.copy()
            for r in self._records.values()
            if all(r.get(k) == v for k, v in filters.items())
        ]


def main() -> None:
    db = InMemoryDB()
    db.insert({"name": "a", "status": "active"})
    db.insert({"name": "b", "status": "inactive"})
    print(db.query(status="active"))


if __name__ == "__main__":
    main()
