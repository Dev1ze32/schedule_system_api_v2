"""
upload_service.py
-----------------
Handles schedule file uploads for:
  • CSV / XLSX / XLS  – legacy spreadsheet path (unchanged logic)
  • DOCX              – parsed by parser.process_docx
  • PDF               – parsed by parser.process_pdf
  • JPEG / JPG / PNG  – parsed by image_parser.process_image (TableLinesRemover OCR)

All non-spreadsheet blocks go through parse_event() which splits the raw
event string into (subject_code, section, room_hint), resolves the room
against the DB, and defaults anything unknown to N/A.
"""

import os
import re
import sys
import difflib
import tempfile
import logging
import csv
import io
from werkzeug.utils import secure_filename

from app.utils.file_parser import parse_schedule_file, normalize_column_names, validate_row_data, format_time
from app.database.connection import create_connection
from app.services.declaration_service import insert_declaration_service

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Allowed extensions
# ─────────────────────────────────────────────────────────────────────────────
SPREADSHEET_EXTS = {'csv', 'xlsx', 'xls'}
DOCUMENT_EXTS    = {'docx'}
PDF_EXTS         = {'pdf'}
IMAGE_EXTS       = {'jpg', 'jpeg', 'png'}
ALL_ALLOWED_EXTS = SPREADSHEET_EXTS | DOCUMENT_EXTS | PDF_EXTS | IMAGE_EXTS

# ─────────────────────────────────────────────────────────────────────────────
# Known non-class activity labels
# ─────────────────────────────────────────────────────────────────────────────
_HOUR_LABELS_FULL = [
    "Administrative Hours",
    "Consultation Hours",
    "Research Hours",
    "Community Extension Hours",
    "Break",
    "Lunch",
    "Quasi Hours",
]
_HOUR_LABELS_SHORT = [
    "Consultation", "Administrative", "Research", "Break", "Lunch", "Quasi",
]
_SHORT_TO_FULL = {
    "consultation":  "Consultation Hours",
    "administrative": "Administrative Hours",
    "research":      "Research Hours",
    "break":         "Break",
    "lunch":         "Lunch",
    "quasi":         "Quasi Hours",
}

# ─────────────────────────────────────────────────────────────────────────────
# Event parser  –  splits "CPP106 2CPEA" or "PSM113 3PSY-D RM319" correctly
# ─────────────────────────────────────────────────────────────────────────────

def _is_hour_label(text: str) -> bool:
    """Return True if this text is a known non-class activity."""
    c = re.sub(r'\s+', ' ', text).strip()
    cl = c.lower()
    if cl in [h.lower() for h in _HOUR_LABELS_FULL + _HOUR_LABELS_SHORT]:
        return True
    if difflib.get_close_matches(c, _HOUR_LABELS_FULL, n=1, cutoff=0.70):
        return True
    if difflib.get_close_matches(c, _HOUR_LABELS_SHORT, n=1, cutoff=0.70):
        return True
    return False


def _normalize_hour_label(text: str) -> str:
    """Map an hour-label string (possibly typo'd) to its canonical full form."""
    c = re.sub(r'\s+', ' ', text).strip()
    # Try full labels first
    m = difflib.get_close_matches(c, _HOUR_LABELS_FULL, n=1, cutoff=0.60)
    if m:
        return m[0]
    # Try short labels and expand
    m2 = difflib.get_close_matches(c.lower(), list(_SHORT_TO_FULL.keys()), n=1, cutoff=0.60)
    if m2:
        return _SHORT_TO_FULL[m2[0]]
    return c


def _normalize_room_token(token: str) -> str:
    """
    Updated to recognize COMLAB without merging tokens.
    """
    t = token.strip().upper()
    
    # RM + digits -> strip the RM (e.g., RM319 -> 319) 
    m = re.match(r'^RM(\d+)$', t)
    if m:
        return m.group(1)
        
    # BCH + digits -> keep as is (e.g., BCH101) 
    if re.match(r'^BCH\d+$', t):
        return t

    # NEW: If the token is 'COMLAB', return it so _resolve_room can search it
    if t == "COMLAB":
        return t
        
    # NEW: If the token is just a digit (like the '1' in 'Comlab 1'), 
    # we return it so the resolver can try to match it.
    if t.isdigit():
        return t

    return ''

