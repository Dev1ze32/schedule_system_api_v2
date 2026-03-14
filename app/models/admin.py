from app.database.connection import create_connection as get_db_connection
from mysql.connector import Error
from datetime import datetime

# --- ADMIN RETRIEVAL ---

def get_admin_by_username(username):
    """Fetches admin login details for authentication."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        # Note: We check if is_active exists. If your DB doesn't have it, remove 'AND l.is_active = 1'
        query = """
            SELECT a.admin_id, a.admin_name, a.email, l.password_hash 
            FROM admins a 
            JOIN admin_login l ON a.admin_id = l.admin_id 
            WHERE l.username = %s AND l.is_active = 1
        """
        cursor.execute(query, (username,))
        return cursor.fetchone()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_all_admins():
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.admin_id, a.admin_name, a.email, l.username, l.is_active, l.last_login 
            FROM admins a 
            JOIN admin_login l ON a.admin_id = l.admin_id 
            ORDER BY a.admin_name ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# --- ADMIN CREATION & MANAGEMENT ---

def insert_admin_profile(name, email):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        # Assuming 'admins' table HAS created_at. If this fails too, remove ', created_at' and ', NOW()'
        cursor.execute("INSERT INTO admins (admin_name, email, created_at) VALUES (%s, %s, NOW())", (name, email))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"DB Error (Insert Profile): {e}") 
        return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def insert_admin_login(admin_id, username, password_hash):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        
        # --- FIX: Removed 'created_at' from this query ---
        query = """
            INSERT INTO admin_login (admin_id, username, password_hash, is_active) 
            VALUES (%s, %s, %s, 1)
        """
        cursor.execute(query, (admin_id, username, password_hash))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"DB Error (Insert Login): {e}") # This will print new errors if any
        return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def update_admin_password_record(admin_id, new_hash):
    conn = get_db_connection()
    if not conn: return False, "DB Connection Error"
    try:
        cursor = conn.cursor()
        
        # --- FIX: Removed 'updated_at' just in case that is missing too ---
        query = "UPDATE admin_login SET password_hash=%s WHERE admin_id=%s"
        
        cursor.execute(query, (new_hash, admin_id))
        conn.commit()
        return True, "Password reset successfully"
    except Error as e:
        return False, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def delete_admin_data(admin_id):
    conn = get_db_connection()
    if not conn: return False, "DB Connection Failed"
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin_login WHERE admin_id = %s", (admin_id,))
        cursor.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
        conn.commit()
        return True, "Admin account removed successfully"
    except Error as e:
        if conn: conn.rollback()
        return False, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()