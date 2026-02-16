"""
Drill 10: Build a Basic REST Client — Reference solution.
"""

import json
import logging
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch(url: str, max_retries: int = 3, timeout: float = 3.0) -> requests.Response:
    """
    Fetch URL. Retry on 500, timeout 3s, log structured JSON.
    """
    last_resp: requests.Response | None = None
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=timeout)
        except requests.RequestException as e:
            log_entry = {"url": url, "error": str(e), "attempt": attempt + 1}
            logger.info(json.dumps(log_entry))
            if attempt < max_retries - 1:
                time.sleep(0.5)
            raise
        log_entry = {"url": url, "status": resp.status_code, "attempt": attempt + 1}
        logger.info(json.dumps(log_entry))
        if resp.status_code < 500:
            return resp
        last_resp = resp
        if attempt < max_retries - 1:
            time.sleep(0.5)
    if last_resp is not None:
        return last_resp
    raise RuntimeError("No response received")


def main() -> None:
    result = fetch("https://httpbin.org/status/200")
    print("Status:", result.status_code)


if __name__ == "__main__":
    main()
