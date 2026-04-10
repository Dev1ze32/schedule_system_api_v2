import re
from datetime import datetime
from functools import wraps
from flask import jsonify

# --- CONSTANTS ---
VALID_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
VALID_STATUSES = ['Pending', 'Active', 'Rejected']

# --- DATA VALIDATORS ---

def validate_password_strength(password, min_length=8):
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    # Check for whitespace only or empty
    if not password.strip():
        return False, "Password cannot be empty or just spaces"
        
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
        
    # Strict complexity checks
    if not re.search(r'[A-Z]', password): 
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password): 
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password): 
        return False, "Password must contain at least one number"
        
    return True, None

def validate_username(username):
    if not username or not isinstance(username, str):
        return False, "Username is required"
    
    # STRICT: No spaces allowed anywhere
    if ' ' in username:
        return False, "Username cannot contain spaces"
        
    username = username.strip()
    
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3-20 characters"
    
    # Regex: Only Alphanumeric, Underscore, or Dot
    if not re.match(r'^[a-zA-Z0-9_.]+$', username):
        return False, "Username can only contain letters, numbers, dots, and underscores"
    
    return True, None

def validate_time_range(start_time, end_time):
    """Validate that end time is after start time and duration is reasonable."""
    try:
        if isinstance(start_time, str):
            start = datetime.strptime(start_time, '%H:%M:%S').time()
        else:
            start = start_time
            
        if isinstance(end_time, str):
            end = datetime.strptime(end_time, '%H:%M:%S').time()
        else:
            end = end_time
            
        if start >= end:
            return False, "End time must be after start time"
        
        start_dt = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        duration = (end_dt - start_dt).total_seconds() / 3600
        
        if duration > 10:
            return False, "Class duration cannot exceed 10 hours"
            
        return True, None
    except ValueError:
        return False, "Invalid time format (Use HH:MM:SS)"

# --- FLASK ROUTE VALIDATORS ---

def validate_id_params(*param_names):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for param in param_names:
                value = kwargs.get(param)
                if value is not None:
                    if not isinstance(value, int) or value <= 0:
                        return jsonify({'error': f'Invalid {param}'}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator