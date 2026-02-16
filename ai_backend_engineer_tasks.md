# Backend AI Systems Engineer: Coding Tasks & Concepts

A list of tasks you need to be able to **code and fully understand** for the Backend Engineer – AI Systems & Automation role. Each task is actionable, mapped to the job description, and organized by domain.

**Source:** [job_description.md](job_description.md)

---

## Suggested Learning Path

1. **Foundations** → Python & Async (Section 1)
2. **APIs** → FastAPI (Section 2) → External API Integration (Section 3)
3. **Resilience** → Retry, rate limiting, circuit breaker (Section 4)
4. **Infrastructure** → Background jobs (Section 5), Databases (Section 15)
5. **AI Integration** → Document ingestion & embeddings (Section 6) → RAG (Section 7)
6. **Production readiness** → Caching (Section 9), Observability (Section 10), Security (Section 11), Cost optimization (Section 12)
7. **Quality & deployment** → Testing (Section 13), Docker (Section 14)

---

## 1. Python & Async Foundations

*Job: "Experience with asynchronous programming (async/await)"*

- [ ] Write async functions with `async/await` and run them with `asyncio`
- [ ] Use `asyncio.gather()` to run multiple coroutines concurrently
- [ ] Build a simple async HTTP client (e.g. with `httpx`) that makes concurrent requests
- [ ] Explain when to use `async def` vs `def` and when blocking calls break the event loop

**Concepts to understand:** Event loop, coroutines, I/O-bound vs CPU-bound, GIL.

**Related:** [python-network-automation/08_concurrency_parallelism](python-network-automation/08_concurrency_parallelism/)

---

## 2. REST APIs with FastAPI

*Job: "Design and implement Python-based backend services using FastAPI or similar frameworks"*

- [ ] Create a FastAPI app with GET and POST endpoints
- [ ] Use Pydantic models for request/response validation
- [ ] Add path parameters, query parameters, and request bodies
- [ ] Implement dependency injection (e.g. shared DB client, config)
- [ ] Add OpenAPI docs and test endpoints with the built-in Swagger UI
- [ ] Return proper HTTP status codes (200, 201, 400, 404, 500) and structured error responses

**Concepts to understand:** REST semantics, request lifecycle, middleware.

**Related:** [python-fluency-drills/07_fastapi_process](python-fluency-drills/07_fastapi_process/), [python-network-automation/12_advanced_patterns](python-network-automation/12_advanced_patterns/)

---

## 3. External API Integration

*Job: "Integrate external AI APIs (LLMs, embeddings, speech-to-text, etc.) into production systems"*

- [ ] Call an external REST API (e.g. OpenAI, Anthropic, or a mock) with `httpx` or `requests`
- [ ] Parse JSON responses and handle pagination
- [ ] Implement request timeouts and connection pooling
- [ ] Use environment variables for API keys and base URLs
- [ ] Handle rate limits (429) and transient errors (5xx) with retries

**Concepts to understand:** Idempotency, backoff strategies, connection reuse.

**Related:** [python-fluency-drills/10_rest_client](python-fluency-drills/10_rest_client/), [python-network-automation/05_api_integration](python-network-automation/05_api_integration/)

---

## 4. Resilience Patterns

*Job: "Add retry logic, rate limiting, caching, and error handling to AI calls" / "Experience implementing retry/backoff and resilience patterns"*

- [ ] Implement retry logic with exponential backoff and jitter (stdlib or tenacity)
- [ ] Add rate limiting to outbound API calls (e.g. token bucket or sliding window)
- [ ] Implement circuit breaker pattern for failing external services
- [ ] Add timeouts to all external calls and fail fast with clear errors

**Concepts to understand:** Degradation, fallbacks, cascading failures.

**Related:** [python-fluency-drills/01_retry_decorator](python-fluency-drills/01_retry_decorator/), [python-fluency-drills/02_rate_limiter](python-fluency-drills/02_rate_limiter/), [python-fluency-drills/11_backoff_function](python-fluency-drills/11_backoff_function/)

---

## 5. Background Job Processing

*Job: "Design asynchronous job processing systems (background workers, task queues)"*

- [ ] Build a simple in-memory job queue (add job, run next, mark success/failure)
- [ ] Use Celery or RQ to process tasks in a background worker
- [ ] Use asyncio-based workers (e.g. ARQ, Celery with gevent) for async tasks
- [ ] Persist job state and support retries on failure
- [ ] Design a workflow where an API enqueues a job and returns a job ID for status polling

**Concepts to understand:** At-least-once vs exactly-once delivery, idempotent handlers.

**Related:** [python-fluency-drills/05_job_queue](python-fluency-drills/05_job_queue/), [python-fluency-drills/17_background_worker](python-fluency-drills/17_background_worker/)

---

## 6. Document Ingestion & Embeddings

*Job: "Build document ingestion pipelines (chunking, embedding, indexing, retrieval)"*

- [ ] Chunk a long document (by character count, sentence, or semantic boundaries)
- [ ] Call an embeddings API (OpenAI, Cohere, or local model) to get vector representations
- [ ] Store embeddings with metadata (source, chunk ID) in a simple structure (dict, SQLite)
- [ ] Implement a basic similarity search (cosine similarity) over stored embeddings

**Concepts to understand:** Embedding space, dimensionality, chunk overlap.

---

## 7. RAG (Retrieval-Augmented Generation)

*Job: "Implement Retrieval-Augmented Generation (RAG) workflows" / "Experience building RAG systems" (nice to have)*

- [ ] Build a minimal RAG pipeline: ingest document → chunk → embed → index
- [ ] Given a user query, embed it, retrieve top-k similar chunks, and pass them as context to an LLM
- [ ] Format a prompt with retrieved context and handle token limits
- [ ] Compare responses with and without RAG to understand the value

