"""
Drill 20: Mini Automation Service
Fill in the TODOs. See README.md for the problem description.
Combines: CLI, Pydantic, retry, logging, background worker, async endpoint.
"""

import argparse
import logging
from pathlib import Path

# TODO: from fastapi import FastAPI
# TODO: from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: class TaskConfig(BaseModel):
#     task: str


# TODO: app = FastAPI()
# TODO: task_queue = ...
# TODO: @app.post("/submit")
# TODO: @app.get("/status/{task_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("run", nargs="?", default=None)
    args = parser.parse_args()
    # TODO: if args.run == "run": uvicorn.run(app, ...)
    logger.info("Run: uvicorn exercise:app --reload (after implementing)")


if __name__ == "__main__":
    main()
