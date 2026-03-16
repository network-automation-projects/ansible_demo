# Ready-to-use retry snippets.
# Prefer tenacity over manual try/except loops. See python-from-basic-to-tools.md

# Requires: pip install tenacity

# -----------------------------------------------------------------------------
# Basic retry with exponential backoff
# -----------------------------------------------------------------------------

# from tenacity import retry, stop_after_attempt, wait_exponential
#
#
# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
# def fetch_data(url: str):
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# -----------------------------------------------------------------------------
# Retry only on specific exceptions
# -----------------------------------------------------------------------------

# from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
#
#
# @retry(
#     retry=retry_if_exception_type((ConnectionError, TimeoutError)),
#     stop=stop_after_attempt(5),
#     wait=wait_exponential(multiplier=1, min=2, max=60),
# )
# def call_api():
#     ...

# -----------------------------------------------------------------------------
# With jitter (adds randomness to avoid thundering herd)
# -----------------------------------------------------------------------------

# from tenacity import retry, wait_exponential_jitter
#
#
# @retry(wait=wait_exponential_jitter(initial=1, max=60))
# def unreliable_operation():
#     ...
