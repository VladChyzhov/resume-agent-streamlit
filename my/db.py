from __future__ import annotations
import sqlite3
from pathlib import Path
import os
import hashlib

# Database paths
DB_PATH_DOCS = Path(__file__).parent / "resume.db"
DB_PATH_PERSONAL = Path(__file__).parent / "user_data.db"


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
            "  category TEXT DEFAULT 'general',\n"
            "  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
            ")"
        )
        conn.commit()

def save_document(file_obj, user_id: int, category: str = "general") -> bool:
    """Save a document with category classification"""
    if not file_obj:
        return False
    
    try:
        data = file_obj.getvalue()
        filename = file_obj.name
        with get_connection_docs() as conn:
            conn.execute(
                "INSERT INTO documents(user_id, filename, file_bytes, category) VALUES (?, ?, ?, ?)",
                (user_id, filename, data, category),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error saving document: {e}")
        return False

def list_documents(user_id: int, category: str | None = None) -> list[tuple[int, str, str]]:
    """List documents, optionally filtered by category"""
    try:
        with get_connection_docs() as conn:
            if category:
                cur = conn.execute(
                    "SELECT id, filename, category FROM documents WHERE user_id=? AND category=? ORDER BY id",
                    (user_id, category),
                )
            else:
                cur = conn.execute(
                    "SELECT id, filename, category FROM documents WHERE user_id=? ORDER BY id",
                    (user_id,),
                )
            return cur.fetchall()
    except Exception as e:
        print(f"Error listing documents: {e}")
        return []

# ==== PERSONAL INFO ====

def get_connection_personal() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH_PERSONAL)

def init_db_personal():
    try:
        with get_connection_personal() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS personal_info(
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    photo BLOB,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )
            conn.commit()
    except Exception as e:
        print(f"Error initializing personal database: {e}")

def save_personal_info(user_id: int, name: str, email: str, phone: str, photo_bytes: bytes | None) -> bool:
    """Save personal information with proper error handling"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO personal_info (user_id, name, email, phone, photo, updated_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (user_id, name, email, phone, photo_bytes),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error saving personal info: {e}")
        return False

def load_personal_info(user_id: int) -> tuple | None:
    """Load personal information with error handling"""
    try:
        with get_connection_personal() as conn:
            cur = conn.execute(
                "SELECT name, email, phone, photo FROM personal_info WHERE user_id=?",
                (user_id,),
            )
            return cur.fetchone()
    except Exception as e:
        print(f"Error loading personal info: {e}")
        return None

# ==== USERS ====

def _hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> int:
    """Register a new user with validation"""
    if not username or not password:
        raise ValueError("Имя пользователя и пароль не могут быть пустыми")
    
    if len(password) < 4:
        raise ValueError("Пароль должен содержать минимум 4 символа")
    
    try:
        with get_connection_personal() as conn:
            cur = conn.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (username.strip(), _hash_password(password)),
            )
            conn.commit()
            user_id = cur.lastrowid
            if user_id is None:
                raise ValueError("Ошибка создания пользователя")
            return user_id
    except sqlite3.IntegrityError:
        raise ValueError("Пользователь с таким именем уже существует")
    except Exception as e:
        raise ValueError(f"Ошибка регистрации: {str(e)}")

def authenticate_user(username: str, password: str) -> int | None:
    """Authenticate user credentials"""
    if not username or not password:
        return None
    
    try:
        with get_connection_personal() as conn:
            cur = conn.execute(
                "SELECT id, password FROM users WHERE username=?",
                (username.strip(),),
            )
            row = cur.fetchone()
            if row and row[1] == _hash_password(password):
                return row[0]
    except Exception as e:
        print(f"Error authenticating user: {e}")
    
    return None

# ==== SKILLS AND LANGUAGES ====

def init_db_skills():
    """Initialize skills and languages database"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS skills(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill_name TEXT NOT NULL,
                    skill_level TEXT DEFAULT 'intermediate',
                    category TEXT DEFAULT 'technical',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS languages(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    language_name TEXT NOT NULL,
                    proficiency_level TEXT DEFAULT 'intermediate',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )
            conn.commit()
    except Exception as e:
        print(f"Error initializing skills database: {e}")

def save_skill(user_id: int, skill_name: str, skill_level: str = "intermediate", category: str = "technical") -> bool:
    """Save a skill"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                "INSERT INTO skills(user_id, skill_name, skill_level, category) VALUES (?, ?, ?, ?)",
                (user_id, skill_name.strip(), skill_level, category),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error saving skill: {e}")
        return False

def save_language(user_id: int, language_name: str, proficiency_level: str = "intermediate") -> bool:
    """Save a language"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                "INSERT INTO languages(user_id, language_name, proficiency_level) VALUES (?, ?, ?)",
                (user_id, language_name.strip(), proficiency_level),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error saving language: {e}")
        return False

def list_skills(user_id: int) -> list[tuple]:
    """List user skills"""
    try:
        with get_connection_personal() as conn:
            cur = conn.execute(
                "SELECT id, skill_name, skill_level, category FROM skills WHERE user_id=? ORDER BY category, skill_name",
                (user_id,),
            )
            return cur.fetchall()
    except Exception as e:
        print(f"Error listing skills: {e}")
        return []

def list_languages(user_id: int) -> list[tuple]:
    """List user languages"""
    try:
        with get_connection_personal() as conn:
            cur = conn.execute(
                "SELECT id, language_name, proficiency_level FROM languages WHERE user_id=? ORDER BY language_name",
                (user_id,),
            )
            return cur.fetchall()
    except Exception as e:
        print(f"Error listing languages: {e}")
        return []

def delete_skill(skill_id: int, user_id: int) -> bool:
    """Delete a skill"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                "DELETE FROM skills WHERE id=? AND user_id=?",
                (skill_id, user_id),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting skill: {e}")
        return False

def delete_language(language_id: int, user_id: int) -> bool:
    """Delete a language"""
    try:
        with get_connection_personal() as conn:
            conn.execute(
                "DELETE FROM languages WHERE id=? AND user_id=?",
                (language_id, user_id),
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting language: {e}")
        return False

# ==== INITIALIZATION ====
try:
    init_db_docs()
    init_db_personal()
    init_db_skills()
    print("Databases initialized successfully")
except Exception as e:
    print(f"Error during database initialization: {e}")

