# app/models/faculty.py

# CHANGE THIS LINE:
# from app.database.connection import get_db_connection 
# TO THIS:
from app.database.connection import create_connection as get_db_connection

from datetime import datetime
from mysql.connector import Error

def faculty_exists(faculty_id):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor(buffered=True) # ? FIX: Add buffered=True
        cursor.execute("SELECT 1 FROM faculty WHERE faculty_id = %s", (faculty_id,))
        result = cursor.fetchone()
        cursor.fetchall() # ? FIX: Clear the buffer
        return result is not None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def insert_faculty(name, email, department):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faculty (faculty_name, email, department, created_at) VALUES (%s, %s, %s, %s)", 
                       (name, email, department, datetime.now()))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"DB Insert Error: {e}")
        return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_all_faculty_details():
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT f.faculty_id, f.faculty_name, f.email, f.department, l.username, l.is_active, l.last_login FROM faculty f LEFT JOIN faculty_login l ON f.faculty_id = l.faculty_id ORDER BY f.faculty_name ASC")
        return cursor.fetchall()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def delete_faculty_data(faculty_id):
    """
    Safely deletes a faculty account and ALL their associated data.
    Order: Schedules -> Login -> Profile
    """
    conn = get_db_connection()
    if not conn: return False, "DB Connection Failed"
    
    try:
        cursor = conn.cursor()
        
        # 1. Delete all schedule declarations for this faculty
        cursor.execute("DELETE FROM work_declaration WHERE faculty_id = %s", (faculty_id,))
        
        # 2. Delete their login credentials
        cursor.execute("DELETE FROM faculty_login WHERE faculty_id = %s", (faculty_id,))
        
        # 3. Delete the faculty profile itself
        cursor.execute("DELETE FROM faculty WHERE faculty_id = %s", (faculty_id,))
        
        conn.commit()
        
        return True, "Faculty account and data deleted successfully."
            
    except Error as e:
        if conn: conn.rollback()
        print(f"Delete Error: {e}")
        return False, f"Database Error: {str(e)}"
    finally:
        if conn.is_connected(): 
            cursor.close()
            conn.close()