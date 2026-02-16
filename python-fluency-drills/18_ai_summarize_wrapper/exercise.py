"""
Drill 18: Build a Mini AI Wrapper
Fill in the TODOs. See README.md for the problem description.
Mock the LLM call. Add timeout, retry, structured logging.
"""

import json
import logging
import random
import time

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
    # TODO: Loop with retries
    # TODO: Use threading or signal for timeout (or asyncio.wait_for if async)
    # TODO: Log {"action": "summarize", "text_len": len(text), "attempt": N, "status": "ok"|"retry"|"failed"}
    # TODO: Call _mock_llm_call, return result
    raise NotImplementedError("Implement me")


def main() -> None:
    result = summarize("This is a long text that should be summarized.")
    print("Result:", result)


if __name__ == "__main__":
    main()
