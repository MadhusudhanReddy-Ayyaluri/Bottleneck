from datetime import datetime
from src.db import get_connection

def request_approval(task_id, employee, approver, reason):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO approval_requests
    (task_id, requested_by, requested_to, reason_for_wait,
     request_time, approval_status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        task_id,
        employee,
        approver,
        reason,
        datetime.now().isoformat(),
        "PENDING"
    ))

    cur.execute("""
    UPDATE task_status
    SET current_status='WAITING_FOR_APPROVAL', status_since=?
    WHERE task_id=?
    """, (datetime.now().isoformat(), task_id))

    conn.commit()
    conn.close()

def approve_task(approval_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE approval_requests
    SET approval_status='APPROVED', approval_time=?
    WHERE approval_id=?
    """, (datetime.now().isoformat(), approval_id))

    conn.commit()
    conn.close()
