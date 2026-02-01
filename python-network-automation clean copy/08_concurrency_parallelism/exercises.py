"""
Python Network Automation - Concurrency & Parallelism Exercises
"""

from typing import List, Callable, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In production: import threading, multiprocessing, asyncio
# from concurrent.futures import ThreadPoolExecutor


def run_parallel_tasks(tasks: List[Callable], max_workers: int = 5) -> List[Any]:
    """Run tasks in parallel using ThreadPoolExecutor."""
    # TODO: Use ThreadPoolExecutor(max_workers=max_workers)
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     results = list(executor.map(lambda f: f(), tasks))
    # return results
    pass


async def async_fetch_device_data(device: str) -> Dict[str, Any]:
    """Async function to fetch device data."""
    # TODO: Use asyncio.sleep() for async delay
    # await asyncio.sleep(1)
    # return {'device': device, 'data': 'mock'}
    pass


async def fetch_multiple_devices(devices: List[str]) -> List[Dict[str, Any]]:
    """Fetch data from multiple devices concurrently."""
    # TODO: Use asyncio.gather() to run async_fetch_device_data concurrently
    # return await asyncio.gather(*[async_fetch_device_data(d) for d in devices])
    pass


if __name__ == "__main__":
    print("Concurrency & Parallelism Exercises")