def _looks_like_subject(token: str) -> bool:
    """
    A subject code is 2+ uppercase letters followed by digits, total 4-10 chars.
    Examples: CPP106, PSM113, CPP117, CHM104A
    """
    return bool(re.match(r'^[A-Za-z]{2,}[A-Za-z0-9]{1,7}$', token)) and len(token) <= 10


def _looks_like_section(token: str) -> bool:
    """
    A section starts with a digit followed by uppercase letters (2CPEA, 3PSY-D, 4CPEB).
    Or letters-dash-letter (PSY-D) when preceded by a leading digit in the full string.
    """
    t = token.strip()
    # digit + 2+ letters (e.g. 2CPEA, 4CPEB, 3PSY)
    if re.match(r'^\d[A-Za-z]{2,}', t):
        return True
    # digit + letters + dash + letter (e.g. 2PSY-D, 3CPE-A)
    if re.match(r'^\d[A-Za-z]+-[A-Za-z]$', t):
        return True
    # Letters + dash + letter only (PSY-D) — accepted as section when no digit-prefix version is found
    if re.match(r'^[A-Za-z]{2,}-[A-Za-z]$', t):
        return True
    return False


def parse_event(event_text: str) -> tuple:
    text = re.sub(r'\s+', ' ', event_text).strip()

    if _is_hour_label(text):
        return _normalize_hour_label(text), 'N/A', '' 

    # --- NEW: Handle "Comlab X" specifically before splitting ---
    # This finds 'Comlab 1' and makes it 'COMLAB 1' for the resolver
    room_match = re.search(r'(COMLAB\s+\d+)', text, re.IGNORECASE)
    room_hint = room_match.group(1).upper() if room_match else ''
    
    # Remove the room string from the text so it doesn't interfere with subject/section parsing
    if room_hint:
        text = text.replace(room_match.group(1), '')

    tokens = text.split()
    subject   = ''
    section   = ''

    for tok in tokens:
        # Check for other room tokens (RM319, etc.) if COMLAB wasn't found
        if not room_hint:
            room_candidate = _normalize_room_token(tok)
            if room_candidate:
                room_hint = room_candidate
                continue

        if not subject and _looks_like_subject(tok):
            subject = tok.upper()
            continue

        if not section and _looks_like_section(tok):
            section = tok.upper()
            continue

        # Stray short tokens / OCR noise — ignore

    if not subject:
        # Couldn't parse at all – store full text as subject, mark section N/A
        subject = text
        section = 'N/A'

    if not section:
        section = 'N/A'

    return subject, section, room_hint


# ─────────────────────────────────────────────────────────────────────────────
# Sanitisation helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sanitize_text(value: str, max_len: int = 100) -> str:
    if not value:
        return ''
    value = re.sub(r'<[^>]+>', '', str(value))
    value = re.sub(r'\s+', ' ', value).strip()
    return value[:max_len]


def _normalize_day(raw_day: str):
    if not raw_day:
        return None
    lower = raw_day.strip().lower()
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        if lower.startswith(day[:3]):
            return day.capitalize()
    return None


def _is_gibberish(text: str) -> bool:
    if not text:
        return True
    alnum_ratio = sum(c.isalnum() for c in text) / max(len(text), 1)
    if alnum_ratio < 0.4:
        return True
    tokens = text.split()
    if len(tokens) > 3 and all(len(t) <= 3 for t in tokens):
        return True
    return False


