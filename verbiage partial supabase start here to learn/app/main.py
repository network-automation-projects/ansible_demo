## 8. POST /ingest

# Wire the ingest endpoint: validate the request body with your Pydantic model;
#  chunk the `text` with your chunking function; insert one row into the documents
#  table; insert one row per chunk into the chunks table (build chunk id from docid:chunkindex); call your embedder for all
#  chunk texts; insert one row per chunk into the embeddings table; return your 
# ingest response. Decide and document: if `doc_id` already exists, do you return
#  an error (e.g. 409) or overwrite? If embedding fails after you’ve written 
# documents/chunks, do you roll back or leave partial data? Prefer “reject duplicate
#  doc_id” and “roll back or don’t persist on embed failure” so the DB stays 
# consistent.

# **Why now:** This is the first end-to-end flow: text in, chunks and embeddings 
# stored. Getting it right here makes the rest of the app usable.

# **Hint:** You can use a single transaction (begin, insert doc + chunks + embeddings,
#  commit) and roll back on any failure, or explicitly delete the document and its 
# chunks if embedding fails. Document your choice in a comment or in `code-notes.md`.

## 9. POST /ask

# Wire the ask endpoint: validate the request; embed the question with the same embedder 
# you use for chunks; call your retrieval function to get top-k chunks; build a prompt 
# that includes a short system instruction (e.g. “You suggest report verbiage based on 
# the following context”), the user’s question, and a “Context:” section with the 
# retrieved chunks (include doc_id and maybe chunk_id so the model can refer to sources). 
# Call your LLM with that prompt and return the model’s answer plus the list of top chunks 
# (and optionally scores/snippets). Cap the total context length (e.g. character or token
#  limit) so you don’t exceed model limits. If retrieval returns no chunks, either return 
# a message like “I don’t have relevant context” or call the LLM without context and say 
# so in the prompt.

# **Why now:** This completes the RAG loop: question → embed → retrieve → prompt 
# with context → LLM → answer. Verbiage’s value is “ask for overview/detail wording 
# and get it from similar reports.”

# **Hint:** Reuse your ai-document LLM client or a minimal async caller; point it at 
# **Ollama** (e.g. `http://localhost:11434`) and use **Llama 3.1 8B** (`llama3.1:8b`) 
# so all generation stays local for client-name privacy. Keep the prompt template in 
# one place so you can tune it later for “overview and detailed image verbiage.” 
# Next phase: **LLaVA** (Ollama) for “look at this job’s images and write report text.”

## 10. GET /documents (list ingested)

# Add an endpoint that returns a list of what has already been ingested so users can 
# see what’s in the system (confirm uploads, spot duplicates, scan by title). Implement
#  **GET /documents** (or **GET /ingest** if you prefer) that queries the documents table
#  and returns a list of items. Each item should include at least: `doc_id`, `title`, 
# `source`, `created_at`, and `num_chunks`. Optionally include a short `snippet` (e.g. 
# first 200–300 characters of the document text, or of the first chunk’s content) so users
#  get a quick preview. Define a Pydantic response model (e.g. `DocumentSummary` with those
#  fields) and a list response (e.g. `DocumentsListResponse` with `documents: 
# list[DocumentSummary]`). Add a DB helper that selects from `documents` and optionally 
# joins with the first chunk per doc for the snippet; keep the query simple (e.g. order 
# by `created_at` desc).


from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import asyncio
import time
import logging
import json


from app.db import create_db, delete_by_doc_id, insert_chunk, insert_document, insert_embedding, doc_exist, list_documents
from app.models import (
    AskRequest,
    AskResponse,
    ChunkingOptions,
    DocumentSummary,
    DocumentsListResponse,
    IngestGoogleDriveRequest,
    IngestGoogleDriveResponse,
    IngestRequest,
    IngestResponse,
)
from app.rate_limit import TokenBucket
from app.chunking import chunk_text_chars
from app.embeddings import HttpEmbedder
from app.job_store import JobStore
from app.worker import worker_loop
from app.retrieval import retrieve_top_k
from app.errors import LLMRateLimitedError, LLMServiceError, LLMTimeoutError, LLMUpstreamTimeoutError
from app.drive_client import list_and_export_docs, DriveClientError
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)
from app import llm_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app):

    # create db
    app.state.db_path = "documentsdb.sqlite"

    newdb = sqlite3.connect(app.state.db_path)
    # app.state.db_conn = create_db(newdb)      concurrency issues since the documents fetch is on a separate thread
    conn = create_db(newdb)
    conn.close()            # we don't need the connection right now, other areas will grab their conn based on the path 

    ### to do - create job store
    app.state.job_store = JobStore()
    job_store = app.state.job_store

    #create token bucket
    app.state.rate_limiter = TokenBucket()
    rate_limiter = app.state.rate_limiter

    #create task loop - worker will poll for pending jobs and process them.
    task = asyncio.create_task(worker_loop(job_store, rate_limiter))
    logger.info("Work Started")

    yield
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError as e:
        pass

    conn.close()
    logger.info("Work has stopped")


