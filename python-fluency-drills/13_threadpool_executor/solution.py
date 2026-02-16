"""
Drill 13: Write a ThreadPool Executor Tool — Reference solution.
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
    results: list[str] = []
    success = 0
    failure = 0
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(simulate_task, i): i for i in range(n)}
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                success += 1
            except Exception:
                failure += 1
    return {"success": success, "failure": failure, "results": results}


def main() -> None:
    summary = run_tasks(10)
    print("Summary:", summary)


if __name__ == "__main__":
    main()
