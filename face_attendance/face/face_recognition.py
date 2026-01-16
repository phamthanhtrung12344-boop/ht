import cv2
import os
import sqlite3
import numpy as np
from datetime import datetime

DB_PATH = "database/db.sqlite"
FACE_DIR = "static/faces"

recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
labels = []

label_map = {}
label_id = 0

# ===== LOAD DATASET =====
for folder in os.listdir(FACE_DIR):
    if not folder.startswith("student_"):
        continue

    student_id = int(folder.split("_")[1])
    label_map[label_id] = student_id

    folder_path = os.path.join(FACE_DIR, folder)
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(label_id)

    label_id += 1

faces = np.array(faces)
labels = np.array(labels)

recognizer.train(faces, labels)

# ===== CAMERA =====
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

marked_today = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces_detected:
        roi = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(roi)

        if confidence < 80:
            student_id = label_map[label]

            now = datetime.now()
            hour = now.hour

            if hour < 12:
                status = "den truong"
            else:
                status = "Tan hoc"

            key = (student_id, status)

            if key not in marked_today:
                cur.execute("""
                    INSERT INTO attendance (student_id, time, status)
                    VALUES (?, ?, ?)
                """, (
                    student_id,
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                    status
                ))
                conn.commit()
                marked_today.add(key)

            cv2.putText(
                frame,
                f"ID {student_id} - {status}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
conn.close()
cv2.destroyAllWindows()
