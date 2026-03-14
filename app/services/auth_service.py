from app.database.connection import create_connection
from app.utils.security import verify_password, hash_password
from app.utils.validators import validate_password_strength
from app.models.admin import get_admin_by_username
from app.models.auth import update_faculty_password_record
from app.models.faculty import delete_faculty_data
from mysql.connector import Error
from datetime import datetime, timedelta
import hashlib

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30

# --- AUTHENTICATION ---

def authenticate_faculty_service(identifier, password):
    if not identifier or not password:
        return None, "Invalid credentials"
    
    conn = create_connection()
    if not conn: return None, "Database connection error"
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT l.* FROM faculty_login l
            JOIN faculty f ON l.faculty_id = f.faculty_id
            WHERE (l.username = %s OR f.email = %s)
            LIMIT 1
        """
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return None, "Invalid credentials"
        
        # Check lockout
        if user.get('locked_until') and datetime.now() < user['locked_until']:
            return None, "Account is temporarily locked. Please try again later."
        elif user.get('locked_until'):
            # Unlock
            cursor.execute("UPDATE faculty_login SET locked_until = NULL, failed_attempts = 0 WHERE login_id = %s", (user['login_id'],))
            conn.commit()
            
        if not user.get('is_active'):
            return None, "Account is disabled."
            
        # Verify Password
        if verify_password(user['password_hash'], user['password_salt'], password):
            cursor.execute("UPDATE faculty_login SET failed_attempts = 0, last_login = %s WHERE login_id = %s", (datetime.now(), user['login_id']))
            conn.commit()
            return {'faculty_id': user['faculty_id'], 'username': user['username']}, "Success"
        else:
            failed_attempts = user.get('failed_attempts', 0) + 1
            if failed_attempts >= MAX_LOGIN_ATTEMPTS:
                lockout = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
                cursor.execute("UPDATE faculty_login SET failed_attempts = %s, locked_until = %s WHERE login_id = %s", (failed_attempts, lockout, user['login_id']))
                conn.commit()
                return None, f"Too many failed attempts. Locked for {LOCKOUT_DURATION_MINUTES} mins."
            else:
                cursor.execute("UPDATE faculty_login SET failed_attempts = %s WHERE login_id = %s", (failed_attempts, user['login_id']))
                conn.commit()
                return None, f"Invalid credentials. {MAX_LOGIN_ATTEMPTS - failed_attempts} attempts remaining."
                
    except Error as e:
        print(f"Auth error: {e}")
        return None, "Authentication failed"
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def authenticate_admin_service(username, password):
    """
    Authenticates an admin using SHA256 (Legacy format).
    """
    admin = get_admin_by_username(username)
    if not admin:
        return None, "Invalid credentials"
        
    # Verify Hash (Legacy system uses simple SHA256)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if input_hash == admin['password_hash']:
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE admin_login SET last_login = NOW() WHERE admin_id = %s", (admin['admin_id'],))
                conn.commit()
            finally:
                if conn.is_connected(): cursor.close(); conn.close()
            
        return admin, "Success"
        
    return None, "Invalid credentials"

# --- ACCOUNT MANAGEMENT ---

def create_faculty_login(faculty_id, username, password):
    hashed, salt = hash_password(password)
    conn = create_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faculty_login (faculty_id, username, password_hash, password_salt, is_active, created_at) VALUES (%s, %s, %s, %s, True, NOW())", 
                       (faculty_id, username, hashed, salt))
        conn.commit()
        return cursor.lastrowid
    except Error: return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def admin_reset_faculty_password(faculty_id, new_password):
    """
    Allows an admin to force reset a faculty password.
    """
    # 1. Validate Password Strength
    valid, msg = validate_password_strength(new_password)
    if not valid: return False, msg
    
    # 2. Hash New Password
    hashed, salt = hash_password(new_password)
    
    # 3. Update DB
    return update_faculty_password_record(faculty_id, hashed, salt)

def delete_faculty_account_service(faculty_id):
    """
    Cascading delete of faculty data.
    """
    return delete_faculty_data(faculty_id)