import pandas as pd
import sqlite3

conn = sqlite3.connect("database/db.sqlite")

df = pd.read_sql("""
SELECT students.name, students.class_name,
       attendance.time, attendance.status
FROM attendance
JOIN students ON attendance.student_id = students.id
""", conn)

df.to_excel("bao_cao_chuyen_can.xlsx", index=False)
print("Đã xuất báo cáo")
