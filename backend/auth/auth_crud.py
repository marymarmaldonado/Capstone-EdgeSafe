from datetime import datetime
from database.db import get_db


def get_user_by_username(username: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row


def create_user(username: str, password_hash: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()