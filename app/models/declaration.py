from app.database.connection import create_connection as get_db_connection
from mysql.connector import Error
from datetime import datetime

# --- DECLARATION WRITES ---

def insert_declaration_record(faculty_id, room_id, semester_id, subject_code, class_section, day, start, end, status='Pending'):
    conn = get_db_connection()
    if not conn: return None, "DB Connection Error"
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Check if semester is locked before inserting (Double check layer)
        cursor.execute("SELECT is_locked FROM semester WHERE semester_id = %s", (semester_id,))
        sem = cursor.fetchone()
        if sem and sem['is_locked']: 
            return None, "Semester is locked"
            
        query = """
        INSERT INTO work_declaration 
        (faculty_id, room_id, semester_id, subject_code, class_section, day_of_week, 
         time_start, time_end, declaration_status, uploaded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        args = (faculty_id, room_id, semester_id, subject_code, class_section, day, start, end, status, datetime.now())
        
        cursor.execute(query, args)
        conn.commit()
        return cursor.lastrowid, None
    except Error as e:
        print(f"Insert Declaration Error: {e}")
        return None, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def update_declaration_record(declaration_id, updates, params):
    conn = get_db_connection()
    if not conn: return False, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Always update the modified timestamp
        updates.append("last_modified_at = %s")
        params.append(datetime.now())
        
        # Add the WHERE clause parameter at the very end
        params.append(declaration_id)
        
        set_clause = ", ".join(updates)
        query = f"UPDATE work_declaration SET {set_clause} WHERE declaration_id = %s"
        
        cursor.execute(query, params)
        conn.commit()
        return True, "Updated successfully"
        
    except Error as e:
        if conn: conn.rollback()
        return False, str(e)
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def delete_declaration_record(declaration_id):
    conn = get_db_connection()
    if not conn: return False, "DB Error"
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM work_declaration WHERE declaration_id=%s", (declaration_id,))
        conn.commit()
        return True, "Deleted"
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# --- DECLARATION READS ---

def get_declaration_by_id(declaration_id):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM work_declaration WHERE declaration_id = %s", (declaration_id,))
        return cursor.fetchone()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_faculty_schedule_data(faculty_id, semester_id=None):
    """
    Fetches all declarations for a specific faculty member.
    """
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        query = """
            SELECT w.declaration_id, f.faculty_name, r.building_name, r.room_name,
                   w.day_of_week, w.time_start, w.time_end, w.subject_code, w.class_section,
                   w.declaration_status, s.semester_name, s.is_locked, s.is_active
            FROM work_declaration w
            JOIN faculty f ON w.faculty_id = f.faculty_id
            JOIN room r ON w.room_id = r.room_id
            JOIN semester s ON w.semester_id = s.semester_id
            WHERE w.faculty_id = %s
        """
        params = [faculty_id]
        if semester_id:
            query += " AND w.semester_id = %s"
            params.append(semester_id)
        query += " ORDER BY s.semester_id DESC, w.day_of_week, w.time_start"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        for row in results:
            if row['time_start']:
                row['time_start'] = str(row['time_start']) # Converts "7:30:00" (timedelta) to string
            if row['time_end']:
                row['time_end'] = str(row['time_end'])

        return results
    except Error as e:
        print(f"Error fetching schedule: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()