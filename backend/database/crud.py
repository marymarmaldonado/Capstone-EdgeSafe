from database.db import get_db
from datetime import datetime

def insert_detection_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO detection_events (model_name, inference_ms, timestamp, confidence, detected, source, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (model_name, inference_ms, timestamp, confidence, detected, source, image_path))

    conn.commit()
    conn.close()


def get_all_events():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detection_events")
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_event_by_id(event_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detection_events WHERE id = ?", (event_id,))
    row = cursor.fetchone()

    conn.close()

    return row

def get_filtered_events(detected = None, source = None, limit = None):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM detection_events WHERE 1=1"
    params = []

    if detected is not None:
        query += " AND detected = ?"
        params.append(int(detected))
    
    if source is not None:
        query += " AND source = ?"
        params.append(source)

    query += " ORDER BY id DESC"

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return rows

# User functions
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user

def create_user(username, password_hash):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password_hash, created_at)
        VALUES (?, ?, ?)
    """, (username, password_hash, datetime.now().isoformat()))

    conn.commit()
    conn.close()