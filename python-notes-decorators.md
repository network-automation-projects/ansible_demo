# Decorators

Decorators are functions that take a function as an argument and return a function.

**Reference:** [Udemy 100 Days of Code — Decorators](https://www.udemy.com/course/100-days-of-code/learn/quiz/6474209#overview)

---

## Basic Example

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before the function is called
        print(f"Decorator: {func.__name__}")
        result = func(*args, **kwargs)
        # Do something after the function is called
        return result
    return wrapper

@decorator
def my_function():
    print("My function")

my_function()
```

**Equivalent (without @ syntax):**

```python
my_decorated_function = decorator(my_function)
my_decorated_function()
```

**Reference:** [Udemy — Decorator syntax](https://www.udemy.com/course/100-days-of-code/learn/quiz/6474205#overview)

---

## `*args` and `**kwargs`

The single `*` and double `**` match how Python separates positional and keyword arguments.

| Symbol | Purpose |
|--------|---------|
| `*args` | Collects extra **positional** arguments into a **tuple** |
| `**kwargs` | Collects extra **keyword** arguments into a **dict** |

**Positional args** — passed by position (order), stored as a sequence:

```python
def foo(*args):
    print(args)  # tuple: (1, 2, 3)

foo(1, 2, 3)
```

**Keyword args** — passed as `name=value` pairs, stored as a mapping:

```python
def bar(**kwargs):
    print(kwargs)  # dict: {'a': 1, 'b': 2}

bar(a=1, b=2)
```

**Unpacking (same symbols):**

- `*iterable` — unpacks an iterable into positional arguments
- `**mapping` — unpacks a mapping into keyword arguments

```python
nums = (1, 2, 3)
d = {'x': 10, 'y': 20}
foo(*nums)   # same as foo(1, 2, 3)
bar(**d)     # same as bar(x=10, y=20)
```

**Summary:** `*` = positional / iterable · `**` = keyword / name-value mapping

---

# Decorators: Basic → Advanced

## 1. Core Idea

A decorator is a function that takes another function and returns a new function, usually to add behavior without changing the original's code.

---

## 2. Functions Are Values

In Python, functions are objects. You can pass them around and return them:

```python
def greet():
    return "Hello"

# Assign to a variable
f = greet
f()  # "Hello"

# Pass as argument
def call_twice(func):
    func()
    func()
call_twice(greet)

# Return from another function
def get_greeter():
    return greet
```

---

## 3. Manual Wrapping (No @)

You can wrap a function by hand:

```python
def greet(name):
    return f"Hello, {name}!"

def log_call(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

# Manually wrap
greet = log_call(greet)
greet("World")  # Before → Hello, World! → After
```

`log_call` takes `greet`, returns `wrapper`, and you replace `greet` with that wrapper.

---

## 4. The @ Syntax

`@decorator` is shorthand for "replace this function with `decorator(this_function)`":

```python
@log_call
def greet(name):
    return f"Hello, {name}!"

# Same as:
# def greet(name): ...
# greet = log_call(greet)
```

So `@log_call` means: "pass `greet` to `log_call` and assign the result back to `greet`."

---

## 5. @wraps(func) — Preserve Metadata

**Without @wraps**, the wrapper hides the original function's identity:

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_call
def greet(name):
    """Say hello."""
    return f"Hello, {name}!"

greet.__name__   # "wrapper"  ← wrong
greet.__doc__    # None       ← lost
help(greet)      # shows wrapper, not greet
```

**With @wraps**, metadata is copied from `func` to the wrapper:

```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_call
def greet(name):
    """Say hello."""
    return f"Hello, {name}!"

greet.__name__   # "greet"
greet.__doc__    # "Say hello."
```

---

## 6. Decorators With Parameters — The Factory Pattern

If you want `@retry(max_attempts=3)`, you need two layers:

1. `retry(max_attempts=3)` is called first → returns a decorator.
2. That decorator is applied to the function.

```python
def retry(max_attempts=3, delay=1.0):
    # retry() is a FACTORY — it returns a decorator
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise  # re-raise last exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1)   # parens = call retry first
def flaky():
    ...
```

**Flow:**

1. `retry(max_attempts=3, delay=0.1)` runs → returns `decorator`.
2. `decorator(flaky)` runs → returns `wrapper`.
3. `flaky` is replaced by `wrapper`.

The inner `decorator` and `wrapper` close over `max_attempts` and `delay`.

---

## 7. Parentheses: @x vs @x()

| Syntax       | What Python does      | Use when                    |
|--------------|------------------------|-----------------------------|
| `@log_call`  | `log_call(greet)`      | Decorator takes the function |
| `@retry(3)`  | `retry(3)(greet)`      | Decorator needs config first |

- **No parens:** the decorator is the function itself.
- **With parens:** the decorator is the return value of the call.

---

## 8. Multiple Decorators

Decorators are applied **bottom-to-top**:

```python
@log_call
@retry(max_attempts=3)
def flaky():
    ...
```

Equivalent to:

```python
flaky = log_call(retry(max_attempts=3)(flaky))
```

**Order of execution** when you call `flaky()`:

1. `log_call`'s wrapper runs (outer).
2. `retry`'s wrapper runs (inner).
3. Original `flaky` runs.

---

## 9. Type Hints for Decorators

**Simple (no params):**

```python
from typing import Any, Callable

def log_call(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper
```

**Advanced (preserve signature and return type):**

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

def log_call(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)
    return wrapper
```

`ParamSpec` and `TypeVar` let the type checker keep the original function's parameter and return types.

---

## 10. Class Decorators

You can decorate classes too. The decorator receives the class and returns a (possibly modified) class:

```python
def add_repr(cls):
    cls.__repr__ = lambda self: f"<{cls.__name__}>"
    return cls

@add_repr
class Foo:
    pass

Foo()  # <Foo>
```

---

## 11. Common Pitfalls

**Mutable default in a factory:**

```python
def bad(cache=[]):  # shared across all calls!
    cache.append(1)
    return cache
```

**Forgetting to return the wrapper:**

```python
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # BUG: no return wrapper!
```

**Decorating a method and losing `self`:**  
Using `*args, **kwargs` and forwarding them correctly (as in the examples above) avoids this.

---

## 12. Quick Reference

| Concept              | Idea |
|----------------------|------|
| Basic decorator      | `func → wrapper`; use `@decorator` |
| Factory              | `(config) → decorator`; use `@decorator()` |
| `@wraps`             | Copy metadata from original to wrapper |
| `*args, **kwargs`    | Forward any arguments to the wrapped function |
| Closure              | Inner functions capture outer variables |
| ParamSpec / TypeVar  | Preserve types for type checkers |

---

## Your Drills in This Progression

| Drill                    | Focus |
|--------------------------|-------|
| `00b_simple_decorator`   | Basic decorator, no params, `@wraps` |
| `01_retry_decorator/simple` | Factory pattern, params, closure over config |
| `01_retry_decorator` (main) | Same idea plus ParamSpec/TypeVar for typing |

---

# AI/ML Backend: Common Decorator Patterns

In backend AI/ML work, these decorator patterns are most common:

## 1. Retry With Exponential Backoff

Used for LLM APIs, embeddings, and other external calls that can fail transiently.

- **Libraries:** tenacity, stamina, LangChain's `create_base_retry_decorator`
- **Why:** Rate limits, timeouts, and 5xx errors are common; retries with backoff reduce failures
- **Typical config:** Max attempts (often 3–6), exponential backoff, retry only on specific exceptions (e.g. `RateLimitError`, `APIConnectionError`, `ServiceUnavailableError`)

```python
# tenacity example
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=60))
def call_llm(prompt: str) -> str:
    ...
