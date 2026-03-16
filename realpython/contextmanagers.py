# exercises to learn context managers


import time
from contextlib import asynccontextmanager
import asyncio


# ------------------
# class based timer

import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self  # what gets bound by "as t"

    def __exit__(self, exc_type, exc, tb):
        elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {elapsed:.6f}s")
        # return False means: do NOT swallow exceptions
        return False

with Timer() as t:
    sum(range(1_000_000))

#------

class SuppressKeyError:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return exc_type is KeyError

d = {"a": 1}
with SuppressKeyError():
    print(d["missing"])  # KeyError suppressed
print("still running")

# real way
from contextlib import suppress

d = {"a": 1}
with suppress(KeyError):
    print(d["missing"])  # KeyError suppressed
print("still running")

# or

d = {"a": 1}
try:
    print(d["missing"])
except KeyError:
    pass
print("still running")

#-----

# generator based context manager from contextlib
# runs the code until yield then the code within the with 
# block executes then upon exiting of the with block code 
# either by completing or raising an exception, the context 
# manager executes the code after yield.

from contextlib import contextmanager

@contextmanager
def open_logged(path, mode="r"):
    print(f"opening {path}")
    f = open(path, mode)
    try:
        yield f
    finally:
        print(f"closing {path}")
        f.close()

with open_logged("data.txt", "w") as f:
    f.write("hello\n")


#------
# same pattern

from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.perf_counter()
    yield
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")

with timer():
    sum(range(1_000_000))

#----
# same pattern

from contextlib import contextmanager
import os

@contextmanager
def in_dir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)

with in_dir("/tmp"):
    print(os.getcwd())  # /tmp
print(os.getcwd())      # back to original


# -----
# same pattern

from contextlib import contextmanager

@contextmanager
def log_block(name):
    print(f"Entering {name}")
    try:
        yield
    finally:
        print(f"Exiting {name}")

with log_block("phase one"):
    print("doing work")


# -------
# practice

# Write Timer (context manager-based), then add:
# print whether an exception occurred (exc_type is not None)

@asynccontextmanager
async def Timer():
    start = time.perf_counter()         # 3rd
    yield start                         # 4th t is set to start
    print (f"{time.perf_counter() - start:.6f}") # 8th (runs when the body of timer is completed)

async def show_concurrent():
    for _ in range(6):
        await asyncio.sleep(0.1)
        print("  (other task running...)")

async def main():                       # runs 1st
    async with Timer() as t:            # 2nd - runs async generator up to the first yield
        task = asyncio.create_task(show_concurrent()) # 5th starts concurrent work
        await asyncio.sleep(0.5)        # 6th - this coroutine pauses here for .5s but other tasks can run
        await task                      # 6th - runs concurrent with above
        print (f"{t}")                  # 7th but only after the sleep finishes




# ------
# real example

# Many HTTP requests (e.g. httpx/aiohttp) in one handler.
# Multiple DB or cache calls.
# Reading/writing files or talking to other services.

# asyncio.gather(...) when you want to run several coroutines “in parallel” and wait for all:
# e.g. fetch from 3 APIs, then combine results.
# task = create_task(...); ... ; await task when you want to do other work while that one task runs, but still wait for it before finishing.
# async with asyncio.TaskGroup(...): (3.11+) when you want several tasks, and “if one fails, cancel the others and raise” (structured concurrency with clear lifecycle).

async def get_user_and_orders(user_id):
    task_profile = asyncio.create_task(fetch_profile(user_id))
    task_orders = asyncio.create_task(fetch_orders(user_id))
    profile, orders = await asyncio.gather(task_profile, task_orders)
    return profile, orders



# OR

async def get_user_and_orders_all(user_id):
    profile, orders = await asyncio.gather(
        fetch_profile2(user_id),   # coroutines are fine; gather wraps them
        fetch_orders2(user_id),
        return_exceptions=True
    )
    if isinstance(profile, Exception):
        pass
        # handle error
    if isinstance(orders, Exception):
        pass
        # handle error
    return profile, orders  # often you'll return (or re-raise) after handling
        
# profile and orders are either results or Exception instances
# then you check: if isinstance(profile, Exception): ...












@asynccontextmanager
async def timer_any():
    start = time.perf_counter()
    yield
    print (f"Elapsed: {time.perf_counter() - start:.6f}")


async def main():
    async with timer_any():
        await asyncio.sleep(0.1)
        

asyncio.run(main())

# -------


# Write a @contextmanager that:
# creates a temp directory and deletes it after (even on exception)
# Use ExitStack to open N files and ensure all close if an exception happens in the middle


# -------

# Implement a fake “SSH connection” object with connect/close and wrap it in a context manager