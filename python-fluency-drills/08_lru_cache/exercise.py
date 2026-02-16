"""
Drill 8: Implement a Simple LRU Cache
Fill in the TODOs. See README.md for the problem description.
Do NOT use functools.lru_cache.
"""

from collections import OrderedDict
from typing import Any


class LRUCache:
    """
    LRU cache with get/put. Uses OrderedDict.
    Evicts least recently used when at capacity.
    """

    def __init__(self, capacity: int) -> None:
        # TODO: self._capacity = capacity
        # TODO: self._cache: OrderedDict[str, Any] = OrderedDict()
        raise NotImplementedError("Implement me")

    def get(self, key: str) -> Any | None:
        """Return value or None. Update access order."""
        # TODO: if key not in cache: return None
        # TODO: move_to_end(key) to mark as recently used
        # TODO: return value
        raise NotImplementedError("Implement me")

    def put(self, key: str, value: Any) -> None:
        """Insert or update. Evict LRU if at capacity."""
        # TODO: if key in cache: move_to_end(key)
        # TODO: cache[key] = value
        # TODO: if len > capacity: popitem(last=False)
        raise NotImplementedError("Implement me")


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
