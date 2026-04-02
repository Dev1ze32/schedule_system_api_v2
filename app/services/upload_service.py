import os
import tempfile
import logging
import csv  # <-- Added for template generation
import io   # <-- Added for template generation
from werkzeug.utils import secure_filename

from app.utils.file_parser import parse_schedule_file, normalize_column_names, validate_row_data, format_time
from app.database.connection import create_connection
from app.services.declaration_service import insert_declaration_service

logger = logging.getLogger(__name__)

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


def process_schedule_upload(file, semester_id, faculty_id):
    logger.info("=== UPLOAD STARTED ===")
    logger.info(f"File: {file.filename}")

    temp_path = None
    conn = None
    cursor = None

    try:
        # Save file
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        raw_data, parse_error = parse_schedule_file(temp_path)
        if parse_error:
            return None, {'message': 'File parsing failed', 'errors': [parse_error]}

        logger.info(f"Parsed {len(raw_data)} rows")

        # Database connection
        conn = create_connection()
        if not conn:
            return None, {'error': 'Database connection failed'}

        conn.cmd_reset_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Simple room lookup (safe version)
        cursor.execute("SELECT room_id, room_name FROM room WHERE room_name IS NOT NULL")
        rooms = cursor.fetchall()
        room_map = {str(row['room_name']).strip().lower(): row['room_id'] for row in rooms}

        cursor.execute("SELECT room_id FROM room WHERE TRIM(LOWER(room_name)) = 'n/a' LIMIT 1")
        na_res = cursor.fetchall()
        na_room_id = na_res[0]['room_id'] if na_res else None

        # Validation
        validation_errors = []
        valid_rows_for_insertion = []

        for index, raw_row in enumerate(raw_data):
            row_num = index + 2
            row = normalize_column_names(raw_row)

            is_valid, error_msg = validate_row_data(row)
            if not is_valid:
                validation_errors.append(f"Row {row_num}: {error_msg}")
                continue

            room_name_input = str(row.get('room', '')).strip()
            room_id = room_map.get(room_name_input.lower())

            if not room_id and room_name_input:
                cursor.execute("SELECT room_id FROM room WHERE LOWER(room_name) = LOWER(%s) LIMIT 1", (room_name_input,))
                fallback = cursor.fetchall()
                if fallback:
                    room_id = fallback[0]['room_id']

            if not room_id:
                validation_errors.append(f"Row {row_num}: Room '{room_name_input}' does not exist.")
                continue

            start = format_time(row.get('start_time'))
            end = format_time(row.get('end_time'))

            if not start or not end or start >= end:
                validation_errors.append(f"Row {row_num}: Invalid time")
                continue

            valid_rows_for_insertion.append({
                'room_id': room_id,
                'subject_code': row.get('subject_code'),
                'class_section': row.get('section'),
                'day': row.get('day'),
                'start_time': start,
                'end_time': end,
                'row_num': row_num
            })

        if validation_errors:
            return None, {
                'message': 'Upload rejected due to errors.',
                'summary': {'successful': 0, 'failed': len(validation_errors)},
                'errors': validation_errors
            }

        # Insertion
        successful_inserts = 0
        execution_errors = []

        for item in valid_rows_for_insertion:
            try:
                dec_id, db_error = insert_declaration_service(
                    faculty_id=faculty_id,
                    room_id=item['room_id'],
                    semester_id=int(semester_id),
                    subject_code=item['subject_code'],
                    class_section=item['class_section'],
                    day=item['day'],
                    start=item['start_time'],
                    end=item['end_time'],
                    na_room_id=na_room_id,
                    status='Pending'
                )
                if dec_id:
                    successful_inserts += 1
                else:
                    execution_errors.append(f"Row {item['row_num']}: {db_error}")
            except Exception as row_e:
                execution_errors.append(f"Row {item['row_num']}: {str(row_e)}")

        return {
            'message': 'Upload successful!',
            'summary': {'successful': successful_inserts, 'failed': len(execution_errors)},
            'errors': execution_errors
        }, None

    except Exception as e:
        logger.error(f"UPLOAD CRASHED: {str(e)}", exc_info=True)
        return None, {'error': 'Upload failed', 'message': str(e)}

    finally:
        if cursor:
            _clear_cursor_results(cursor)
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

# ADD THIS AT THE BOTTOM OF THE FILE
def generate_template_csv():
    import csv  
    import io   
    """
    Generates the CSV template with example room data safely.
    """
    real_rooms = []
    conn = create_connection()
    cursor = None
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT room_name FROM room WHERE room_name IS NOT NULL LIMIT 4")
            results = cursor.fetchall()
            real_rooms = [row['room_name'] for row in results]
        except Exception as e:
            print(f"Template DB Error: {e}", flush=True)
        finally:
            # We MUST close the cursor before the connection, or MySQL panics
            if cursor:
                try:
                    if cursor.with_rows: cursor.fetchall()
                    cursor.close()
                except Exception:
                    pass
            if conn.is_connected():
                conn.close()
    
    # Fallback if the database is empty or connection failed
    if not real_rooms:
        real_rooms = ['BCH101', 'BCH102', 'BCH103', '301']

    # Ensure we have exactly 4 items for the template rows
    while len(real_rooms) < 4:
        real_rooms.append(real_rooms[0])

    headers = ['Day', 'Start Time', 'End Time', 'Subject Code', 'Section', 'Room', 'Activity Type']
    
    rows = [
        ['Monday', '07:30', '10:00', 'CPP106', '2CPEA', real_rooms[0], 'Class'],
        ['Monday', '10:00', '11:30', 'Research', 'N/A', real_rooms[1], 'Research Hours'],
        ['Tuesday', '10:00', '11:30', 'CPP106', '2CPEB', real_rooms[2], 'Class'],
        ['Wednesday', '13:00', '16:00', 'CPP117', '4CPEA', real_rooms[3], 'Class']
    ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return mem