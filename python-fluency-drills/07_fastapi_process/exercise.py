"""
Drill 7: Async FastAPI Endpoint
Fill in the TODOs. See README.md for the problem description.
Requires: pip install fastapi uvicorn pydantic
"""

import asyncio
from typing import Any

# TODO: from fastapi import FastAPI
# TODO: from pydantic import BaseModel


# TODO: class ProcessRequest(BaseModel):
#     data: str
#     delay: float = 0.0


# TODO: app = FastAPI()


# TODO: @app.post("/process")
# async def process(req: ProcessRequest) -> dict[str, Any]:
#     await asyncio.sleep(req.delay)
#     return {"status": "ok", "processed": req.data}


def main() -> None:
    # Run with: uvicorn exercise:app --reload
    print("Run: uvicorn exercise:app --reload")
    print("Then: curl -X POST http://localhost:8000/process -H 'Content-Type: application/json' -d '{\"data\":\"hello\",\"delay\":0.5}'")


if __name__ == "__main__":
    main()
