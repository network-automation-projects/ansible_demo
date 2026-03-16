"""
Drill 0d: Retry Decorator (Factory Pattern)

@retry(times=3) uses the factory pattern: retry(3) returns a decorator,
which then wraps the function. Three levels: retry → decorator → wrapper.
"""


def retry(times):
    """Factory: returns a decorator configured with `times` attempts."""


            #loop through times number of times

            #try to run the function (in this mock scenario, the function itself has the number of times set to fail until the 3rd try)

            # All attempts exhausted — re-raise the last exception




count = {"n": 0}

@retry(times=3)
def flaky():
    count["n"] += 1
    if count["n"] < 3:
        raise ValueError("not yet")
    return "ok"

print(flaky())
# Expected: "attempt 1 failed: not yet" and "attempt 2 failed: not yet", then "ok"