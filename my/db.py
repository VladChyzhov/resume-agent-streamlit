from __future__ import annotations
import sqlite3
from pathlib import Path
import os
import hashlib

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
            "  user_id INTEGER,\n"
            "  filename TEXT,\n"
            "  file_bytes BLOB\n"
            ")"
        )
        conn.commit()

def save_document(file_obj, user_id: int) -> None:
    if not file_obj:
        return
    data = file_obj.getvalue()
    filename = file_obj.name
    with get_connection_docs() as conn:
        conn.execute(
            "INSERT INTO documents(user_id, filename, file_bytes) VALUES (?, ?, ?)",
            (user_id, filename, data),
        )
        conn.commit()

def list_documents(user_id: int) -> list[tuple[int, str]]:
    with get_connection_docs() as conn:
        cur = conn.execute(
            "SELECT id, filename FROM documents WHERE user_id=? ORDER BY id",
            (user_id,),
        )
        return cur.fetchall()

# ==== PERSONAL INFO ====

def init_db_personal():
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS personal_info(
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            photo BLOB,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()

def save_personal_info(user_id: int, name: str, email: str, phone: str, photo_bytes: bytes | None):
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO personal_info (user_id, name, email, phone, photo) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, email, phone, photo_bytes),
    )
    conn.commit()
    conn.close()

def load_personal_info(user_id: int):
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "SELECT name, email, phone, photo FROM personal_info WHERE user_id=?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row

# ==== USERS ====

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, password: str) -> int:
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, _hash_password(password)),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Пользователь уже существует")
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> int | None:
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password FROM users WHERE username=?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    if row and row[1] == _hash_password(password):
        return row[0]
    return None

# ==== ИНИЦИАЛИЗАЦИЯ ====
init_db_docs()
init_db_personal()

