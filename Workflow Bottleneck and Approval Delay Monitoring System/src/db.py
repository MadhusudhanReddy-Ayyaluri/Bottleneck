import sqlite3
import os

DB_PATH = "database/workflow.db"

def get_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_assignment (
        task_id INTEGER PRIMARY KEY,
        task_title TEXT,
        assigned_by TEXT,
        employee_id TEXT,
        assigned_time TEXT,
        deadline TEXT,
        priority TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_status (
        task_id INTEGER,
        current_status TEXT,
        status_since TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS approval_requests (
        approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        requested_by TEXT,
        requested_to TEXT,
        reason_for_wait TEXT,
        request_time TEXT,
        approval_time TEXT,
        approval_status TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
