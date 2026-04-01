from app.database.connection import create_connection
from mysql.connector import Error
from datetime import datetime

def get_semester_by_id(semester_id):
    conn = create_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM semester WHERE semester_id = %s", (semester_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching semester: {e}")
        return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_active_semester():
    conn = create_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM semester WHERE is_active = 1 LIMIT 1")
        return cursor.fetchone()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_all_semesters():
    conn = create_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM semester ORDER BY created_at DESC")
        return cursor.fetchall()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def create_semester_record(name, code, year, start, end):
    conn = create_connection()
    if not conn: return None, "Database connection failed"
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO semester 
            (semester_name, semester_code, academic_year, start_date, end_date, is_active, is_locked) 
            VALUES (%s, %s, %s, %s, %s, 0, 0)
        """
        cursor.execute(query, (name, code, year, start, end))
        conn.commit()
        return cursor.lastrowid, None # Success: (ID, No Error)

    except Error as e:
        # Check for Duplicate Entry Error (MySQL Error 1062)
        if e.errno == 1062:
            return None, f"Semester code '{code}' already exists."
        
        print(f"Database Error: {e}")
        return None, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def update_semester_record(semester_id, name, code, year, start, end):
    conn = create_connection()
    if not conn: return False, "DB Connection Error"
    try:
        cursor = conn.cursor()
        query = """
            UPDATE semester SET 
            semester_name=%s, semester_code=%s, academic_year=%s, start_date=%s, end_date=%s 
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
        if conn.is_connected(): cursor.close(); conn.close()

def delete_semester_data(semester_id):
    conn = create_connection()
    if not conn: return False, "DB Connection Error"
    try:
        cursor = conn.cursor()
        # Delete related declarations first (or rely on DB constraints, but safer to be explicit)
        cursor.execute("DELETE FROM work_declaration WHERE semester_id = %s", (semester_id,))
        cursor.execute("DELETE FROM semester WHERE semester_id = %s", (semester_id,))
        conn.commit()
        return True, "Semester deleted"
    except Error as e:
        return False, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def semester_exists(semester_id):
    conn = create_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM semester WHERE semester_id = %s", (semester_id,))
        return cursor.fetchone() is not None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()