# create the web service and async life cycle thingy
app = FastAPI(lifespan=lifespan)


async def ingest_text(
    conn: sqlite3.Connection,
    doc_id: str,
    title: str | None,
    source: str | None,
    text: str,
    chunking_options: ChunkingOptions,
) -> IngestResponse:
    """
    Shared ingest: chunk text, insert document + chunks, embed, insert embeddings, commit.
    Raises ValueError('doc_id already exists') if doc_id is duplicate.
    Rollback (delete_by_doc_id) on embedding failure.
    """
    if doc_exist(conn, doc_id):
        raise ValueError("doc_id already exists")
    opts = chunking_options
    chunks = chunk_text_chars(text, opts.chunk_size, opts.chunk_overlap)
    insert_document(conn, doc_id, int(time.time()), title, source)
    for chunk in chunks:
        chunk_id = f"{doc_id}:{chunk.chunk_index}"
        insert_chunk(
            conn, chunk_id, doc_id, chunk.chunk_index, chunk.content,
            chunk.start_offset, chunk.end_offset,
        )
    embedder = HttpEmbedder()
    try:
        vectors = await embedder.embed_many([c.content for c in chunks])
    except Exception as e:
        delete_by_doc_id(conn, doc_id)
        logger.exception("embedding failed", exc_info=e)
        raise
    for chunk, vector in zip(chunks, vectors):
        chunk_id = f"{doc_id}:{chunk.chunk_index}"
        insert_embedding(conn, chunk_id, embedder.model, json.dumps(vector), embedder.dim)
    conn.commit()
    return IngestResponse(
        doc_id=doc_id,
        num_chunks=len(chunks),
        embedding_model=embedder.model,
        dim=embedder.dim,
    )


@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: Request, ingest_request: IngestRequest):
    with sqlite3.connect(request.app.state.db_path) as conn:
        try:
            return await ingest_text(
                conn,
                ingest_request.doc_id,
                ingest_request.title,
                ingest_request.source,
                ingest_request.text,
                ingest_request.chunking_options,
            )
        except ValueError as e:
            if "already exists" in str(e):
                raise HTTPException(
                    status_code=409,
                    detail="doc_id (document title) already exists. Use a different doc_id or delete the existing document first.",
                ) from e
            raise
        except Exception as e:
            raise HTTPException(status_code=503, detail="Embedding failed") from e


@app.post("/ingest/google-drive", response_model=IngestGoogleDriveResponse)
async def ingest_google_drive(request: Request, body: IngestGoogleDriveRequest):
    """
    Ingest Google Docs from Drive (read-only). List/export then run shared ingest per doc.
    Duplicate doc_id is skipped and counted; other errors are recorded and processing continues.
    """
    try:
        docs = list_and_export_docs(folder_id=body.folder_id, file_ids=body.file_ids)
    except DriveClientError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    default_opts = ChunkingOptions()
    ingested = 0
    skipped = 0
    errors: list[str] = []
    doc_ids: list[str] = []
    with sqlite3.connect(request.app.state.db_path) as conn:
        for doc in docs:
            try:
                await ingest_text(
                    conn,
                    doc.doc_id,
                    doc.title,
                    doc.source,
                    doc.text,
                    default_opts,
                )
                ingested += 1
                doc_ids.append(doc.doc_id)
            except ValueError as e:
                if "already exists" in str(e):
                    skipped += 1
                else:
                    errors.append(f"{doc.doc_id} ({doc.title}): {e}")
            except Exception as e:
                errors.append(f"{doc.doc_id} ({doc.title}): {e}")
                logger.warning("Ingest failed for %s: %s", doc.doc_id, e)
    return IngestGoogleDriveResponse(
        ingested=ingested,
        skipped=skipped,
        errors=errors,
        doc_ids=doc_ids,
    )


