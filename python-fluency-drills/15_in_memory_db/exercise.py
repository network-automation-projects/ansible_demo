"""
Drill 15: Build a Minimal In-Memory Database
Fill in the TODOs. See README.md for the problem description.
"""

from typing import Any


class InMemoryDB:
    """
    Minimal in-memory DB: insert, update, delete, query.
    Backed by dict. Simple filtering in query().
    """

    def __init__(self) -> None:
        # TODO: self._records: dict[int, dict] = {}
        # TODO: self._next_id = 1
        raise NotImplementedError("Implement me")

    def insert(self, record: dict[str, Any]) -> int:
        """Insert record, assign id. Return id."""
        # TODO: record["id"] = self._next_id; self._records[id] = record.copy()
        # TODO: self._next_id += 1; return id
        raise NotImplementedError("Implement me")

    def update(self, id: int, **kwargs: Any) -> None:
        """Update record by id."""
        # TODO: if id in self._records: self._records[id].update(kwargs)
        raise NotImplementedError("Implement me")

    def delete(self, id: int) -> None:
        """Remove record by id."""
        # TODO: self._records.pop(id, None)
        raise NotImplementedError("Implement me")

    def query(self, **filters: Any) -> list[dict[str, Any]]:
        """Return records matching all filters."""
        # TODO: return [r for r in self._records.values() if all(r.get(k)==v for k,v in filters.items())]
        raise NotImplementedError("Implement me")


def main() -> None:
    db = InMemoryDB()
    db.insert({"name": "a", "status": "active"})
    db.insert({"name": "b", "status": "inactive"})
    print(db.query(status="active"))


if __name__ == "__main__":
    main()
