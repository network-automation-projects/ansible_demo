# llm_client.py
# has an async answer with context function

'''**Hint:** Reuse your ai-document LLM client or a minimal async caller; 
point it at **Ollama** (e.g. `http://localhost:11434`) and use 
**Llama 3.1 8B** (`llama3.1:8b`) so all generation stays local for 
client-name privacy. Keep the prompt template in one place so you can 
tune it later for “overview and detailed image verbiage.” Next phase: **LLaVA** 
(Ollama) for “look at this job’s images and write report text.”'''

import os
import httpx
from httpx import TimeoutException
import random

import asyncio
from app.errors import LLMRateLimitedError, LLMServiceError, LLMUpstreamTimeoutError
from app.config import LLM_MODEL, LLM_TIMEOUT_SECONDS, LLM_BASE_URL, LLM_MAX_ATTEMPTS



async def answer_with_context(prompt: str)->str:
    """Call OpenAI chat completions with the RAG prompt; return the assistant reply."""
    
    last_exc: BaseException | None = None
    for attempt in range(LLM_MAX_ATTEMPTS):
    
        try:
            async with httpx.AsyncClient(timeout=LLM_TIMEOUT_SECONDS) as client:
                resp = await client.post(
                    url = f"{LLM_BASE_URL.rstrip('/')}/api/chat",
                    json={
                        "model": LLM_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False
                    },
                )
            if resp.status_code == 429:
                raise LLMRateLimitedError("LLM rate limited")
            if resp.status_code >= 400:
                raise LLMServiceError(f"LLM API error {resp.status_code}: {resp.text[:200]}")
            data = resp.json()
            
            text = data.get("message", {}).get("content", "").strip()

            return text

        except (LLMServiceError):
            raise



        except httpx.TimeoutException as e:
            # last_exc = LLMUpstreamTimeoutError("Embedding request timed out") from e      # this version of python didn't like this exception chaining. We will figure that out later.
            last_exc = LLMUpstreamTimeoutError("Embedding request timed out")
            if attempt < LLM_MAX_ATTEMPTS - 1:
                delay = 1.0 * (2**attempt)
                jitter = random.uniform(0, delay * 0.5)
                await asyncio.sleep(delay + jitter)
            else:
                raise last_exc
            continue
        except (LLMRateLimitedError, LLMUpstreamTimeoutError) as e:
            last_exc = e
            if attempt < LLM_MAX_ATTEMPTS - 1:
                delay = 1.0 * (2**attempt)
                jitter = random.uniform(0, delay * 0.5)
                await asyncio.sleep(delay + jitter)
            else:
                raise
            continue



    else:
        if last_exc:
            raise last_exc
        raise RuntimeError("Embedding retries exhausted attempting to reach llm client")

    

