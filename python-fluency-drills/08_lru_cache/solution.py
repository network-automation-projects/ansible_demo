"""
Drill 8: Implement a Simple LRU Cache — Reference solution.
"""

from collections import OrderedDict
from typing import Any


class LRUCache:
    """
    LRU cache with get/put. Uses OrderedDict.
    Evicts least recently used when at capacity.
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Any | None:
        """Return value or None. Update access order."""
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: str, value: Any) -> None:
        """Insert or update. Evict LRU if at capacity."""
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)


def main() -> None:
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    print(cache.get("a"))
    cache.put("c", 3)
    print(cache.get("b"))
    print(cache.get("c"))


if __name__ == "__main__":
    main()
