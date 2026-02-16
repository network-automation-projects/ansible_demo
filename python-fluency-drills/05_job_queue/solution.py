"""
Drill 5: Build a Simple Job Queue — Reference solution.
"""

from collections import deque
from collections.abc import Callable
from typing import Any


class JobQueue:
    """
    Simple job queue. add_job() to enqueue, run_next() to execute.
    Track success, failure, retry count.
    """

    def __init__(self) -> None:
        self._queue: deque[Callable[[], Any]] = deque()
        self._success = 0
        self._failure = 0
        self._retry = 0

    def add_job(self, job: Callable[[], Any] | dict[str, Any]) -> None:
        """Add a job. Job can be callable or dict with 'task' key (callable)."""
        if callable(job):
            self._queue.append(job)
        elif isinstance(job, dict) and "task" in job:
            self._queue.append(job["task"])
        else:
            raise ValueError("Job must be callable or dict with 'task' key")

    def run_next(self) -> Any:
        """Run the next job. Return result or re-raise exception."""
        if not self._queue:
            raise IndexError("No jobs in queue")
        task = self._queue.popleft()
        try:
            result = task()
            self._success += 1
            return result
        except Exception:
            self._failure += 1
            raise

    def stats(self) -> dict[str, int]:
        """Return {"success": N, "failure": N, "retry": N}."""
        return {"success": self._success, "failure": self._failure, "retry": self._retry}


def main() -> None:
    queue = JobQueue()
    queue.add_job(lambda: 1 + 1)
    queue.add_job(lambda: 1 / 0)
    print(queue.run_next())
    try:
        queue.run_next()
    except ZeroDivisionError:
        print("Caught expected error")
    print("Stats:", queue.stats())


if __name__ == "__main__":
    main()
