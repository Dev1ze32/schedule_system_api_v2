import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls']

def parse_schedule_file(file_path):
    """
    Reads a CSV or Excel file and returns a raw list of schedule rows.
    """
    if not os.path.exists(file_path):
        return None, "File not found"

    try:
        # Determine file type and load
        # FIX: keep_default_na=False ensures "N/A" is read as the text "N/A", not as Null/Empty.
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8-sig', keep_default_na=False)
        else:
            df = pd.read_excel(file_path, keep_default_na=False)
            
        # Clean Headers
        df.columns = df.columns.str.strip()
            
        # Clean the Data (Only drop rows that are completely empty)
        df.dropna(how='all', inplace=True)
        
        # Note: We don't need fillna('') anymore because keep_default_na=False 
        # already loaded empty cells as empty strings '' instead of NaN.

        # Convert to List of Dictionaries
        raw_data = df.to_dict(orient='records')
        return raw_data, None

    except Exception as e:
        print(f"Error parsing file: {e}")
        return None, str(e)


def normalize_column_names(row):
    """
    Normalize different possible column name variations.
    """
    normalized = {}
    
    key_mappings = {
        'room': ['room', 'room_name', 'room_number', 'Room'],
        'day': ['day', 'day_of_week', 'Day'],
        'start_time': ['start_time', 'time_start', 'Start Time', 'start', 'Start'],
        'end_time': ['end_time', 'time_end', 'End Time', 'end', 'End'],
        'subject_code': ['subject_code', 'subject', 'Subject Code', 'course', 'Subject'],
        'section': ['section', 'Section', 'class_section', 'Class Section', 'Section ', 'SECTION'], 
        'activity_type': ['activity_type', 'Activity Type', 'type']
    }
    
    for standard_key, variations in key_mappings.items():
        for var in variations:
            if var in row:
                val = str(row[var]).strip()
                # Check for 'nan' string just in case, but keep everything else
                if val and val.lower() != 'nan': 
                    normalized[standard_key] = val
                break
    
    return normalized


def validate_row_data(row):
    """
    Validate that a row has all required fields.
    """
    required_fields = ['room', 'day', 'start_time', 'end_time', 'subject_code', 'section']
    
    for field in required_fields:
        # Check if field exists. 
        # Note: We allow "N/A" as a valid section now because it's a string.
        if field not in row or not row[field]:
            if field == 'section':
                return False, "Missing required field: Section"
            return False, f"Missing required field: {field}"
    
    return True, None


def format_time(time_str):
    """
    Convert various time formats to HH:MM:SS.
    """
    time_str = str(time_str).strip()
    
    try:
        # Try parsing common formats
        for fmt in ['%H:%M:%S', '%H:%M', '%I:%M %p', '%I:%M:%S %p']:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.strftime('%H:%M:%S')
            except ValueError:
                continue
        
        # Fallback manual parsing
        if ':' in time_str:
            parts = time_str.split(':')
            hour = int(parts[0])
            minute = int(parts[1].split()[0]) 
            
            if 'PM' in time_str.upper() and hour < 12:
                hour += 12
            elif 'AM' in time_str.upper() and hour == 12:
                hour = 0
                
            return f"{hour:02d}:{minute:02d}:00"
            
    except Exception as e:
        return None
    
    return None

def validate_file_extension(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_EXTENSIONS