def _fix_time(t: str):
    t = str(t).strip()
    if re.match(r'^\d{1,2}:\d{2}$', t):
        return t + ':00'
    if re.match(r'^\d{1,2}:\d{2}:\d{2}$', t):
        return t
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Room resolution
# ─────────────────────────────────────────────────────────────────────────────

def _build_room_map(cursor):
    cursor.execute("SELECT room_id, room_name FROM room WHERE room_name IS NOT NULL")
    rooms = cursor.fetchall()
    room_map = {str(r['room_name']).strip().lower(): r['room_id'] for r in rooms}
    cursor.execute("SELECT room_id FROM room WHERE TRIM(LOWER(room_name)) = 'n/a' LIMIT 1")
    na_res = cursor.fetchall()
    na_room_id = na_res[0]['room_id'] if na_res else None
    return room_map, na_room_id


def _resolve_room(raw_room: str, room_map: dict, na_room_id, cursor):
    """
    Resolve a room name string to a room_id.
    Falls back to N/A for empty/unknown values.
    """
    raw = (raw_room or '').strip()
    if not raw or raw.upper() == 'N/A':
        return na_room_id

    # Exact case-insensitive lookup
    room_id = room_map.get(raw.lower())
    if room_id:
        return room_id

    # Fallback DB query
    cursor.execute(
        "SELECT room_id FROM room WHERE LOWER(room_name) = LOWER(%s) LIMIT 1",
        (raw,)
    )
    res = cursor.fetchall()
    if res:
        return res[0]['room_id']

    logger.warning("Room '%s' not found in DB – defaulting to N/A", raw)
    return na_room_id


