from app.models.declaration import insert_declaration_record
from app.models.semester import get_semester_by_id
from app.models.room import room_exists
from app.models.faculty import faculty_exists
from app.services.conflict_detector import check_schedule_conflicts
from app.utils.validators import validate_time_range, VALID_DAYS
from app.models.declaration import (
    update_declaration_record, delete_declaration_record,
    get_declaration_by_id
)
from datetime import datetime

def _clear_cursor_results(cursor):
    """Stronger cleanup - use this everywhere now"""
    if not cursor:
        return
    try:
        # Consume current result set if any
        if cursor.with_rows:
            cursor.fetchall()
    except Exception:
        pass
    try:
        # Clear any multi-result sets
        while cursor.nextset():
            try:
                if cursor.with_rows:
                    cursor.fetchall()
            except Exception:
                pass
    except Exception:
        pass


def insert_declaration_service(faculty_id, room_id, semester_id, subject_code, class_section, day, start, end, na_room_id=None, status='Pending'):
    from app.database.connection import create_connection
    from app.utils.validators import validate_time_range, VALID_DAYS

    conn = None
    cursor = None
    try:
        if day not in VALID_DAYS:
            return None, "Invalid day"

        valid_time, time_error = validate_time_range(start, end)
        if not valid_time:
            return None, time_error

        conn = create_connection()
        if conn:
            conn.cmd_reset_connection()
        if not conn:
            return None, "Database Connection Failed"

        cursor = conn.cursor(dictionary=True, buffered=True)
        _clear_cursor_results(cursor)

        # Faculty & Room checks
        cursor.execute("SELECT 1 FROM faculty WHERE faculty_id = %s LIMIT 1", (faculty_id,))
        if not cursor.fetchall():
            return None, "Faculty not found"

        cursor.execute("SELECT 1 FROM room WHERE room_id = %s LIMIT 1", (room_id,))
        if not cursor.fetchall():
            return None, "Room not found"

        # Semester lock
        cursor.execute("SELECT is_locked FROM semester WHERE semester_id = %s LIMIT 1", (semester_id,))
        semester = cursor.fetchall()
        if not semester:
            return None, "Semester not found"
        if semester[0].get('is_locked'):
            return None, "Semester is locked."

        # === CONFLICT CHECK (this is the N/A hotspot) ===
        has_conflict, error_msg = check_schedule_conflicts(
            semester_id, day, start, end, room_id, faculty_id
        )

        if has_conflict:
            return None, error_msg

        # === INSERT ===
        insert_query = """
            INSERT INTO work_declaration
            (faculty_id, room_id, semester_id, subject_code, class_section, day_of_week,
             time_start, time_end, declaration_status, uploaded_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (faculty_id, room_id, semester_id, subject_code, class_section, day, start, end, status))
        conn.commit()

        return cursor.lastrowid, None

    except Exception as e:
        if conn and conn.is_connected():
            conn.rollback()
        return None, f"DB Error: {str(e)}"

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
def update_declaration_service(declaration_id, faculty_id, room_id=None, subject_code=None, class_section=None, day=None, start=None, end=None):
    """
    Handles updating a schedule declaration with conflict checks.
    """
    # 1. Fetch current data to ensure ownership and existence
    current = get_declaration_by_id(declaration_id)
    if not current:
        return False, "Declaration not found"
    
    if current['faculty_id'] != faculty_id:
        return False, "Unauthorized: You do not own this declaration"

    # 2. Check Semester Lock
    semester = get_semester_by_id(current['semester_id'])
    if semester and semester['is_locked']:
        return False, "Semester is locked. Cannot modify."

    # 3. Determine values for conflict checking (New vs Old)
    check_room = room_id if room_id else current['room_id']
    check_day = day if day else current['day_of_week']
    check_start = start if start else current['time_start']
    check_end = end if end else current['time_end']
    
    # 4. Conflict Check (Exclude self)
    # We only check conflicts if time/location changed, but checking always is safer/easier
    has_conflict, error_msg = check_schedule_conflicts(
        current['semester_id'], check_day, check_start, check_end, 
        check_room, faculty_id, exclude_declaration_id=declaration_id
    )
    if has_conflict:
        return False, error_msg

    # 5. Prepare Updates
    updates = []
    params = []

    if room_id: 
        updates.append("room_id = %s") 
        params.append(room_id)
    if subject_code: 
        updates.append("subject_code = %s") 
        params.append(subject_code)
    if class_section: 
        updates.append("class_section = %s") 
        params.append(class_section)
    if day: 
        updates.append("day_of_week = %s") 
        params.append(day)
    if start: 
        updates.append("time_start = %s") 
        params.append(start)
    if end: 
        updates.append("time_end = %s") 
        params.append(end)
    
    if not updates:
        return False, "No changes detected"

    # 6. Execute Update
    return update_declaration_record(declaration_id, updates, params)

def delete_declaration_service(declaration_id, faculty_id):
    """
    Handles deletion with lock checks.
    """
    current = get_declaration_by_id(declaration_id)
    if not current:
        return False, "Declaration not found"
        
    if current['faculty_id'] != faculty_id:
        return False, "Unauthorized"
        
    semester = get_semester_by_id(current['semester_id'])
    if semester and semester['is_locked']:
        return False, "Semester is locked. Cannot delete."
        
    return delete_declaration_record(declaration_id)