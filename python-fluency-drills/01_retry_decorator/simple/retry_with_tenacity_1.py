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
    def flaky()->str:



if __name__ == "__main__":
    main()