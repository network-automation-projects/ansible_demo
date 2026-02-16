"""
Drill 20: Mini Automation Service — Reference solution.
"""

import argparse
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)
tasks: dict[str, dict] = {}


class TaskSubmit(BaseModel):
    task: str


class TaskConfig(BaseModel):
    task: str


@app.post("/submit")
async def submit(req: TaskSubmit) -> dict:
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {"status": "pending", "result": None}

    def run_task() -> None:
        try:
            time.sleep(0.2)
            tasks[task_id]["status"] = "done"
            tasks[task_id]["result"] = f"Processed: {req.task}"
        except Exception as e:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = str(e)

    executor.submit(run_task)
    logger.info("Submitted task %s", task_id)
    return {"task_id": task_id}


@app.get("/status/{task_id}")
async def status(task_id: str) -> dict:
    if task_id not in tasks:
        return {"error": "not found"}
    return tasks[task_id]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("run", nargs="?", default=None)
    args = parser.parse_args()
    if args.run == "run" or not args.run:
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
