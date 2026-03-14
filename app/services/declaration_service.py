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

def insert_declaration_service(faculty_id, room_id, semester_id, subject_code, class_section, day, start, end, status='Pending'):
    """
    Orchestrates the creation of a schedule declaration:
    1. Validates inputs (Time, Day)
    2. Checks foreign key existence (Faculty, Room, Semester)
    3. Checks business rules (Semester Locks)
    4. Checks Logic (Schedule Conflicts)
    5. Inserts the record
    """
    
    # 1. Basic Input Validation
    if day not in VALID_DAYS:
        return None, "Invalid day"
        
    valid_time, time_error = validate_time_range(start, end)
    if not valid_time:
        return None, time_error

    # 2. Existence Checks (Delegated to Models)
    # Note: These are often implicitly handled by DB constraints, but explicit checks provide better error messages.
    if not faculty_exists(faculty_id):
        return None, "Faculty not found"
    
    if not room_exists(room_id):
        return None, "Room not found"

    # 3. Semester Lock Check
    semester = get_semester_by_id(semester_id)
    if not semester:
        return None, "Semester not found"
        
    if semester['is_locked']:
        return None, "Semester is locked. No new declarations allowed."

    # 4. Conflict Check (Delegated to Conflict Service)
    has_conflict, error_msg = check_schedule_conflicts(
        semester_id, day, start, end, room_id, faculty_id
    )
    if has_conflict:
        return None, error_msg

    # 5. Insert Record (Delegated to Model)
    declaration_id, db_error = insert_declaration_record(
        faculty_id=faculty_id,
        room_id=room_id,
        semester_id=semester_id,
        subject_code=subject_code,
        class_section=class_section,
        day=day,
        start=start,
        end=end,
        status=status
    )
    
    if db_error:
        return None, db_error
        
    return declaration_id, None

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