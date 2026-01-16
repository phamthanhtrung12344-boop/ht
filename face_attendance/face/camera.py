import cv2
import datetime
import sqlite3
import numpy as np
from face.face_recognition import get_embedding

conn = sqlite3.connect("database/db.sqlite", check_same_thread=False)
cursor = conn.cursor()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def start_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        emb = get_embedding(frame)

        if emb is not None:
            cursor.execute("SELECT id, face_embedding FROM students")
            for sid, stored in cursor.fetchall():
                stored_emb = np.frombuffer(stored, dtype=np.float32)
                sim = cosine_similarity(emb, stored_emb)

                if sim > 0.6:
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    img_path = f"static/captures/{sid}_{time_now}.jpg"
                    cv2.imwrite(img_path, frame)

                    cursor.execute("""
                        INSERT INTO attendance(student_id, time, status, image_path)
                        VALUES (?, ?, ?, ?)
                    """, (sid, time_now, "Có mặt", img_path))
                    conn.commit()
                    break

        cv2.imshow("Attendance Camera", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
