import sqlite3
from typing import Optional, Dict

DB_PATH = "user_data.db"


def init_db() -> None:
    """Initialize the SQLite database and personal_info table."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS personal_info("
        "name TEXT, email TEXT, phone TEXT, photo BLOB)"
    )
    conn.commit()
    conn.close()


def save_personal_info(name: str, email: str, phone: str, photo_bytes: Optional[bytes]) -> None:
    """Save personal information to the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM personal_info")
    cur.execute(
        "INSERT INTO personal_info(name, email, phone, photo) VALUES(?,?,?,?)",
        (name, email, phone, photo_bytes),
    )
    conn.commit()
    conn.close()


def load_personal_info() -> Optional[Dict[str, Optional[str]]]:
    """Load personal information from the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT name, email, phone, photo FROM personal_info LIMIT 1"
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "photo": row[3],
        }
    return None

