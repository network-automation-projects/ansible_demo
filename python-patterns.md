# Python Patterns

## wrapper functions    

wrapper functions are functions that take in a function as an argument and return a function.

they are used to add behavior to a function without changing the original function.

example:
def wrapper(func):
    def wrapper(*args, **kwargs):
        #do something before the function is called
        print(f"Wrapper: {func.__name__}")
        #do something after the function is called
        return func(*args, **kwargs)
    return wrapper

## decorators
decorators are functions that take in a function as an argument and return a function.

they are used to add behavior to a function without changing the original function.

example:
def decorator(func):
    def wrapper(*args, **kwargs):
        #do something before the function is called
        print(f"Decorator: {func.__name__}")
        #do something after the function is called
        return func(*args, **kwargs)
    return wrapper

@decorator


# most decorators are wrappers, but not all.

Decorators that wrap — Most decorators take a function and return a new function that does extra work and then calls the original. Those are wrappers:

def retry(fn):
    def inner(*args, **kwargs):
        # extra behavior
        return fn(*args, **kwargs)
    return inner  # returns a wrapper

Decorators that don’t wrap — Some decorators only do side effects or metadata and return the original function:

def register(fn):
    REGISTRY.append(fn)
    return fn   # returns the original, no wrapping

@register
def my_func():
    pass

    So: decorators that add behavior around the original are wrappers. Decorators that only register, annotate, or do similar side effects are not wrappers.



# coroutines

A coroutine is still the same function; the difference is how it runs.
Regular function call: result = foo() runs the function, blocks until it finishes, and returns the result.
Async function call: coro = bar() creates a coroutine object. Nothing has run yet. When you await coro, the event loop runs it in a cooperative way: it can pause at await points and let other coroutines run, then resume later.
So a coroutine is that function’s execution represented as something the event loop can start, pause, and resume. It’s the same code, but with a non-blocking, cooperative execution model instead of blocking the whole thread.



# asyncio

await — Runs any coroutine and waits for it to finish. No time limit; it can block indefinitely.

vs

asyncio.wait_for(awaitable, timeout=seconds) — Runs the awaitable with a timeout. If it doesn’t finish in time, it cancels it and raises asyncio.TimeoutError.

await = run and wait
wait_for = run and wait, but only up to a given number of seconds.