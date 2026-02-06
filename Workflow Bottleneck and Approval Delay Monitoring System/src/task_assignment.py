import sqlite3
from datetime import datetime
from src.db import get_connection

def assign_task(task_id, title, assigned_by, employee_id, deadline, priority):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO task_assignment
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task_id,
        title,
        assigned_by,
        employee_id,
        datetime.now().isoformat(),
        deadline,
        priority
    ))

    cur.execute("""
    INSERT INTO task_status
    VALUES (?, ?, ?)
    """, (
        task_id,
        "ASSIGNED",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
