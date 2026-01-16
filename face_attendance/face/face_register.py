import cv2
import os

STUDENT_ID = 1   # 🔴 đổi ID sinh viên cho phù hợp

SAVE_DIR = f"faces/student_{STUDENT_ID}"
os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Nhấn SPACE để chụp ảnh, ESC để thoát")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

    if key == 32:  # SPACE
        img_path = f"{SAVE_DIR}/{count}.jpg"
        cv2.imwrite(img_path, frame)
        print("Đã lưu:", img_path)
        count += 1

cap.release()
cv2.destroyAllWindows()
