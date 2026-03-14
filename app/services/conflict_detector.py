from app.database.connection import create_connection
from mysql.connector import Error

def check_schedule_conflicts(semester_id, day, start_time, end_time, room_id, faculty_id, exclude_declaration_id=None):
    conn = create_connection()
    if not conn: return True, "Database Connection Failed"
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Check Room Conflict
        query_room = """
            SELECT faculty_id, time_start, time_end, subject_code 
            FROM work_declaration 
            WHERE semester_id = %s 
            AND room_id = %s 
            AND day_of_week = %s
            AND time_start < %s 
            AND time_end > %s
            AND declaration_status != 'Rejected'
        """
        params_room = [semester_id, room_id, day, end_time, start_time]
        
        if exclude_declaration_id:
            query_room += " AND declaration_id != %s"
            params_room.append(exclude_declaration_id)
            
        cursor.execute(query_room, params_room)
        conflict = cursor.fetchone()
        
        if conflict:
            return True, f"Room Conflict: {conflict['subject_code']} is already scheduled here from {conflict['time_start']} to {conflict['time_end']}."

        # 2. Check Faculty Conflict
        query_faculty = """
            SELECT room_id, time_start, time_end, subject_code
            FROM work_declaration
            WHERE semester_id = %s
            AND faculty_id = %s
            AND day_of_week = %s
            AND time_start < %s
            AND time_end > %s
            AND declaration_status != 'Rejected'
        """
        params_faculty = [semester_id, faculty_id, day, end_time, start_time]
        
        if exclude_declaration_id:
            query_faculty += " AND declaration_id != %s"
            params_faculty.append(exclude_declaration_id)
            
        cursor.execute(query_faculty, params_faculty)
        conflict = cursor.fetchone()
        
        if conflict:
            return True, f"Schedule Conflict: You already have {conflict['subject_code']} scheduled from {conflict['time_start']} to {conflict['time_end']}."

        return False, None

    except Error as e:
        return True, f"Validation Error: {str(e)}"
    finally:
        if conn.is_connected(): cursor.close(); conn.close()