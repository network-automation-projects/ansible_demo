# Drill 8: Implement a Simple LRU Cache

Implement an LRU cache without using `functools.lru_cache`.

## Requirements

**Base:**
- `LRUCache(capacity)` class
- `get(key)` — return value or None if not found; update access order
- `put(key, value)` — insert or update; evict least recently used if at capacity
- Use `collections.OrderedDict`

## Example

```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")  # 1
cache.put("c", 3)  # evicts "b"
cache.get("b")  # None
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
