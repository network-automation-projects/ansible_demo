"""
Drill 17: Write a Simple Background Worker
Fill in the TODOs. See README.md for the problem description.
"""

import asyncio
import time
from typing import Any, Literal

TaskStatus = Literal["pending", "running", "done", "failed"]


class BackgroundWorker:
    """
    Submit tasks, run in background, poll status.
    Use asyncio or threading.
    """

    def __init__(self) -> None:
        # TODO: self._tasks: dict[str, ...] = {}
        # TODO: self._next_id = 0
        raise NotImplementedError("Implement me")

    def submit(self, task) -> str:
        """Submit task. Return task_id."""
        # TODO: Create task_id, schedule task, store future/thread
        # TODO: Return task_id
        raise NotImplementedError("Implement me")

    def get_status(self, task_id: str) -> TaskStatus:
        """Return status: pending, running, done, failed."""
        # TODO: Check future/thread state
        raise NotImplementedError("Implement me")

    def all_done(self) -> bool:
        """Return True if all tasks finished."""
        # TODO: Check all tasks
        raise NotImplementedError("Implement me")


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
