## Config and environment

# Small config module that reads from the environment: things like database path, 
# embedding model name and (if you use a remote API) base URL and API key. 
# Use sensible defaults where safe (e.g. a local SQLite path); never default secrets. 
# Keep config in one place so the rest of the app doesn’t touch `os.environ` directly.

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # Load .env into os.environ; no-op override if Docker already set vars

# Database: SQLite (local) or Postgres (Supabase)
# - For SQLite: set DATABASE_PATH (default verbiage.db). Leave DATABASE_URL unset/empty.
# - For Postgres/Supabase: set DATABASE_URL to the Postgres connection string from
#   Project Settings → Database → "Connection string" (choose URI). It looks like:
#   postgresql://postgres.[ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
#   (This is not the project URL https://xxx.supabase.co — that's for the JS client.)
#   Use pooler port 6543 for short-lived connections; use with psycopg2 or asyncpg.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()  # No default; empty = use SQLite

# SQLite path (used only when DATABASE_URL is empty)
DB_PATH = os.getenv("DATABASE_PATH", "verbiage.db")

EMBED_BASE_URL = os.getenv("EMBED_BASE_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
# EMBED_API_KEY = "" # optional for local Ollama; don’t default it. The client should only require it when you’re not using local (e.g. only require it when base URL is not localhost, or allow empty for local).
EMBED_TIMEOUT = int(os.getenv("EMBED_TIMEOUT", 30))
EMBED_MAX_ATTEMPTS = int(os.getenv("EMBED_MAX_ATTEMPTS", 3))

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", 60))
LLM_MAX_ATTEMPTS = int(os.getenv("LLM_MAX_ATTEMPTS", 3))
LLM_TOKEN_LIMIT = int(os.getenv("LLM_TOKEN_LIMIT", 10))
LLM_RATE_LIMIT_SECONDS = int(os.getenv("LLM_RATE_LIMIT_SECONDS", 60))

# Google Drive (read-only ingest). No defaults for secrets.
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN", "")
# Callback URL for one-time OAuth (must match value in Google Cloud Console).
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

# old settings if we want to switch to chatgpt:
# so the full embedding URL used by the client becomes http://localhost:11434/api/embeddings (base + path in code).
# EMBED_BASE_URL = os.getenv("EMBED_BASE_URL", "https://api.openai.com/v1").rstrip("/")
# EMBED_API_KEY = os.getenv("EMBED_API_KEY", "")
# EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
# EMBED_TIMEOUT = float(os.getenv("EMBED_TIMEOUT", "30"))
# EMBED_MAX_ATTEMPTS = int(os.getenv("EMBED_MAX_ATTEMPTS", "3"))
