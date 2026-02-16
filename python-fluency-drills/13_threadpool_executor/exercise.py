"""
Drill 13: Write a ThreadPool Executor Tool
Fill in the TODOs. See README.md for the problem description.
"""

import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def simulate_task(task_id: int) -> str:
    """Simulate a task. Some fail (raise), some succeed."""
    time.sleep(0.05)
    if random.random() < 0.3:
        raise RuntimeError(f"Task {task_id} failed")
    return f"result-{task_id}"


def run_tasks(n: int = 10) -> dict:
    """
    Run n tasks with ThreadPoolExecutor.
    Return {"success": N, "failure": N, "results": [...]}
    """
    # TODO: with ThreadPoolExecutor() as ex:
    # TODO:   futures = {ex.submit(simulate_task, i): i for i in range(n)}
    # TODO:   for future in as_completed(futures): get result or exception
    # TODO:   aggregate success/failure/results
    raise NotImplementedError("Implement me")


def main() -> None:
    summary = run_tasks(10)
    print("Summary:", summary)


if __name__ == "__main__":
    main()
