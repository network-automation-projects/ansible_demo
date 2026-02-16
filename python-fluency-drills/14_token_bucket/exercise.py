"""
Drill 14: Implement Basic Token Bucket Rate Limiter
Fill in the TODOs. See README.md for the problem description.
"""

import time


class TokenBucket:
    """
    Token bucket: rate tokens per second.
    acquire() consumes 1 token; returns True if available, False if empty.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        # TODO: self.rate = rate, self.tokens = capacity or rate
        # TODO: self.last_refill = time.monotonic()
        raise NotImplementedError("Implement me")

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        # TODO: now = time.monotonic()
        # TODO: elapsed = now - self.last_refill
        # TODO: self.tokens = min(capacity, self.tokens + elapsed * self.rate)
        # TODO: self.last_refill = now
        raise NotImplementedError("Implement me")

    def acquire(self) -> bool:
        """Consume 1 token. Return True if available, False if empty."""
        # TODO: _refill()
        # TODO: if self.tokens >= 1: self.tokens -= 1; return True
        # TODO: return False
        raise NotImplementedError("Implement me")


def main() -> None:
    bucket = TokenBucket(rate=2.0)
    for _ in range(4):
        print(bucket.acquire())
    time.sleep(0.6)
    print(bucket.acquire())


if __name__ == "__main__":
    main()
