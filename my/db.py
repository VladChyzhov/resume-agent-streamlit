import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'user_data.db')

def init_db():
    """Initialize the SQLite database and personal_info table."""
    conn = sqlite3.connect(DB_PATH)
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
    """Save personal information, replacing previous entry."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM personal_info")
    cur.execute(
        "INSERT INTO personal_info (name, email, phone, photo) VALUES (?, ?, ?, ?)",
        (name, email, phone, photo_bytes),
    )
    conn.commit()
    conn.close()


def load_personal_info():
    """Load saved personal information. Returns tuple or None."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT name, email, phone, photo FROM personal_info LIMIT 1"
    )
    row = cur.fetchone()
    conn.close()
    return row


# Initialize DB on module import
init_db()
