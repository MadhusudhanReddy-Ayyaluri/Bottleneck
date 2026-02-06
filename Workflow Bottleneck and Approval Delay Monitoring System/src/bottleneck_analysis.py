import pandas as pd
from src.db import get_connection

def get_pending_approvals():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT * FROM approval_requests
        WHERE approval_status='PENDING'
    """, conn)
    conn.close()
    return df
