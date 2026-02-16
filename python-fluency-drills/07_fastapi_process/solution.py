"""
Drill 7: Async FastAPI Endpoint — Reference solution.
"""

import asyncio
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ProcessRequest(BaseModel):
    data: str
    delay: float = 0.0


@app.post("/process")
async def process(req: ProcessRequest) -> dict[str, Any]:
    await asyncio.sleep(req.delay)
    return {"status": "ok", "processed": req.data}


def main() -> None:
    print("Run: uvicorn solution:app --reload")
    print(
        "Then: curl -X POST http://localhost:8000/process "
        "-H 'Content-Type: application/json' -d '{\"data\":\"hello\",\"delay\":0.5}'"
    )


if __name__ == "__main__":
    main()
