"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import List, Callable, Any, Dict
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_parallel_tasks(tasks: List[Callable], max_workers: int = 5) -> List[Any]:
    """Run tasks in parallel using ThreadPoolExecutor. Raises if any task raises."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda f: f(), tasks))
    return results


async def async_fetch_device_data(device: str) -> Dict[str, Any]:
    """Async function to fetch device data."""
    await asyncio.sleep(1)
    return {'device': device, 'data': 'mock'}


async def fetch_multiple_devices(devices: List[str]) -> List[Dict[str, Any]]:
    """Fetch data from multiple devices concurrently."""
    return await asyncio.gather(*[async_fetch_device_data(d) for d in devices])



def _dummy_task_1():
    """Sync callable used by run_parallel_tasks."""
    return "task1"


def _dummy_task_2():
    return "task2"


async def main() -> None:
    # -------------------------------------------------------------------------
    # 1) Sync parallel execution (ThreadPoolExecutor)
    # -------------------------------------------------------------------------
    # run_parallel_tasks RUNS each callable in a thread; it does not await.
    # We pass a list of callables; executor.map(lambda f: f(), tasks) invokes
    # each f() in a worker thread and blocks until all are done.
    tasks = [_dummy_task_1, _dummy_task_2, lambda: "task3"]
    try:
        parallel_results = run_parallel_tasks(tasks, max_workers=5)
        print("run_parallel_tasks result:", parallel_results)
    except Exception as e:
        logger.exception("Parallel tasks failed")
        parallel_results = []  # or retry, or sys.exit(1), etc.

    # -------------------------------------------------------------------------
    # 2) Single async fetch (one coroutine)
    # -------------------------------------------------------------------------
    # async_fetch_device_data(device) creates a coroutine; it doesn't run until
    # we await it. Here we await it, so the event loop RUNS that coroutine,
    # which internally awaits asyncio.sleep(1) then returns the dict.
    single_device = await async_fetch_device_data("router1")
    print("async_fetch_device_data (single):", single_device)


    # -------------------------------------------------------------------------
    # 3) Multiple async fetches (concurrent via gather)
    # -------------------------------------------------------------------------
    # fetch_multiple_devices builds a list of coroutines (one per device) and
    # passes them to asyncio.gather(). We await gather, so the event loop
    # RUNS all those coroutines concurrently; this main() awaits until every
    # async_fetch_device_data(d) has finished.
    devices = ["router1", "switch1", "firewall1"]
    multiple_devices = await fetch_multiple_devices(devices)
    print("fetch_multiple_devices:", multiple_devices)


if __name__ == "__main__":
    # asyncio.run() creates an event loop, RUNS the main() coroutine until it
    # completes (so every await inside main is driven by the loop), then
    # closes the loop. No top-level await here—asyncio.run does the "run".
    asyncio.run(main())



# if __name__ == "__main__":
#     print("08_concurrency_parallelism – answer key (run exercises.py to practice)")
