from database.db import get_db

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