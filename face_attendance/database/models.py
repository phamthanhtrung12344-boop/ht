import sqlite3

conn = sqlite3.connect("database/db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class_name TEXT,
    face_embedding BLOB
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    time TEXT,
    status TEXT,
    image_path TEXT
)
""")

conn.commit()
