from app.database.connection import create_connection
from mysql.connector import Error
from datetime import datetime

# Import Model Functions
from app.models.semester import (
    get_semester_by_id,
    get_all_semesters,
    get_active_semester,
    create_semester_record,
    update_semester_record,
    delete_semester_data
)

# --- SERVICE FUNCTIONS ---

def create_semester_service(name, code, year, start, end):
    """
    Creates a semester with strict validation:
    1. Start Date must be in the current year (or future).
    2. Duration must be between 5 to 6 months (approx 150-185 days).
    """
    # --- 1. PARSE DATES ---
    try:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return None, "Invalid date format. Use YYYY-MM-DD."

    # --- 2. VALIDATE CURRENT YEAR ---
    current_year = datetime.now().year
    if start_date.year < current_year:
        return None, f"Cannot create a semester for a past year ({start_date.year}). It must be {current_year} or later."

    # --- 3. VALIDATE DURATION (5-6 MONTHS) ---
    # We use days for accuracy:
    # 5 months ~= 150 days
    # 6 months ~= 185 days (allowing for 31-day months)
    duration_days = (end_date - start_date).days
    
    if duration_days < 150:
        return None, "Semester is too short. Minimum duration is 5 months."
    if duration_days > 185:
        return None, "Semester is too long. Maximum duration is 6 months."

    # --- 4. CREATE RECORD ---
    # Pass the tuple (id, error) back to the route
    return create_semester_record(name, code, year, start, end)

def update_semester_service(semester_id, name, code, year, start, end):
    semester = get_semester_by_id(semester_id)
    if not semester:
        return False, "Semester not found"
    if semester['is_active']:
        return False, "Cannot edit an Active semester. Deactivate it first."
    
    # (Optional) You can add the same date validation logic here if you want to enforce it on updates too.
        
    return update_semester_record(semester_id, name, code, year, start, end)

def activate_semester_service(semester_id):
    """
    Business logic to activate a semester:
    1. Locks the row
    2. Checks rules (already active, locked?)
    3. Deactivates others
    4. Activates this one
    5. Updates pending declarations
    """
    conn = create_connection()
    if conn:
        conn.cmd_reset_connection()
    if not conn: return False, "Database connection failed", 0
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        conn.start_transaction(isolation_level='SERIALIZABLE')
        
        cursor.execute("SELECT * FROM semester WHERE semester_id = %s FOR UPDATE", (semester_id,))
        semester = cursor.fetchone()
        
        if not semester:
            conn.rollback()
            return False, "Semester not found", 0
        
        if semester['is_active']:
            conn.rollback()
            return False, "Semester is already active", 0
        if semester['is_locked']:
            conn.rollback()
            return False, "Semester is locked", 0
        
        # Deactivate all active semesters
        cursor.execute("UPDATE semester SET is_active = 0 WHERE is_active = 1")
        
        # Activate target semester
        cursor.execute("UPDATE semester SET is_active = 1, is_locked = 1, activated_at = %s WHERE semester_id = %s", (datetime.now(), semester_id))
        
        # Auto-approve Pending declarations
        cursor.execute("UPDATE work_declaration SET declaration_status = 'Active' WHERE semester_id = %s AND declaration_status = 'Pending'", (semester_id,))
        
        affected = cursor.rowcount
        conn.commit()
        return True, f"Semester activated. {affected} declarations updated.", affected
    except Error as e:
        if conn: conn.rollback()
        return False, str(e), 0
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def deactivate_semester_service(semester_id):
    conn = create_connection()
    if not conn: return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE semester SET is_active = 0, deactivated_at = %s WHERE semester_id = %s", (datetime.now(), semester_id))
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Semester deactivated"
        return False, "Semester not found"
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def delete_semester_service(semester_id):
    semester = get_semester_by_id(semester_id)
    if not semester:
        return False, "Semester not found"
    if semester['is_active']:
        return False, "Cannot delete an Active semester. Deactivate it first."
        
    return delete_semester_data(semester_id)

def get_semester_statistics(semester_id):
    """
    Counts declarations by status for a given semester.
    """
    conn = create_connection()
    if not conn: return None
    
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        query = """
        SELECT 
            declaration_status,
            COUNT(*) as count
        FROM work_declaration
        WHERE semester_id = %s
        GROUP BY declaration_status
        """
        
        cursor.execute(query, (semester_id,))
        results = cursor.fetchall()
        
        stats = {
            'pending': 0,
            'active': 0,
            'rejected': 0,
            'total': 0
        }
        
        for row in results:
            status = row['declaration_status'].lower()
            if status in stats:
                stats[status] = row['count']
            stats['total'] += row['count']
        
        return stats
        
    except Error as e:
        print(f"Error getting statistics: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()