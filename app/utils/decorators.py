from functools import wraps
from flask import request, jsonify, current_app
from app.utils.security import decode_jwt_token

# --- API KEY DECORATOR (Keep this for external tools if needed) ---
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS': return jsonify({'status': 'ok'}), 200
        
        api_keys = current_app.config.get('API_KEYS', {})
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key not in api_keys:
            return jsonify({'error': 'Invalid or missing API Key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- JWT TOKEN DECORATOR (For Faculty) ---
def require_jwt_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS': return jsonify({'status': 'ok'}), 200
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing Authorization header'}), 401
        try:
            token = auth_header.split(" ")[1]
            jwt_secret = current_app.config['JWT_SECRET_KEY']
            
            payload = decode_jwt_token(token, jwt_secret)
            if not payload: return jsonify({'error': 'Invalid token'}), 401
            
            # Attach to request for use in route
            request.faculty_id = payload.get('faculty_id')
            request.username = payload.get('username')
            request.current_user = payload 
            
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- FIX: ADMIN DECORATOR (Updated to use JWT instead of API Key) ---
def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS': return jsonify({'status': 'ok'}), 200
        
        # 1. Check for Authorization Header (JWT)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing Authorization header'}), 401

        try:
            # 2. Decode Token
            token = auth_header.split(" ")[1]
            jwt_secret = current_app.config['JWT_SECRET_KEY']
            
            payload = decode_jwt_token(token, jwt_secret)
            if not payload: 
                return jsonify({'error': 'Invalid token'}), 401

            # 3. Verify Admin Privileges
            # We check if 'admin_id' exists in the payload OR if 'role' is set to 'admin'
            if not payload.get('admin_id') and payload.get('role') != 'admin':
                return jsonify({'error': 'Admin privileges required'}), 403

            # 4. Attach Admin Info to Request
            request.admin_id = payload.get('admin_id')
            request.current_user = payload

        except Exception as e:
            print(f"Admin Auth Error: {e}")
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function