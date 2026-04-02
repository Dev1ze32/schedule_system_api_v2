from app.database.connection import create_connection as get_db_connection
from mysql.connector import Error


def _clear_cursor_results(cursor):
    if not cursor:
        return
    try:
        if cursor.with_rows:
            cursor.fetchall()
    except Exception:
        pass
    try:
        while cursor.nextset():
            try:
                if cursor.with_rows:
                    cursor.fetchall()
            except Exception:
                pass
    except Exception:
        pass


def get_admin_by_username(username):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True, buffered=True)
        _clear_cursor_results(cursor)

        query = """
            SELECT a.admin_id, a.admin_name, a.email, l.password_hash
            FROM admins a
            JOIN admin_login l ON a.admin_id = l.admin_id
            WHERE l.username = %s AND l.is_active = 1
        """
        cursor.execute(query, (username,))
        return cursor.fetchone()

    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


def get_all_admins():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True, buffered=True)
        query = """
            SELECT a.admin_id, a.admin_name, a.email, l.username, l.is_active, l.last_login
            FROM admins a
            JOIN admin_login l ON a.admin_id = l.admin_id
            ORDER BY a.admin_name ASC
        """
        cursor.execute(query)
        return cursor.fetchall()

    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


def insert_admin_profile(name, email):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO admins (admin_name, email, created_at) VALUES (%s, %s, NOW())",
            (name, email)
        )
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"DB Error (Insert Profile): {e}")
        return None
    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


def insert_admin_login(admin_id, username, password_hash):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = """
            INSERT INTO admin_login (admin_id, username, password_hash, is_active)
            VALUES (%s, %s, %s, 1)
        """
        cursor.execute(query, (admin_id, username, password_hash))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"DB Error (Insert Login): {e}")
        return None
    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


def update_admin_password_record(admin_id, new_hash):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return False, "DB Connection Error"

        cursor = conn.cursor()
        query = "UPDATE admin_login SET password_hash=%s WHERE admin_id=%s"
        cursor.execute(query, (new_hash, admin_id))
        conn.commit()
        return True, "Password reset successfully"

    except Error as e:
        return False, str(e)
    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass


def delete_admin_data(admin_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return False, "DB Connection Failed"

        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin_login WHERE admin_id = %s", (admin_id,))
        cursor.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
        conn.commit()
        return True, "Admin account removed successfully"

    except Error as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if cursor:
            try:
                _clear_cursor_results(cursor)
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass