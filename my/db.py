from __future__ import annotations
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "resume.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS documents(\n"
            "  id INTEGER PRIMARY KEY,\n"
            "  filename TEXT,\n"
            "  file_bytes BLOB\n"
            ")"
        )
        conn.commit()


def save_document(file_obj) -> None:
    """Save uploaded file object to the database."""
    if not file_obj:
        return
    data = file_obj.getvalue()
    filename = file_obj.name
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO documents(filename, file_bytes) VALUES (?, ?)",
            (filename, data),
        )
        conn.commit()


def list_documents() -> list[tuple[int, str]]:
    """Return list of saved documents (id, filename)."""
    with get_connection() as conn:
        cur = conn.execute("SELECT id, filename FROM documents ORDER BY id")
        return cur.fetchall()


# Initialize database when module is imported
init_db()
