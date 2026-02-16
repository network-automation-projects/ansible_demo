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
    """Run tasks in parallel using ThreadPoolExecutor."""
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


if __name__ == "__main__":
    print("08_concurrency_parallelism – answer key (run exercises.py to practice)")
