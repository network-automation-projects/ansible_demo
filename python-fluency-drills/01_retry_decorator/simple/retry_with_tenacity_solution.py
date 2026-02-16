"""
Retry with tenacity — the "real way" for any callable.

tenacity is a general-purpose retry library. It works on any function,
not just HTTP. You decorate with @retry(...) and configure stop
conditions, wait strategy, and which exceptions to retry.

Same conceptual task as the custom decorator, but production-ready.
"""

from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential


def main() -> None:
    call_count = 0

    # Same pattern as custom @retry(max_attempts=3, delay=0.05)
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(0.05))
    def flaky() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Simulated failure")
        return "ok"

    print("1. Basic retry (3 attempts, 0.05s fixed wait)")
    result = flaky()
    print(f"   Result: {result}, Calls: {call_count}\n")

    # With exponential backoff (like use_exponential_backoff=True)
    call_count2 = 0

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.1, min=0.1, max=2.0),
    )
    def flaky_backoff() -> str:
        nonlocal call_count2
        call_count2 += 1
        if call_count2 < 4:
            raise ConnectionError("Simulated failure")
        return "ok"

    print("2. Retry with exponential backoff")
    result = flaky_backoff()
    print(f"   Result: {result}, Calls: {call_count2}\n")

    print("3. Works for any callable — HTTP, DB, file I/O, etc.")


if __name__ == "__main__":
    main()
