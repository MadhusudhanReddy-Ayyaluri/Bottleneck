from datetime import datetime
from src.db import get_connection

def update_status(task_id, status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE task_status
    SET current_status=?, status_since=?
    WHERE task_id=?
    """, (status, datetime.now().isoformat(), task_id))

    conn.commit()
    conn.close()
