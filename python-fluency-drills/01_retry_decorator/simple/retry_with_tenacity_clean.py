"""
Retry with tenacity — the "real way" for any callable.

tenacity is a general-purpose retry library. It works on any function,
not just HTTP. You decorate with @retry(...) and configure stop
conditions, wait strategy, and which exceptions to retry.

Same conceptual task as the custom decorator, but production-ready.
"""


def main...


    # Same pattern as custom @retry(max_attempts=3, delay=0.05)