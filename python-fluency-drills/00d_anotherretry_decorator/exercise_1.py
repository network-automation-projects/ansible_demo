"""
Drill 0d: Retry Decorator (Factory Pattern)

@retry(times=3) uses the factory pattern: retry(3) returns a decorator,
which then wraps the function. Three levels: retry → decorator → wrapper.
"""

from functools import wraps
from sys import last_exc

def retry(times):
    """Factory: returns a decorator configured with `times` attempts."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs)-> Any:
            last_exc = None
            #loop through times number of times
            for attempt in range(1, times+1):
                try: 
                    func(attempt)
            
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