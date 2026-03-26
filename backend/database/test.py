from datetime import datetime
from backend.database.db import get_db


def test_write():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO detection_events (model_name, inference_ms, timestamp, confidence, detected, source, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, ("YOLO", 345, datetime.now().isoformat(), 0.85, True, "CAM 2", "images/test.jpg"))

    conn.commit()
    conn.close()


def test_read():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detection_events")
    rows = cursor.fetchall()

    for row in rows:
        print(row["confidence"])

    conn.close()


if __name__ == "__main__":
    test_read()