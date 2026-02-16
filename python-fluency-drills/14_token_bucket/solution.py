"""
Drill 14: Implement Basic Token Bucket Rate Limiter — Reference solution.
"""

import time


class TokenBucket:
    """
    Token bucket: rate tokens per second.
    acquire() consumes 1 token; returns True if available, False if empty.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self.rate = rate
        self.capacity = capacity if capacity is not None else rate
        self.tokens = self.capacity
        self.last_refill = time.monotonic()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now

    def acquire(self) -> bool:
        """Consume 1 token. Return True if available, False if empty."""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def main() -> None:
    bucket = TokenBucket(rate=2.0)
    for _ in range(4):
        print(bucket.acquire())
    time.sleep(0.6)
    print(bucket.acquire())


if __name__ == "__main__":
    main()