**Concepts to understand:** Context window, prompt engineering, hallucination reduction.

---

## 8. Vector Databases (Nice to Have)

*Job: "Familiarity with vector databases (pgvector, Pinecone, Weaviate, etc.)"*

- [ ] Use pgvector or a simple vector DB (e.g. Chroma, LanceDB) to store and query embeddings
- [ ] Perform approximate nearest neighbor (ANN) search
- [ ] Understand trade-offs: in-memory vs persisted, scalability, cost

**Concepts to understand:** ANN vs exact search, indexing strategies.

---

## 9. Caching

*Job: "Add retry logic, rate limiting, caching..." / "Experience with caching systems (Redis)"*

- [ ] Cache LLM or embedding API responses with Redis (or in-memory for learning)
- [ ] Define cache keys (e.g. hash of prompt + model)
- [ ] Set TTLs and handle cache invalidation
- [ ] Measure latency and cost savings with vs without cache

**Concepts to understand:** Cache key design, cache stampede, invalidation strategies.

**Related:** [python-fluency-drills/08_lru_cache](python-fluency-drills/08_lru_cache/)

---

## 10. Observability & Monitoring

*Job: "Implement structured logging, metrics, and monitoring for AI services" / "Experience monitoring APIs with Prometheus/Grafana"*

- [ ] Add structured logging (JSON format) with request IDs and correlation
- [ ] Emit metrics (request count, latency, error rate) compatible with Prometheus
- [ ] Add health check endpoints (`/health`, `/ready`)
- [ ] Trace a request through API → worker → external API and log at each step

**Concepts to understand:** Log levels, cardinality, alerting thresholds.

**Related:** [python-network-automation/07_monitoring_observability](python-network-automation/07_monitoring_observability/)

---

## 11. Security & Secrets

*Job: "Manage API keys and secrets securely"*

- [ ] Load API keys from environment variables (never hardcode)
- [ ] Use a secrets manager pattern (e.g. AWS Secrets Manager, Vault) or `.env` for local dev
- [ ] Validate and sanitize user inputs before sending to AI APIs
- [ ] Implement basic auth or API key auth for internal endpoints

**Concepts to understand:** Principle of least privilege, injection risks.

---

## 12. Cost & Performance Optimization

*Job: "Optimize performance and cost of AI inference workflows" / "Understanding of cost optimization for API-based AI systems"*

- [ ] Count tokens before calling an LLM (using tiktoken or similar)
- [ ] Implement streaming responses for LLM endpoints to reduce perceived latency
- [ ] Batch embedding requests when possible
- [ ] Add cost tracking (tokens × price) and log or metric it

**Concepts to understand:** Token pricing models, context window costs.

**Related:** [python-fluency-drills/18_ai_summarize_wrapper](python-fluency-drills/18_ai_summarize_wrapper/)

---

## 13. Testing

*Job: "Write unit and integration tests"*

- [ ] Write unit tests with pytest for core logic (chunking, retry, parsing)
- [ ] Mock external API calls in tests
- [ ] Write integration tests for a FastAPI endpoint (TestClient)
- [ ] Test error paths: timeout, 429, 500, malformed response

**Concepts to understand:** Arrange-Act-Assert, test isolation, coverage vs confidence.

**Related:** [python-fluency-drills/19_unit_tests](python-fluency-drills/19_unit_tests/)

---

## 14. Docker & Deployment

*Job: "Familiarity with Docker and CI/CD pipelines"*

- [ ] Dockerize a FastAPI app with a multi-stage build
- [ ] Run the app and a worker (e.g. Celery) in separate containers
- [ ] Use docker-compose to orchestrate app, worker, Redis, and PostgreSQL
- [ ] Add a simple CI pipeline (e.g. GitHub Actions) that runs tests and builds the image

**Concepts to understand:** Layer caching, non-root user, health checks in containers.

---

## 15. Databases

*Job: "Experience with PostgreSQL or NoSQL databases"*

- [ ] Connect to PostgreSQL with asyncpg or SQLAlchemy (async)
- [ ] Define a simple schema for jobs, embeddings, or audit logs
- [ ] Use a vector extension (pgvector) for embedding storage and similarity search
- [ ] Understand when to use relational vs document/NoSQL for AI use cases

**Concepts to understand:** Connection pooling, migrations, indexing.

**Related:** [python-fluency-drills/15_in_memory_db](python-fluency-drills/15_in_memory_db/)

---

## Self-Assessment Checklist

For each task above, ask yourself:

| Question | Use when |
|----------|----------|
| **Can I code this from scratch without looking at docs?** | Core tasks (Sections 1–5, 13) |
| **Can I explain it to a colleague in 2 minutes?** | All tasks |
| **Have I built a small project that uses it?** | Sections 2, 3, 5, 6, 7 |
| **Do I know the failure modes and how to handle them?** | Sections 3, 4, 5, 10 |

---

## Summary by Job Requirement

| Job requirement | Primary sections |
|-----------------|------------------|
| Python proficiency | 1 |
| REST APIs (FastAPI) | 2 |
| Async programming | 1, 2, 5 |
| External API integration | 3, 4 |
| Document pipelines, RAG | 6, 7, 8 |
| Background task processing | 5 |
| Retry, rate limiting, caching | 4, 9 |
| Logging, metrics, monitoring | 10 |
| Secrets management | 11 |
| Cost optimization | 12 |
| Unit and integration tests | 13 |
| Docker and CI/CD | 14 |
| PostgreSQL / NoSQL | 15 |
| Vector databases | 8 |
