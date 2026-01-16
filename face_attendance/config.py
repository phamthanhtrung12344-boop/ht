import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "db.sqlite")

FACE_SIMILARITY_THRESHOLD = 0.6

CAMERA_INDEX = 0

SECRET_KEY = "attendance-secret-key"
