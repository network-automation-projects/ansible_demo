"""Preserving coroutine return type — solution."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def with_retry(
    coro_fn: Callable[[], Awaitable[T]],
    max_attempts: int = 2,
) -> T:
    """Run coro_fn(); on failure retry up to max_attempts. Return type is T."""
    last_exc = None
    for attempt in range(max_attempts):
        try:
            result = await coro_fn()
            return result
        except Exception as e:
            last_exc = e
            if attempt == max_attempts - 1: # last attempt
                raise
            await asyncio.sleep(0.1)
    raise last_exc or RuntimeError("retry exhausted")


async def _do_summarize() -> str:
    await asyncio.sleep(0.01)
    return "summary"


async def _do_fetch_count() -> int:
    await asyncio.sleep(0.01)
    return 42


async def main() -> None:
    result_summary = await with_retry(_do_summarize)  # type: str
    result_count = await with_retry(_do_fetch_count)  # type: int

    print("Summary:", result_summary)
    print("Count:", result_count)

    assert isinstance(result_summary, str)
    assert isinstance(result_count, int)


if __name__ == "__main__":
    asyncio.run(main())
