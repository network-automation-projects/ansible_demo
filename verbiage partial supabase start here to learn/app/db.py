## 4. Database schema and a small DB layer

# Design the SQLite schema: tables for **documents** 
# (e.g. `doc_id`, `title`, `source`, `created_at`), 
# **chunks** (e.g. `chunk_id`, `doc_id`, `chunk_index`, 
# `content`, `start_offset`, `end_offset`), and **embeddings** 
# (e.g. `chunk_id`, `model`, `vector_json`, `dim`). 
# 
# Add indexes that support “get chunks by doc_id” and 
# “get embedding by chunk_id.” Implement a thin DB module 
# that opens the DB, creates tables if they don’t exist, 
# and exposes a few helpers (e.g. insert document, insert chunks, 
# insert embeddings, fetch embeddings for retrieval). 
# Keep it synchronous and simple unless you already know you want async.

# can use app.state.dbconn for db conn since we will create that in main right before we call create db

import sqlite3
import json

def create_db(conn: sqlite3.Connection) -> sqlite3.Connection:
    #conn = app.state.dbconn    # sqlite3.connect("documentsdb.sqlite")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            title TEXT,
            source TEXT,
            created_at INTEGER
        )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY,
        doc_id TEXT,
        chunk_index INTEGER,
        content TEXT,
        start_offset INTEGER,
        end_offset INTEGER
        )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        chunk_id TEXT PRIMARY KEY,
        model TEXT,
        vector_json TEXT,
        dim INTEGER
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_doc_id_chunk_index ON chunks(doc_id, chunk_index)
    """)

    conn.commit()

    return conn

# CRUD

def insert_document(conn,
    doc_id: str,
    created_at: int,
    title: str | None = None,
    source: str | None = None,
    )->None:
    conn.execute("INSERT INTO documents(doc_id, title, source, created_at) VALUES (?,?,?,?)", (doc_id, title, source, created_at),)


def insert_chunk(conn: sqlite3.Connection, 
    chunk_id: str,
    doc_id: str,
    chunk_index: int,
    content: str,
    start_offset: int,
    end_offset: int
    ) -> None:
    conn.execute("INSERT INTO chunks(chunk_id, doc_id, chunk_index, content, start_offset, end_offset) VALUES (?,?,?,?,?,?)", (chunk_id, doc_id, chunk_index, content, start_offset, end_offset),)
    # conn.commit()

def insert_embedding(conn: sqlite3.Connection, 
    chunk_id: str,
    model: str,
    vector_json: str,
    dim: int
    ) -> None:
    conn.execute("INSERT INTO embeddings(chunk_id, model, vector_json, dim) VALUES (?,?,?,?)", (chunk_id, model, vector_json, dim),)
    # conn.commit()

def doc_exist(
    conn: sqlite3.Connection,
    doc_id: str
    )->None:
    '''returns none if doc does not exist.  if it's a duplicate, raises 409'''
    cursor = conn.execute("SELECT 1 FROM documents WHERE doc_id = ?", (doc_id,))
    return cursor.fetchone() is not None        # returns True if it finds one?

def get_embeddings_for_retrieval(conn, doc_id=None)->list[tuple]:
    sql = """
    SELECT e.chunk_id, c.doc_id, e.vector_json, c.content
    FROM embeddings e
    JOIN chunks c ON e.chunk_id = c.chunk_id
    """
    if doc_id is not None:
        cursor = conn.execute(sql + " WHERE c.doc_id = ?", (doc_id,))
    else:
        cursor = conn.execute(sql)
    rows = cursor.fetchall()
    return [
        (chunk_id, doc_id, json.loads(vector_json), content)
        for chunk_id, doc_id, vector_json, content in rows
    ]


def delete_by_doc_id(conn: sqlite3.Connection, doc_id: str) -> None:
    conn.execute("DELETE FROM embeddings WHERE chunk_id IN (SELECT chunk_id FROM chunks WHERE doc_id = ?)", (doc_id,))
    conn.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
    conn.execute("DELETE FROM documents WHERE doc_id = ?", (doc_id,))
    conn.commit()


def list_documents(conn: sqlite3.Connection, snippet_max_len: int = 250) -> list[tuple]:
    """
    Returns list of (doc_id, title, source, created_at, num_chunks, snippet).
    snippet is first chunk content truncated to snippet_max_len; None if no chunks.
    Ordered by created_at desc.
    """
    sql = """
    SELECT
        d.doc_id,
        d.title,
        d.source,
        d.created_at,
        (SELECT COUNT(*) FROM chunks c WHERE c.doc_id = d.doc_id) AS num_chunks,
        (SELECT c.content FROM chunks c WHERE c.doc_id = d.doc_id ORDER BY c.chunk_index LIMIT 1) AS first_content
    FROM documents d
    ORDER BY d.created_at DESC
    """
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    result = []
    for doc_id, title, source, created_at, num_chunks, first_content in rows:
        snippet = None
        if first_content:
            snippet = first_content[:snippet_max_len] + ("..." if len(first_content) > snippet_max_len else "")
        result.append((doc_id, title, source, created_at, num_chunks, snippet))
    return result


