from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.services.auth_service import authenticate_faculty_service, authenticate_admin_service
from app.utils.security import generate_jwt_token

auth_bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
@limiter.limit("5 per minute")
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Invalid credentials'}), 400
        
    user, message = authenticate_faculty_service(username.strip(), password.strip())
    
    if not user:
        return jsonify({'error': 'Authentication failed', 'message': message}), 401

    # ADD: fetch full faculty profile from DB
    from app.database.connection import create_connection
    full_faculty = None
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT faculty_name, department FROM faculty WHERE faculty_id = %s", 
                (user['faculty_id'],)
            )
            full_faculty = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    token = generate_jwt_token(
        user['faculty_id'], 
        user['username'], 
        current_app.config['JWT_SECRET_KEY'],
        role='faculty',
        faculty_name=full_faculty['faculty_name'] if full_faculty else user['username'],
        department=full_faculty.get('department', '') if full_faculty else ''
    )
    
    return jsonify({
        'message': 'Login successful', 
        'access_token': token,
        'faculty': {**user, **(full_faculty or {})}  # merge both dicts
    })

@auth_bp.route('/admin/login', methods=['POST'], strict_slashes=False)
@limiter.limit("5 per minute")
def admin_login():
    data = request.get_json() or {}
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
        
    user, message = authenticate_admin_service(data['username'], data['password'])
    
    if user:
        # Generate Admin Token
        token = generate_jwt_token(
            user['admin_id'], 
            user['admin_name'], # <--- KEY FIX: Legacy DB uses 'admin_name', not 'name'
            current_app.config['JWT_SECRET_KEY'],
            role='admin',
            expires_in=43200
        )
        
        return jsonify({
            'access_token': token,
            'token': token,
            'user': user
        })
    
    return jsonify({'message': message}), 401