```

## 2. Caching / Memoization

Used for embeddings, repeated prompts, and expensive model calls.

- **Patterns:** `@lru_cache`, Redis-backed cache, semantic cache
- **Why:** Cuts cost and latency for repeated inputs
- **Typical config:** Cache key from inputs, TTL, in-memory vs distributed

```python
@lru_cache(maxsize=1000)
def get_embedding(text: str) -> list[float]:
    ...
```

## 3. Observability / Tracing

Used for logging, tracing, and metrics around model calls.

- **Libraries:** Langfuse `@observe()`, OpenTelemetry, custom decorators
- **Why:** Track latency, token usage, costs, and errors
- **Typical config:** Log inputs/outputs, timing, token counts, error rates

```python
@observe()
def call_model(prompt: str) -> str:
    ...
```

## 4. Rate Limiting

Used when calling APIs with strict rate limits.

- **Patterns:** Token bucket, sliding window, per-user limits
- **Why:** Avoid hitting provider limits and getting blocked
- **Typical config:** Max calls per second/minute, optional queuing

---

## Summary: AI/ML Decorator Patterns

| Pattern       | Use case              | Typical library / approach      |
|---------------|------------------------|---------------------------------|
| Retry         | Flaky LLM/API calls    | tenacity, stamina               |
| Caching       | Repeated embeddings/prompts | lru_cache, Redis, semantic cache |
| Observability | Tracing, cost, latency | Langfuse, OpenTelemetry         |
| Rate limiting | Respecting API limits  | Custom or ratelimit             |

Retry with exponential backoff is the most widely used pattern, since LLM and API calls are inherently unreliable. Caching and observability are next in importance for cost and debugging.
