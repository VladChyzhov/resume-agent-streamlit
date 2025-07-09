from __future__ import annotations
import sqlite3
from pathlib import Path
import os

# Для документов
DB_PATH_DOCS = Path(__file__).parent / "resume.db"

# Для персональных данных
DB_PATH_PERSONAL = os.path.join(os.path.dirname(__file__), 'user_data.db')


# ==== DOCUMENTS (файлы) ====

def get_connection_docs() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH_DOCS)

def init_db_docs():
    with get_connection_docs() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS documents(\n"
            "  id INTEGER PRIMARY KEY,\n"
            "  filename TEXT,\n"
            "  file_bytes BLOB\n"
            ")"
        )
        conn.commit()

def save_document(file_obj) -> None:
    if not file_obj:
        return
    data = file_obj.getvalue()
    filename = file_obj.name
    with get_connection_docs() as conn:
        conn.execute(
            "INSERT INTO documents(filename, file_bytes) VALUES (?, ?)",
            (filename, data),
        )
        conn.commit()

def list_documents() -> list[tuple[int, str]]:
    with get_connection_docs() as conn:
        cur = conn.execute("SELECT id, filename FROM documents ORDER BY id")
        return cur.fetchall()

# ==== PERSONAL INFO ====

def init_db_personal():
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS personal_info(
            name TEXT,
            email TEXT,
            phone TEXT,
            photo BLOB
        )
        """
    )
    conn.commit()
    conn.close()

def save_personal_info(name: str, email: str, phone: str, photo_bytes: bytes | None):
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute("DELETE FROM personal_info")
    cur.execute(
        "INSERT INTO personal_info (name, email, phone, photo) VALUES (?, ?, ?, ?)",
        (name, email, phone, photo_bytes),
    )
    conn.commit()
    conn.close()

def load_personal_info():
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "SELECT name, email, phone, photo FROM personal_info LIMIT 1"
    )
    row = cur.fetchone()
    conn.close()
    return row

# ==== ИНИЦИАЛИЗАЦИЯ ====
init_db_docs()
init_db_personal()

