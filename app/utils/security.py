import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
import os

# --- PASSWORD SECURITY ---

def hash_password(password, salt=None):
    """Secure password hashing using PBKDF2-HMAC-SHA256 (Used for Faculty)."""
    if salt is None: 
        salt = secrets.token_hex(16)
    
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        200000 
    )
    return hash_bytes.hex(), salt

def verify_password(stored_hash, stored_salt, provided_password):
    hashed, _ = hash_password(provided_password, stored_salt)
    return secrets.compare_digest(hashed, stored_hash)

# --- ADMIN PASSWORD SECURITY (SHA256 - Legacy) ---

def hash_sha256(password):
    """
    Simple SHA256 hashing.
    REQUIRED: The legacy system used this for Admins. 
    Without this, Admin login will fail.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_sha256(stored_hash, provided_password):
    """Verifies a legacy SHA256 password."""
    input_hash = hash_sha256(provided_password)
    return secrets.compare_digest(input_hash, stored_hash)

# --- JWT TOKENS ---

def generate_jwt_token(user_id, username, secret_key, role='faculty', expires_in=3600):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'role': role,
        'type': 'access'
    }
    
    if role == 'admin':
        payload['admin_id'] = user_id
    else:
        payload['faculty_id'] = user_id

    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(
            token, 
            secret_key, 
            algorithms=['HS256'],
            options={'verify_exp': True} 
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None 
    except Exception as e:
        print(f"JWT decode error: {e}")
        return None