from app.database.connection import create_connection
from mysql.connector import Error
from datetime import datetime

def insert_audit_log(action_type, related_id, details):
    conn = create_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (action_type, related_id, details, search_timestamp)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (action_type, related_id, details, datetime.now()))
        conn.commit()
        return True
    except Error as e:
        print(f"Log Error: {e}")
        return False
    finally:
        if conn.is_connected(): cursor.close(); conn.close()