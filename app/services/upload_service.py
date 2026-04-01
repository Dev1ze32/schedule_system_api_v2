import os
import tempfile
import csv
import io
from werkzeug.utils import secure_filename
from app.utils.file_parser import parse_schedule_file, normalize_column_names, validate_row_data, format_time
from app.models.room import get_room_id
from app.database.connection import create_connection
from app.services.declaration_service import insert_declaration_service

def process_schedule_upload(file, semester_id, faculty_id):
    """
    Handles the full process of parsing a file, validating all rows, 
    and inserting them if the entire file is valid.
    """
    temp_path = None
    try:
        # 1. Save to Temp File
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # 2. Parse File
        raw_data, parse_error = parse_schedule_file(temp_path)
        if parse_error:
            return None, {'message': 'File parsing failed', 'errors': [parse_error]}

        # 3. Validate Rows
        validation_errors = []
        valid_rows_for_insertion = []

        for index, raw_row in enumerate(raw_data):
            row_num = index + 2  # Account for header
            row = normalize_column_names(raw_row)

            # Structure Check
            is_valid_structure, error_msg = validate_row_data(row)
            if not is_valid_structure:
                validation_errors.append(f"Row {row_num}: {error_msg}")
                continue 

            # Room Check
            room_name = row.get('room', '').strip()
            room_id = get_room_id(room_name)
            if not room_id:
                validation_errors.append(f"Row {row_num}: Room '{room_name}' does not exist.")
                continue

            # Time Format Check
            start = format_time(row.get('start_time'))
            end = format_time(row.get('end_time'))
            
            if not start or not end:
                validation_errors.append(f"Row {row_num}: Invalid time format.")
                continue
            if start >= end:
                validation_errors.append(f"Row {row_num}: Start time must be before End.")
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

        # 4. Decision: Abort if any validation errors
        if len(validation_errors) > 0:
            return None, {
                'message': 'Upload rejected due to errors.',
                'summary': {'successful': 0, 'failed': len(validation_errors)},
                'errors': validation_errors
            }

        # 5. Execution: Insert Data (FIXED VERSION)
        successful_inserts = 0
        execution_errors = []

        # Get one connection for the whole file to avoid overhead
        conn = create_connection()
        if not conn:
            return None, {'error': 'Upload failed', 'message': 'Could not establish database connection'}

        try:
            # IMPORTANT: Using buffered=True to prevent "Unread result found" errors
            # This ensures Python reads the full response from MySQL immediately.
            cursor = conn.cursor(dictionary=True, buffered=True)

            for item in valid_rows_for_insertion:
                try:
                    # 1. Per-row Semester Lock Check (consumes results immediately due to buffered=True)
                    cursor.execute("SELECT is_locked FROM semester WHERE semester_id = %s", (int(semester_id),))
                    sem = cursor.fetchone()
                    
                    if sem and sem['is_locked']:
                        execution_errors.append(f"Row {item['row_num']}: Semester is locked.")
                        continue

                    # 2. Insert the declaration
                    insert_query = """
                        INSERT INTO work_declaration 
                        (faculty_id, room_id, semester_id, subject_code, class_section, day_of_week, 
                         time_start, time_end, declaration_status, uploaded_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    insert_args = (
                        faculty_id, 
                        item['room_id'], 
                        int(semester_id), 
                        item['subject_code'], 
                        item['class_section'], 
                        item['day'], 
                        item['start_time'], 
                        item['end_time'], 
                        'Pending'
                    )
                    
                    cursor.execute(insert_query, insert_args)
                    successful_inserts += 1

                except Exception as row_error:
                    execution_errors.append(f"Row {item['row_num']}: {str(row_error)}")

            # Commit all changes at once after the loop finishes
            conn.commit()

        except Exception as global_error:
            if conn: conn.rollback()
            print(f"Global Insertion Error: {global_error}")
            return None, {'error': 'Database processing failed', 'message': str(global_error)}

        finally:
            # Clean up: Close cursor and return connection to the pool
            if 'cursor' in locals(): cursor.close()
            if conn.is_connected(): conn.close()

        # Final Return Structure
        return {
            'message': 'Upload processed',
            'summary': {
                'successful': successful_inserts, 
                'failed': len(execution_errors)
            },
            'errors': execution_errors
        }, None

    except Exception as e:
        print(f"Service Error: {e}")
        return None, {'error': 'Upload failed', 'message': str(e)}
    finally:
        # Cleanup
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

def validate_schedule_preview(file):
    """
    Parses and validates the file without inserting, returning a preview.
    """
    temp_path = None
    try:
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        raw_data, parse_error = parse_schedule_file(temp_path)
        
        if parse_error:
            return None, parse_error
        
        validation_results = []
        valid_count = 0
        invalid_count = 0
        
        # Preview first 100 rows
        for i, raw_row in enumerate(raw_data[:100], start=1): 
            row = normalize_column_names(raw_row)
            is_valid, error = validate_row_data(row)
            
            # Additional format checks for preview
            if is_valid:
                start = format_time(row.get('start_time', ''))
                end = format_time(row.get('end_time', ''))
                if not start or not end:
                    is_valid = False
                    error = "Invalid time format"
            
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
            
            validation_results.append({
                'row': i,
                'valid': is_valid,
                'data': row,
                'error': error
            })
            
        return {
            'total_rows': len(raw_data),
            'preview_rows': len(validation_results),
            'valid': valid_count,
            'invalid': invalid_count,
            'validation_results': validation_results
        }, None
        
    except Exception as e:
        return None, str(e)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

def generate_template_csv():
    """
    Generates the CSV template with example room data.
    """
    real_rooms = []
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT room_name FROM room LIMIT 4")
            results = cursor.fetchall()
            real_rooms = [row['room_name'] for row in results]
        finally:
            if conn.is_connected(): conn.close()
    
    if not real_rooms:
        real_rooms = ['Room 101', 'Room 102', 'Lab 1', 'Conference Room']

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