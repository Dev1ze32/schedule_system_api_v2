from app.database.connection import create_connection
from mysql.connector import Error


def _clear_cursor_results(cursor):
    """Safety net - use consistently across all models"""
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


def get_semester_by_id(semester_id):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True, buffered=True)
        _clear_cursor_results(cursor)   # Extra safety

        cursor.execute("SELECT * FROM semester WHERE semester_id = %s", (semester_id,))
        result = cursor.fetchone()
        return result

    except Error as e:
        print(f"Error fetching semester: {e}")
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


def get_active_semester():
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM semester WHERE is_active = 1 LIMIT 1")
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


def get_all_semesters():
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM semester ORDER BY created_at DESC")
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


def create_semester_record(name, code, year, start, end):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return None, "Database connection failed"

        cursor = conn.cursor()   # No need for dictionary here
        query = """
            INSERT INTO semester
            (semester_name, semester_code, academic_year, start_date, end_date, is_active, is_locked)
            VALUES (%s, %s, %s, %s, %s, 0, 0)
        """
        cursor.execute(query, (name, code, year, start, end))
        conn.commit()
        return cursor.lastrowid, None

    except Error as e:
        if e.errno == 1062:
            return None, f"Semester code '{code}' already exists."
        print(f"Database Error: {e}")
        return None, str(e)
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


def update_semester_record(semester_id, name, code, year, start, end):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return False, "DB Connection Error"

        cursor = conn.cursor()
        query = """
            UPDATE semester SET
            semester_name=%s, semester_code=%s, academic_year=%s, 
            start_date=%s, end_date=%s
            WHERE semester_id=%s
        """
        cursor.execute(query, (name, code, year, start, end, semester_id))
        conn.commit()
        return True, "Semester updated successfully"

    except Error as e:
        if e.errno == 1062:
            return False, f"Semester code '{code}' already exists."
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


def delete_semester_data(semester_id):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return False, "DB Connection Error"

        cursor = conn.cursor()
        # Delete related declarations first
        cursor.execute("DELETE FROM work_declaration WHERE semester_id = %s", (semester_id,))
        cursor.execute("DELETE FROM semester WHERE semester_id = %s", (semester_id,))
        conn.commit()
        return True, "Semester deleted"

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


def semester_exists(semester_id):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if not conn:
            return False

        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT 1 FROM semester WHERE semester_id = %s", (semester_id,))
        result = cursor.fetchone()
        return result is not None

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
