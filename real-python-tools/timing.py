# Ready-to-use timing snippets.
# Use perf_counter for single-run, timeit for benchmarking, monotonic for clock-skew-safe duration.
# See python-from-basic-to-tools.md

import time
import timeit

# -----------------------------------------------------------------------------
# Single-run elapsed time — use perf_counter (not time.time or datetime)
# -----------------------------------------------------------------------------

# start = time.perf_counter()
# result = do_something()
# elapsed = time.perf_counter() - start
# print(f"Took {elapsed:.4f} seconds")

# -----------------------------------------------------------------------------
# Benchmarking — run code many times, get mean/std
# Use when comparing algorithms or micro-optimizing
# -----------------------------------------------------------------------------

# timeit.timeit(stmt="func()", setup="from mymodule import func", number=10000)
# Returns total seconds for 10000 runs. Divide by number for per-call average.

# timeit.repeat(stmt="func()", setup="from mymodule import func", repeat=5, number=1000)
# Returns list of 5 timings. Use min() for best run, or statistics for mean/std.

# Example:
# def fib(n):
#     return n if n < 2 else fib(n - 1) + fib(n - 2)
# t = timeit.timeit("fib(20)", globals={"fib": fib}, number=10)
# print(f"fib(20) x10: {t:.4f}s")

# -----------------------------------------------------------------------------
# Clock-skew-safe duration — use monotonic when wall clock may change
# -----------------------------------------------------------------------------

# Use when measuring intervals that must not be affected by NTP, DST, or manual clock changes.
# Common in rate limiters, timeouts, and token buckets.

# start = time.monotonic()
# ... do work ...
# elapsed = time.monotonic() - start

# Note: monotonic() values are not comparable across processes. Use perf_counter() for
# cross-process timing if needed (though both are process-specific on some platforms).
