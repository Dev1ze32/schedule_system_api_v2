from app.database.connection import create_connection
from mysql.connector import Error

def get_faculty_login_by_identifier(identifier):
    """
    Used for logging in. Identifier can be username or email.
    """
    conn = create_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT l.* FROM faculty_login l
            JOIN faculty f ON l.faculty_id = f.faculty_id
            WHERE (l.username = %s OR f.email = %s)
            LIMIT 1
        """
        cursor.execute(query, (identifier, identifier))
        return cursor.fetchone()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def insert_faculty_login(faculty_id, username, password_hash, password_salt):
    conn = create_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faculty_login (faculty_id, username, password_hash, password_salt, is_active, created_at) VALUES (%s, %s, %s, %s, True, NOW())", 
            (faculty_id, username, password_hash, password_salt)
        )
        conn.commit()
        return cursor.lastrowid
    except Error: return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def update_faculty_password_record(faculty_id, new_hash, new_salt):
    """Used for Admin Reset or User Change Password"""
    conn = create_connection()
    if not conn: return False, "DB Error"
    try:
        cursor = conn.cursor()
        # Updates password and resets lockout counters
        cursor.execute(
            "UPDATE faculty_login SET password_hash=%s, password_salt=%s, failed_attempts=0, locked_until=NULL, updated_at=NOW() WHERE faculty_id=%s", 
            (new_hash, new_salt, faculty_id)
        )
        conn.commit()
        return True, "Success"
    except Error as e:
        return False, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def username_exists(username):
    conn = create_connection()
    if not conn: return True
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM faculty_login WHERE username = %s", (username.strip(),))
        return cursor.fetchone() is not None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()