from app.database.connection import create_connection

def _clear_cursor_results(cursor):
    """Strongest version - use this one everywhere"""
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


def check_schedule_conflicts(semester_id, day, start_time, end_time, room_id, faculty_id, exclude_declaration_id=None):
    """
    Ultra-safe conflict checker for N/A rooms.
    """
    conn = None
    cursor = None
    try:
        conn = create_connection()
        if conn:
            conn.cmd_reset_connection()
        if not conn:
            return True, "Database Connection Failed"

        cursor = conn.cursor(dictionary=True, buffered=True)
        _clear_cursor_results(cursor)   # ← Extra safety

        # 1. Get N/A room ID
        cursor.execute("""
            SELECT room_id 
            FROM room 
            WHERE TRIM(LOWER(room_name)) = 'n/a' 
            LIMIT 1
        """)
        na_res = cursor.fetchall()
        na_room_id = na_res[0]['room_id'] if na_res else None

        is_na_room = (na_room_id is not None and 
                     str(room_id).strip() == str(na_room_id).strip())

        # 2. Conflict query
        query = """
            SELECT subject_code 
            FROM work_declaration
            WHERE semester_id = %s 
              AND day_of_week = %s
              AND (time_start < %s AND time_end > %s)
              AND declaration_status != 'Rejected'
        """
        params = [semester_id, day, end_time, start_time]

        if exclude_declaration_id:
            query += " AND declaration_id != %s"
            params.append(exclude_declaration_id)

        if is_na_room:
            query += " AND faculty_id = %s"
            params.append(faculty_id)
        else:
            query += " AND (faculty_id = %s OR room_id = %s)"
            params.extend([faculty_id, room_id])

        cursor.execute(query, tuple(params))
        conflicts = cursor.fetchall()

        if conflicts:
            return True, f"Conflict detected with {conflicts[0]['subject_code']}"

        return False, None

    except Exception as e:
        print(f"CRITICAL DB ERROR IN check_schedule_conflicts: {str(e)}")
        return True, f"System Error: {str(e)}"

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
