"""
Retry with requests — the "real way" for HTTP calls.

requests uses urllib3 under the hood. Retries are configured via
urllib3.util.retry.Retry + requests.adapters.HTTPAdapter, then
mounted on a Session. All HTTP calls through that session get
automatic retries on connection errors and (optionally) status codes.

This is HTTP-specific: it retries failed connections, timeouts,
and configurable status codes (500, 502, 503, 504).
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session_with_retries(
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: tuple[int, ...] = (500, 502, 503, 504),
) -> requests.Session:
    """
    Create a requests Session with retry behavior.
    Retries on connection errors and on the given status codes.
    """
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def main() -> None:
    session = make_session_with_retries(max_retries=3, backoff_factor=0.5)

    # 1. Normal request — succeeds, no retries needed
    print("1. GET https://httpbin.org/get")
    resp = session.get("https://httpbin.org/get", timeout=10)
    resp.raise_for_status()
    print(f"   Status: {resp.status_code}, OK\n")

    # 2. Request to endpoint that always returns 503 — retries then gives up
    print("2. GET https://httpbin.org/status/503 (always fails)")
    try:
        resp = session.get("https://httpbin.org/status/503", timeout=10)
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"   After retries: {e}\n")

    # 3. Use the session for any HTTP call — retries are automatic
    print("3. Any session.get/post uses the same retry config")
    resp = session.get("https://httpbin.org/headers", timeout=10)
    resp.raise_for_status()
    print(f"   Status: {resp.status_code}, OK")


if __name__ == "__main__":
    main()