# ─────────────────────────────────────────────────────────────────────────────
# Path helper — makes parser.py and image_parser.py importable from project root
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_root_on_path():
    """
    parser.py and image_parser.py live in the project root (/app).
    This file is at /app/app/services/upload_service.py, so walk up two dirs.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
        logger.debug("Added project root to sys.path: %s", root)


# ─────────────────────────────────────────────────────────────────────────────
# Spreadsheet path (CSV / XLSX / XLS) — original logic, sanitisation added
# ─────────────────────────────────────────────────────────────────────────────

def _process_spreadsheet(temp_path, faculty_id, semester_id, cursor, room_map, na_room_id):
    raw_data, parse_error = parse_schedule_file(temp_path)
    if parse_error:
        return None, {'message': 'File parsing failed', 'errors': [parse_error]}

    validation_errors = []
    valid_rows = []

    for index, raw_row in enumerate(raw_data):
        row_num = index + 2
        row = normalize_column_names(raw_row)
        is_valid, error_msg = validate_row_data(row)
        if not is_valid:
            validation_errors.append(f"Row {row_num}: {error_msg}")
            continue

        raw_room = str(row.get('room', '')).strip()
        room_id = _resolve_room(raw_room, room_map, na_room_id, cursor)
        if room_id is None:
            validation_errors.append(
                f"Row {row_num}: Room '{raw_room}' not found and N/A room is not configured."
            )
            continue

        start = format_time(row.get('start_time'))
        end   = format_time(row.get('end_time'))
        if not start or not end or start >= end:
            validation_errors.append(f"Row {row_num}: Invalid time range.")
            continue

        day = _normalize_day(str(row.get('day', '')))
        if not day:
            validation_errors.append(f"Row {row_num}: Unrecognised day '{row.get('day')}'.")
            continue

        subject = _sanitize_text(str(row.get('subject_code', '')), 50)
        section = _sanitize_text(str(row.get('section', 'N/A')), 50) or 'N/A'

        valid_rows.append({
            'room_id':       room_id,
            'subject_code':  subject,
            'class_section': section,
            'day':           day,
            'start_time':    start,
            'end_time':      end,
            'row_num':       row_num,
        })

    if validation_errors:
        return None, {
            'message': 'Upload rejected due to errors.',
            'summary': {'successful': 0, 'failed': len(validation_errors)},
            'errors': validation_errors,
        }

    return valid_rows, None


# ─────────────────────────────────────────────────────────────────────────────
# DOCX / PDF / Image path — parse_event splits each block properly
# ─────────────────────────────────────────────────────────────────────────────

def _blocks_to_rows(blocks: list, room_map: dict, na_room_id, cursor, source_label='file') -> tuple:
    """
    Convert parser output blocks [{day, event, start, end}, …] into
    insertion-ready rows with properly split subject_code, class_section, room.

    parse_event() handles all the splitting logic:
      - 'CPP106 2CPEA'         -> subject=CPP106, section=2CPEA, room=N/A
      - 'PSM113 3PSY-D RM319'  -> subject=PSM113, section=3PSY-D, room=319 -> room_id
      - 'Research Hours'       -> subject=Research Hours, section=N/A, room=N/A
    """
    valid_rows = []
    skipped = 0

    for i, block in enumerate(blocks):
        # --- Basic block validation ---
        day = _normalize_day(str(block.get('day', '')))
        if not day:
            skipped += 1
            continue

        raw_event = _sanitize_text(str(block.get('event', '')), max_len=300)
        if not raw_event or _is_gibberish(raw_event):
            skipped += 1
            continue

        start = _fix_time(str(block.get('start', '')))
        end   = _fix_time(str(block.get('end', '')))
        if not start or not end or start >= end:
            skipped += 1
            continue

        # --- Split event text into subject / section / room ---
        subject_code, class_section, room_hint = parse_event(raw_event)

        # --- Resolve room ---
        # room_hint comes from parse_event (e.g. '319' stripped from 'RM319')
        room_id = _resolve_room(room_hint, room_map, na_room_id, cursor)
        if room_id is None:
            logger.warning("Block %d: no N/A room configured, skipping.", i)
            skipped += 1
            continue

        # --- Final sanitisation on split fields ---
        subject_code  = _sanitize_text(subject_code, 100)
        class_section = _sanitize_text(class_section, 50) or 'N/A'

        if not subject_code:
            skipped += 1
            continue

        valid_rows.append({
            'room_id':       room_id,
            'subject_code':  subject_code,
            'class_section': class_section,
            'day':           day,
            'start_time':    start,
            'end_time':      end,
            'row_num':       i + 1,
        })

    logger.info("[%s] %d valid rows, %d skipped.", source_label, len(valid_rows), skipped)
    return valid_rows, None


# ─────────────────────────────────────────────────────────────────────────────
# Insertion loop (shared by all paths)
# ─────────────────────────────────────────────────────────────────────────────

def _insert_rows(valid_rows, faculty_id, semester_id, na_room_id):
    successful = 0
    execution_errors = []

    for item in valid_rows:
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
                status='Pending',
            )
            if dec_id:
                successful += 1
            else:
                execution_errors.append(f"Row {item['row_num']}: {db_error}")
        except Exception as row_e:
            execution_errors.append(f"Row {item['row_num']}: {str(row_e)}")

    return successful, execution_errors


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


# ─────────────────────────────────────────────────────────────────────────────
# Main public entry-point
# ─────────────────────────────────────────────────────────────────────────────

def process_schedule_upload(file, semester_id, faculty_id):
    logger.info("=== UPLOAD STARTED: %s ===", file.filename)

    temp_path = None
    conn = None
    cursor = None

    try:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

        if ext not in ALL_ALLOWED_EXTS:
            return None, {
                'message': (
                    f"Unsupported file type '.{ext}'. "
                    f"Allowed: {', '.join(sorted(ALL_ALLOWED_EXTS))}"
                ),
                'errors': [],
            }

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
            file.save(tmp.name)
            temp_path = tmp.name

        # DB connection + room map
        conn = create_connection()
        if not conn:
            return None, {'error': 'Database connection failed'}
        conn.cmd_reset_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        room_map, na_room_id = _build_room_map(cursor)

        # ── Dispatch by extension ────────────────────────────────────────────
        if ext in SPREADSHEET_EXTS:
            valid_rows, err = _process_spreadsheet(
                temp_path, faculty_id, semester_id, cursor, room_map, na_room_id
            )
            if err:
                return None, err

        elif ext in DOCUMENT_EXTS:
            try:
                _ensure_root_on_path()
                from app.services.parser import process_docx
            except ImportError as e:
                logger.error("DOCX import failed: %s", e)
                return None, {'message': f'DOCX parser could not be loaded: {e}', 'errors': []}
            blocks = process_docx(temp_path)
            if not blocks:
                return None, {'message': 'No schedule data found in the DOCX file.', 'errors': []}
            valid_rows, err = _blocks_to_rows(blocks, room_map, na_room_id, cursor, 'DOCX')
            if err:
                return None, err

        elif ext in PDF_EXTS:
            try:
                _ensure_root_on_path()
                from app.services.parser import process_pdf
            except ImportError as e:
                logger.error("PDF import failed: %s", e)
                return None, {'message': f'PDF parser could not be loaded: {e}', 'errors': []}
            blocks = process_pdf(temp_path)
            if not blocks:
                return None, {'message': 'No schedule data found in the PDF file.', 'errors': []}
            valid_rows, err = _blocks_to_rows(blocks, room_map, na_room_id, cursor, 'PDF')
            if err:
                return None, err

        elif ext in IMAGE_EXTS:
            try:
                _ensure_root_on_path()
                from app.services.image_parser import process_image
            except ImportError as e:
                logger.error("Image parser import failed: %s", e)
                return None, {'message': f'Image parser could not be loaded: {e}', 'errors': []}
            blocks = process_image(temp_path)
            if not blocks:
                return None, {'message': 'No schedule data could be extracted from the image.', 'errors': []}
            valid_rows, err = _blocks_to_rows(blocks, room_map, na_room_id, cursor, 'IMAGE')
            if err:
                return None, err

        else:
            return None, {'message': f"Unsupported extension: {ext}", 'errors': []}

        if not valid_rows:
            return None, {
                'message': 'No valid schedule rows could be extracted from the file.',
                'errors': [],
            }

        # ── Insert ───────────────────────────────────────────────────────────
        successful, execution_errors = _insert_rows(valid_rows, faculty_id, semester_id, na_room_id)

        return {
            'message': 'Upload successful!',
            'summary': {'successful': successful, 'failed': len(execution_errors)},
            'errors': execution_errors,
        }, None

    except Exception as e:
        logger.error("UPLOAD CRASHED: %s", str(e), exc_info=True)
        return None, {'error': 'Upload failed', 'message': str(e)}

    finally:
        if cursor:
            _clear_cursor_results(cursor)
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


# ─────────────────────────────────────────────────────────────────────────────
# CSV template generator (unchanged)
# ─────────────────────────────────────────────────────────────────────────────

def generate_template_csv():
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
            logger.error("Template DB Error: %s", e)
        finally:
            if cursor:
                try:
                    if cursor.with_rows:
                        cursor.fetchall()
                    cursor.close()
                except Exception:
                    pass
            if conn.is_connected():
                conn.close()

    if not real_rooms:
        real_rooms = ['BCH101', 'BCH102', 'BCH103', '301']

    while len(real_rooms) < 4:
        real_rooms.append(real_rooms[0])

    headers = ['Day', 'Start Time', 'End Time', 'Subject Code', 'Section', 'Room', 'Activity Type']
    rows = [
        ['Monday',    '07:30', '10:00', 'CPP106', '2CPEA', real_rooms[0], 'Class'],
        ['Monday',    '10:00', '11:30', 'Research Hours', 'N/A', 'N/A', 'Research Hours'],
        ['Tuesday',   '10:00', '11:30', 'CPP106', '2CPEB', real_rooms[2], 'Class'],
        ['Wednesday', '13:00', '16:00', 'CPP117', '4CPEA', real_rooms[3], 'Class'],
    ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)

    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return mem