"""
Drill 10: Build a Basic REST Client
Fill in the TODOs. See README.md for the problem description.
Requires: pip install requests
"""

import json
import logging
import time

# TODO: import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch(url: str, max_retries: int = 3, timeout: float = 3.0):
    """
    Fetch URL. Retry on 500, timeout 3s, log structured JSON.
    """
    # TODO: for attempt in range(max_retries):
    # TODO:   resp = requests.get(url, timeout=timeout)
    # TODO:   log {"url": url, "status": resp.status_code, "attempt": attempt+1}
    # TODO:   if resp.status_code < 500: return resp
    # TODO:   time.sleep(0.5)  # before retry
    # TODO: return resp (or raise)
    raise NotImplementedError("Implement me")


def main() -> None:
    # Use httpbin for testing
    result = fetch("https://httpbin.org/status/200")
    print("Status:", result.status_code)


if __name__ == "__main__":
    main()
