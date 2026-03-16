# Part C — Embeddings (chunk → vector)
# Real embedding API (best, if you have it)
# Implement embeddings_client.py:
# async def embed_texts(texts: list[str]) -> list[list[float]]
# Use env vars:
# EMBED_BASE_URL
# EMBED_API_KEY
# EMBED_MODEL
# Add timeout, retries (reuse Phase 2 patterns)

# Verbiage will use the local model for embedding (privacy)

import os
import asyncio
import random
import logging

from app.config import EMBED_BASE_URL, EMBED_MODEL, EMBED_TIMEOUT, EMBED_MAX_ATTEMPTS 

import httpx

from app.errors import (
    LLMRateLimitedError,
    LLMUpstreamTimeoutError,
    LLMServiceError,
)

logger = logging.getLogger(__name__)



async def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of texts in one batched request. Returns one vector per text, same order.
    Uses timeout and retries (exponential backoff + jitter) on rate limit / timeout.
    """
    if not texts:
        return []

    # if not EMBED_API_KEY:     #Ollama doesn't require key
    #     raise LLMServiceError("EMBED_API_KEY is not set")

    last_exc: BaseException | None = None
    for attempt in range(EMBED_MAX_ATTEMPTS):
        try:
            async with httpx.AsyncClient(timeout=EMBED_TIMEOUT) as client:
                response = await client.post(
                    f"{EMBED_BASE_URL}/api/embed",             #Ollama; openai chatgpt uses /embeddings",
                    headers={
                        # "Authorization": f"Bearer {EMBED_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": EMBED_MODEL,
                        "input": texts,
                    },
                )
            if response.status_code == 429:
                raise LLMRateLimitedError("Embedding API rate limited")
            if response.status_code >= 400:
                raise LLMServiceError(
                    f"Embedding API error {response.status_code}: {response.text[:200]}"
                )
            data = response.json()
        except httpx.TimeoutException as e:
            # last_exc = LLMUpstreamTimeoutError("Embedding request timed out") from e      # this version of python didn't like this exception chaining. We will figure that out later.
            last_exc = LLMUpstreamTimeoutError("Embedding request timed out")
            if attempt < EMBED_MAX_ATTEMPTS - 1:
                delay = 1.0 * (2**attempt)
                jitter = random.uniform(0, delay * 0.5)
                await asyncio.sleep(delay + jitter)
            else:
                raise last_exc
            continue
        except (LLMRateLimitedError, LLMUpstreamTimeoutError) as e:
            last_exc = e
            if attempt < EMBED_MAX_ATTEMPTS - 1:
                delay = 1.0 * (2**attempt)
                jitter = random.uniform(0, delay * 0.5)
                await asyncio.sleep(delay + jitter)
            else:
                raise
            continue
        except LLMServiceError:
            raise
        break
    else:
        if last_exc:
            raise last_exc
        raise RuntimeError("Embedding retries exhausted")

    # data["data"] is list of {"embedding": [...], "index": 0, ...}; preserve order
        # Ollama: {"embeddings": [[...], ...]} or {"embedding": [...]} for single input
    if data.get("embeddings"):
        return data["embeddings"]
    if data.get("embedding") is not None:
        return [data["embedding"]]
    raise LLMServiceError("Unexpected embed response shape")

    
    # if data["data"]:
    #     # using chatgpt
    #     by_index = {item["index"]: item["embedding"] for item in data["data"]}
    #     return [by_index[i] for i in range(len(texts))]  
    # if data["embeddings"]:
    #     # using Ollama
    #     return data["embeddings"]
    # if "embedding" in data:
    #     return [data["embedding"]]
    # raise LLMServiceError("Unexpected embed response shape")        #if we get here, nothing worked



