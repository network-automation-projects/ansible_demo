"""
Drill 1: Retry Decorator (Simple — no ParamSpec/TypeVar)
Fill in the TODOs. See README.md for the problem description.

- `@retry(max_attempts=3, delay=1)` — decorator with configurable max attempts and delay
- Retry the function when it raises an exception
- Stop after `max_attempts` attempts
- Re-raise the final exception if all attempts fail

"""



def :
    """
    Decorator that retries a function on exception.
    Stops after max_attempts and re-raises the final exception.
    """

    def :
        
        def :
            # TODO: Implement retry loop
            # - Call func(*args, **kwargs)
            # - On exception: sleep(delay), retry
            # - Use exponential backoff if use_exponential_backoff: delay *= 2 each retry
            # - After max_attempts, re-raise last exception
            raise NotImplementedError("Implement me")

        return wrapper

    return decorator


def :


    
    result = flaky()
    print("Result:", result)
    print("Calls:", call_count)


if 
