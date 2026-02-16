"""
Drill 18: Build a Mini AI Wrapper — Reference solution.
"""

import json
import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _mock_llm_call(text: str) -> str:
    """Simulate LLM: 20% fail, else return truncated summary."""
    time.sleep(0.05)
    if random.random() < 0.2:
        raise RuntimeError("Mock LLM failure")
    return text[:50] + "..." if len(text) > 50 else text


def summarize(text: str, timeout: float = 2.0, max_retries: int = 3) -> str:
    """
    Summarize text. Mock LLM call with timeout, retry, structured logging.
    """
    executor = ThreadPoolExecutor(max_workers=1)
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        log_entry = {
            "action": "summarize",
            "text_len": len(text),
            "attempt": attempt + 1,
        }
        try:
            future = executor.submit(_mock_llm_call, text)
            result = future.result(timeout=timeout)
            log_entry["status"] = "ok"
            logger.info(json.dumps(log_entry))
            return result
        except (RuntimeError, FuturesTimeoutError) as e:
            last_exc = e
            log_entry["status"] = "retry" if attempt < max_retries - 1 else "failed"
            log_entry["error"] = str(e)
            logger.info(json.dumps(log_entry))
            if attempt >= max_retries - 1:
                break
    executor.shutdown(wait=False)
    if last_exc:
        raise last_exc
    raise RuntimeError("Max retries exceeded")


def main() -> None:
    result = summarize("This is a long text that should be summarized.")
    print("Result:", result)


if __name__ == "__main__":
    main()
