import sqlite3
from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
from openpyxl import Workbook

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite")

# ================= DASHBOARD =================
@app.route("/")
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Tổng học sinh
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    # Đến trường hôm nay
    cur.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE status='Đến trường'
        AND date(time) = date('now')
    """)
    arrived_today = cur.fetchone()[0]

    # Tan học hôm nay
    cur.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE status='Tan học'
        AND date(time) = date('now')
    """)
    left_today = cur.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        arrived_today=arrived_today,
        left_today=left_today
    )

# ================= STUDENTS =================
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        class_name = request.form["class_name"]
        cur.execute(
            "INSERT INTO students (name, class_name) VALUES (?, ?)",
            (name, class_name)
        )
        conn.commit()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()

    return render_template("students.html", students=students)

# ================= ATTENDANCE =================
@app.route("/attendance")
def attendance():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # ⭐ QUAN TRỌNG
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            attendance.id,
            students.name AS student_name,
            attendance.time,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.time DESC
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("attendance.html", data=data)

@app.route("/attendance/export")
def export_attendance():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT students.id,
               students.name,
               students.class_name,
               attendance.time,
               attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.time DESC
    """)
    rows = cur.fetchall()
    conn.close()

    # Tạo file Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    ws.append(["ID", "Tên học sinh", "Lớp", "Thời gian", "Trạng thái"])

    # Data
    for r in rows:
        ws.append(r)

    # Lưu file
    filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(BASE_DIR, filename)
    wb.save(file_path)

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename
    )


# ================= MAIN =================
if __name__ == "__main__":
    app.run(debug=True)
