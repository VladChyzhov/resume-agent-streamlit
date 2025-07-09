import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS documents("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "filename TEXT,"
        "file_bytes BLOB"
        ")"
    )
    return conn


def save_document(file_obj):
    """Save uploaded file object to the database."""
    if file_obj is None:
        return
    conn = get_conn()
    with conn:
        conn.execute(
            "INSERT INTO documents(filename, file_bytes) VALUES(?, ?)",
            (file_obj.name, file_obj.read()),
        )
    conn.close()


def list_documents():
    """Return list of (id, filename)."""
    conn = get_conn()
    cur = conn.execute("SELECT id, filename FROM documents ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
