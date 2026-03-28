from db import get_db

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detection_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        inference_ms INTEGER,
        timestamp TEXT,
        confidence REAL,
        detected BOOLEAN,
        source TEXT,
        image_path TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()