import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(__file__), "edgesafe.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn