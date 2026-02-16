"""
Drill 17: Write a Simple Background Worker — Reference solution.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Literal

TaskStatus = Literal["pending", "running", "done", "failed"]


class BackgroundWorker:
    """
    Submit tasks, run in background, poll status.
    Uses ThreadPoolExecutor.
    """

    def __init__(self) -> None:
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._tasks: dict[str, Any] = {}
        self._next_id = 0
        self._lock = threading.Lock()

    def submit(self, task: Any) -> str:
        """Submit task. Return task_id."""
        with self._lock:
            task_id = str(self._next_id)
            self._next_id += 1
            future = self._executor.submit(self._run_task, task_id, task)
            self._tasks[task_id] = {"future": future, "status": "pending"}
        return task_id

    def _run_task(self, task_id: str, task: Any) -> None:
        self._tasks[task_id]["status"] = "running"
        try:
            task()
            self._tasks[task_id]["status"] = "done"
        except Exception:
            self._tasks[task_id]["status"] = "failed"

    def get_status(self, task_id: str) -> TaskStatus:
        """Return status: pending, running, done, failed."""
        with self._lock:
            if task_id not in self._tasks:
                return "failed"
            return self._tasks[task_id]["status"]

    def all_done(self) -> bool:
        """Return True if all tasks finished."""
        with self._lock:
            return all(
                t["status"] in ("done", "failed") for t in self._tasks.values()
            )


def main() -> None:
    def slow_task() -> str:
        time.sleep(0.2)
        return "ok"

    worker = BackgroundWorker()
    ids = [worker.submit(slow_task) for _ in range(3)]
    while not worker.all_done():
        for tid in ids:
            print(tid, worker.get_status(tid))
        time.sleep(0.05)
    print("All done")


if __name__ == "__main__":
    main()
