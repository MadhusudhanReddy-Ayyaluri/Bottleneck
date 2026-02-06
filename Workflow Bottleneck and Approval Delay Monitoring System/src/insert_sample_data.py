import sqlite3
from datetime import datetime
import os

DB_PATH = "database/workflow.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ---------------- TASK ASSIGNMENT ----------------
cur.executemany("""
INSERT INTO task_assignment VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    (1, "Build Login Module", "ADMIN01", "E01", "2025-02-01 09:00", "2025-02-05 18:00", "High"),
    (2, "API Integration", "ADMIN01", "E02", "2025-02-01 10:00", "2025-02-06 18:00", "Medium"),
    (3, "UI Design", "ADMIN02", "E03", "2025-02-01 11:00", "2025-02-07 18:00", "Low"),
    (4, "Database Setup", "ADMIN02", "E04", "2025-02-01 12:00", "2025-02-04 18:00", "High"),
    (5, "Testing Module", "ADMIN01", "E05", "2025-02-01 13:00", "2025-02-06 18:00", "Medium"),
])

# ---------------- TASK STATUS ----------------
cur.executemany("""
INSERT INTO task_status VALUES (?, ?, ?)
""", [
    (1, "IN_PROGRESS", "2025-02-02 10:00"),
    (2, "WAITING_FOR_APPROVAL", "2025-02-02 11:00"),
    (3, "IN_PROGRESS", "2025-02-02 12:00"),
    (4, "WAITING_FOR_APPROVAL", "2025-02-02 13:00"),
    (5, "ASSIGNED", "2025-02-02 14:00"),
])

# ---------------- APPROVAL REQUESTS ----------------
cur.executemany("""
INSERT INTO approval_requests
(task_id, requested_by, requested_to, reason_for_wait, request_time, approval_status)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    (2, "E02", "ADMIN01", "Software license pending", "2025-02-02 11:05", "PENDING"),
    (4, "E04", "ADMIN02", "Tool access pending", "2025-02-02 13:10", "PENDING"),
    (1, "E01", "ADMIN01", "Data access pending", "2025-02-02 10:30", "APPROVED"),
    (3, "E03", "ADMIN02", "Client approval pending", "2025-02-02 12:30", "APPROVED"),
    (5, "E05", "ADMIN01", "Software license pending", "2025-02-02 14:15", "PENDING"),
])

conn.commit()
conn.close()

print("✅ Sample data inserted successfully.")
