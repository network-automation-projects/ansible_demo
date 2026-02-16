"""
Drill 5: Build a Simple Job Queue
Fill in the TODOs. See README.md for the problem description.
"""

from collections.abc import Callable
from typing import Any


class JobQueue:
    """
    Simple job queue. add_job() to enqueue, run_next() to execute.
    Track success, failure, retry count.
    """

    def __init__(self) -> None:
        # TODO: Initialize queue (list or deque) and stats
        raise NotImplementedError("Implement me")

    def add_job(self, job: Callable[[], Any] | dict[str, Any]) -> None:
        """Add a job. Job can be callable or dict with 'task' key (callable)."""
        # TODO: Append job to queue
        raise NotImplementedError("Implement me")

    def run_next(self) -> Any:
        """Run the next job. Return result or re-raise exception."""
        # TODO: Pop next job, execute, update stats
        # TODO: On success: increment success; on exception: increment failure, re-raise
        raise NotImplementedError("Implement me")

    def stats(self) -> dict[str, int]:
        """Return {"success": N, "failure": N, "retry": N}."""
        # TODO: Return current stats
        raise NotImplementedError("Implement me")


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
