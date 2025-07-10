from __future__ import annotations
import sqlite3
from pathlib import Path
import os
import hashlib
import secrets

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
            "  file_bytes BLOB,\n"
            "  doc_type TEXT\n"  # Added document type
            ")"
        )
        conn.commit()

def save_document(file_obj, user_id: int, doc_type: str = 'general') -> None:
    if not file_obj:
        return
    data = file_obj.getvalue()
    filename = file_obj.name
    
    # Validate file size (limit to 10MB)
    if len(data) > 10 * 1024 * 1024:
        raise ValueError("File size must be less than 10MB")
    
    with get_connection_docs() as conn:
        conn.execute(
            "INSERT INTO documents(user_id, filename, file_bytes, doc_type) VALUES (?, ?, ?, ?)",
            (user_id, filename, data, doc_type),
        )
        conn.commit()

def list_documents(user_id: int, doc_type: str | None = None) -> list[tuple[int, str]]:
    with get_connection_docs() as conn:
        if doc_type:
            cur = conn.execute(
                "SELECT id, filename FROM documents WHERE user_id=? AND doc_type=? ORDER BY id",
                (user_id, doc_type),
            )
        else:
            cur = conn.execute(
                "SELECT id, filename FROM documents WHERE user_id=? ORDER BY id",
                (user_id,),
            )
        return cur.fetchall()

def delete_document(doc_id: int, user_id: int) -> bool:
    with get_connection_docs() as conn:
        cur = conn.execute(
            "DELETE FROM documents WHERE id=? AND user_id=?",
            (doc_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0

# ==== PERSONAL INFO ====

def init_db_personal():
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            salt TEXT
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS skills_languages(
            user_id INTEGER PRIMARY KEY,
            skills TEXT,
            languages TEXT,
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

# ==== SKILLS & LANGUAGES ====

def save_skills_languages(user_id: int, skills: str, languages: str):
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO skills_languages (user_id, skills, languages) VALUES (?, ?, ?)",
        (user_id, skills, languages),
    )
    conn.commit()
    conn.close()

def load_skills_languages(user_id: int):
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "SELECT skills, languages FROM skills_languages WHERE user_id=?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row

# ==== USERS ====

def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()


def register_user(username: str, password: str) -> int:
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    try:
        salt = secrets.token_hex(16)
        hashed_password = _hash_password(password, salt)
        cur.execute(
            "INSERT INTO users(username, password, salt) VALUES (?, ?, ?)",
            (username, hashed_password, salt),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("User already exists")
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> int | None:
    conn = sqlite3.connect(DB_PATH_PERSONAL)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password, salt FROM users WHERE username=?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        user_id, stored_password, salt = row
        if salt is None:  # Handle legacy users without salt
            # Check with old method
            if stored_password == hashlib.sha256(password.encode()).hexdigest():
                return user_id
        else:
            # Check with new salted method
            if stored_password == _hash_password(password, salt):
                return user_id
    return None

# ==== GET ALL USER DATA ====

def get_user_resume_data(user_id: int):
    """Get all user data for resume generation"""
    personal = load_personal_info(user_id)
    skills_langs = load_skills_languages(user_id)
    education_docs = list_documents(user_id, 'education')
    work_docs = list_documents(user_id, 'work')
    
    return {
        'personal': {
            'name': personal[0] if personal else '',
            'email': personal[1] if personal else '',
            'phone': personal[2] if personal else '',
            'has_photo': personal[3] is not None if personal else False
        },
        'skills': skills_langs[0] if skills_langs else '',
        'languages': skills_langs[1] if skills_langs else '',
        'education_documents': education_docs,
        'work_documents': work_docs
    }

# ==== ИНИЦИАЛИЗАЦИЯ ====
init_db_docs()
init_db_personal()

