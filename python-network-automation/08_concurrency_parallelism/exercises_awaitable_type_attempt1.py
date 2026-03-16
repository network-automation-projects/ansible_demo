"""
Preserving the return type from a coroutine (Callable[[], Awaitable[T]])
=======================================================================

When you pass an async function (coroutine) into a helper like with_retry(),
you want the *return type* of that coroutine to be preserved. So if you pass
a function that returns str, the result of with_retry(...) should be typed
as str, not Any.

This is done with a TypeVar T and typing the parameter as:
  coro_fn: Callable[[], Awaitable[T]]
meaning: "a callable that takes no arguments and returns an Awaitable whose
result has type T." The helper then returns T, so the type checker (and IDE)
know the result type from the coroutine you passed in.

Example:
  async def _do_summarize() -> str:
      return "summary"

  result = await with_retry(_do_summarize, ...)   # result is str, not Any
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

# --- Step 1: Declare a TypeVar ---
T = TypeVar("T")   # uncomment and use in with_retry signature


async def with_retry(
    coro_fn: Callable[[], Awaitable[T]],
    max_attempts: int = 2
    )-> T:
    """Run coro_fn(); on failure retry up to max_attempts. (min 1 attempt) Return type is T."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(max_attempts):
        try:
            result = await coro_fn()
            return result
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(0.1)


async def _do_summarize() -> str:
    """Returns str. So await with_retry(_do_summarize, ...) should be typed str."""
    await asyncio.sleep(0.01)
    return "summary"


async def _do_fetch_count() -> int:
    """Returns int. So await with_retry(_do_fetch_count, ...) should be typed int."""
    await asyncio.sleep(0.01)
    return 42


async def main() -> None:
    result_summary = await with_retry(_do_summarize)
    result_count = await with_retry(_do_fetch_count)

    print("Summary:", result_summary)
    print("Count:", result_count)

    assert isinstance(result_summary, str), "with_retry should preserve str"
    assert isinstance(result_count, int), "with_retry should preserve int"


if __name__ == "__main__":
    asyncio.run(main())