@app.post("/ask", response_model= AskResponse)
async def ask(request: Request, ask_request: AskRequest):
     # full RAG Flow
    with sqlite3.connect(request.app.state.db_path) as conn:

        rate_limiter = request.app.state.rate_limiter
        embedder = HttpEmbedder()
        embedder.embed_many([ask_request.question])

        query_vectors = await embedder.embed_many([ask_request.question])      #body.question is a str but embed many expects a list of strings, so we enclose it in []
        query_vec = query_vectors[0]

        top_chunks = retrieve_top_k(conn,query_vec,ask_request.top_k, ask_request.doc_id)
        
        # Build prompt for llm from top_chunks (cap context size), then call LLM (a string that we pass that includes a system instruction, context and the question itself)
        MAX_CONTEXT_CHARS = 8000   # cap so you don't overflow the LLM
        context_parts = []
        total_len = 0
        if not top_chunks:
            answer = "I don't have relevant context to answer that question."
            return AskResponse(answer, top_chunks=[])
        else:
            for c in top_chunks:
                block = f"[doc_id={c.doc_id} chunk_id={c.chunk_id}]\n{c.content_snippet}\n"
                if total_len + len(block) > MAX_CONTEXT_CHARS:
                    break                       
                context_parts.append(block)
                total_len += len(block)
            
            context_str = "\n".join(context_parts) if context_parts else "(No relevant context found.)"
            prompt = (
                "Answer using only the context below. If the context doesn't contain enough information, say so.\n\n"
                "Context:\n" + context_str + "\n\n"
                "Question: " + ask_request.question
            )
            await rate_limiter.acquire()
            answer = await llm_client.answer_with_context(prompt)

            return AskResponse(answer=answer, top_chunks=top_chunks)

@app.get("/documents", response_model=DocumentsListResponse)
def get_documents(request: Request):
    with sqlite3.connect(request.app.state.db_path) as conn:

        rows = list_documents(conn)
        documents = [
            DocumentSummary(
                doc_id=r[0],
                title=r[1],
                source=r[2],
                created_at=r[3],
                num_chunks=r[4],
                snippet=r[5],
            )
            for r in rows
        ]
        return DocumentsListResponse(documents=documents)


@app.get("/health")
def health():
    return {"healthy": True}


@app.exception_handler(LLMTimeoutError)
async def timeout_handler(request: Request, exc: LLMTimeoutError):
    return JSONResponse(
        status_code=504,
        content={"detail": "LLM request timed out"},
    )

@app.exception_handler(LLMUpstreamTimeoutError)
async def timeout_handler(request: Request, exc: LLMUpstreamTimeoutError):
    return JSONResponse(
        status_code=504,
        content={"detail": "LLM request timed out"},
    )


@app.exception_handler(LLMServiceError)
async def service_error_handler(request: Request, exc: LLMServiceError):
    return JSONResponse(
        status_code=503,
        content={"detail": "LLM service unavailable"},
    )

@app.exception_handler(LLMRateLimitedError)
async def service_error_handler(request: Request, exc: LLMRateLimitedError):
    return JSONResponse(
        status_code=429,
        content={"detail": "LLM rate limit issue."},
    )


def _google_flow():
    """Build OAuth flow for Drive read-only (state will be set per-request)."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set")
    from google_auth_oauthlib.flow import Flow

    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_REDIRECT_URI],
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
        redirect_uri=GOOGLE_REDIRECT_URI,
    )


@app.get("/auth/google")
async def auth_google(request: Request):
    """
    Start one-time OAuth: redirect to Google consent (Drive read-only).
    After approval, user is sent to /auth/google/callback.
    """
    try:
        flow = _google_flow()
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="false",
    )
    response = RedirectResponse(url=auth_url, status_code=302)
    response.set_cookie(key="oauth_state", value=state, max_age=600, httponly=True)
    return response


@app.get("/auth/google/callback", response_class=HTMLResponse)
async def auth_google_callback(request: Request):
    """
    OAuth callback: exchange code for tokens, show refresh token to set in .env.
    """
    state_cookie = request.cookies.get("oauth_state")
    state_query = request.query_params.get("state")
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback")
    if not state_cookie or state_cookie != state_query:
        raise HTTPException(status_code=400, detail="Invalid or missing state")
    try:
        flow = _google_flow()
        flow._state = state_query
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        logger.exception("OAuth fetch_token failed: %s", e)
        raise HTTPException(status_code=503, detail="Token exchange failed") from e
    refresh_token = flow.credentials.refresh_token
    if not refresh_token:
        raise HTTPException(
            status_code=503,
            detail="No refresh token; try revoking app access and re-authorizing with prompt=consent",
        )
    response = HTMLResponse(
        content=f"""
        <html><body style="font-family: sans-serif; padding: 2rem;">
        <h1>Google Drive auth complete</h1>
        <p>Add this to your <code>.env</code> (or set the env var):</p>
        <pre style="background: #eee; padding: 1rem; overflow-x: auto;">GOOGLE_REFRESH_TOKEN={refresh_token!r}</pre>
        <p>You already have <code>GOOGLE_CLIENT_ID</code> and <code>GOOGLE_CLIENT_SECRET</code> set (required for this flow).</p>
        <p>Then restart the app and use <b>POST /ingest/google-drive</b> to sync.</p>
        </body></html>
        """
    )
    response.delete_cookie("oauth_state")
    return response


# Serve frontend (tabs + documents drawer); 
# mount last so API routes take precedence
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

