from flask import Blueprint, jsonify, request
from app.models.faculty import get_all_faculty_details, insert_faculty, delete_faculty_data
from app.models.admin import get_all_admins
from app.models.declaration import get_faculty_schedule_data
from app.utils.decorators import require_admin
from app.utils.validators import validate_id_params, validate_username, validate_password_strength
from app.services.auth_service import (
    admin_reset_faculty_password, 
    delete_faculty_account_service,
    create_faculty_login
)
from app.services.admin_service import (
    create_admin_account_service, 
    delete_admin_service, 
    reset_admin_password_service
)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create-faculty', methods=['POST'], strict_slashes=False)
@require_admin
def admin_create_faculty():
    data = request.get_json() or {}
    
    # Check basic fields
    if not data.get('faculty_name') or not data.get('email'):
        return jsonify({'error': 'Name and Email are required'}), 400

    # --- 1. VALIDATE USERNAME & PASSWORD BEFORE CREATING ANYTHING ---
    if 'username' in data:
        is_valid_user, user_msg = validate_username(data['username'])
        if not is_valid_user:
            return jsonify({'error': user_msg}), 400

    if 'password' in data:
        is_valid_pass, pass_msg = validate_password_strength(data['password'])
        if not is_valid_pass:
            return jsonify({'error': pass_msg}), 400
    # ----------------------------------------------------------------

    # 2. Create Profile
    faculty_id = insert_faculty(data['faculty_name'], data['email'], data.get('department', 'N/A'))
    if not faculty_id:
        return jsonify({'error': 'Failed to create profile (Email might already exist)'}), 400
        
    # 3. Create Login (If provided)
    if 'username' in data and 'password' in data:
        login_id = create_faculty_login(faculty_id, data['username'], data['password'])
        
        if not login_id:
             # Rollback: If login creation fails (e.g. duplicate username), delete the profile we just made
             delete_faculty_data(faculty_id) 
             return jsonify({'error': 'Username already taken or invalid'}), 409
             
    return jsonify({'message': 'Faculty created', 'faculty_id': faculty_id}), 201

@admin_bp.route('/faculty', methods=['GET'])
@require_admin
def admin_get_faculty():
    faculty = get_all_faculty_details()
    return jsonify(faculty)

# --- PUBLIC ROUTES (no auth required) ---

@admin_bp.route('/faculty/all', methods=['GET'], strict_slashes=False)
def public_get_all_faculty():
    faculty = get_all_faculty_details()
    return jsonify(faculty)

@admin_bp.route('/faculty/<int:faculty_id>/schedule', methods=['GET'], strict_slashes=False)
def public_get_faculty_schedule(faculty_id):
    semester_id = request.args.get('semester_id', type=int)
    schedule = get_faculty_schedule_data(faculty_id, semester_id)
    return jsonify(schedule)

@admin_bp.route('/faculty/<int:faculty_id>', methods=['DELETE'])
@require_admin
@validate_id_params('faculty_id')
def admin_delete_faculty(faculty_id):
    success, message = delete_faculty_account_service(faculty_id)
    return jsonify({'message' if success else 'error': message}), 200 if success else 400

@admin_bp.route('/reset-password', methods=['POST'])
@require_admin
def admin_reset_pw():
    data = request.get_json() or {}
    if 'faculty_id' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing faculty_id or new_password'}), 400
        
    # --- VALIDATE PASSWORD HERE TOO ---
    is_valid, msg = validate_password_strength(data['new_password'])
    if not is_valid:
        return jsonify({'error': msg}), 400
    # ----------------------------------
        
    success, message = admin_reset_faculty_password(data['faculty_id'], data['new_password'])
    return jsonify({'message' if success else 'error': message}), 200 if success else 400

# --- ADMIN ACCOUNT MANAGEMENT ---

@admin_bp.route('/accounts', methods=['GET'])
@require_admin
def list_admins():
    return jsonify(get_all_admins())

@admin_bp.route('/create-admin', methods=['POST'], strict_slashes=False)
@require_admin
def create_new_admin():
    data = request.get_json() or {}
    required = ('name', 'email', 'username', 'password')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400

    # 1. Validate Username (Check spaces, special chars)
    is_valid_user, user_msg = validate_username(data['username'])
    if not is_valid_user:
        # Returns 400 Bad Request with SPECIFIC error message
        return jsonify({'error': user_msg}), 400

    # 2. Validate Password Strength
    is_valid_pass, pass_msg = validate_password_strength(data['password'])
    if not is_valid_pass:
        return jsonify({'error': pass_msg}), 400

    # 3. Create Account
    admin_id, msg = create_admin_account_service(
        data['name'], data['email'], data['username'], data['password']
    )
    
    if admin_id:
        return jsonify({'message': 'Admin created', 'admin_id': admin_id}), 201
        
    return jsonify({'error': msg}), 400

@admin_bp.route('/reset-admin-password', methods=['POST'])
@require_admin
def reset_admin_pw():
    data = request.get_json() or {}
    if 'admin_id' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing admin_id or new_password'}), 400
        
    is_valid, msg = validate_password_strength(data['new_password'])
    if not is_valid: return jsonify({'error': msg}), 400
        
    success, message = reset_admin_password_service(data['admin_id'], data['new_password'])
    return jsonify({'message' if success else 'error': message}), 200 if success else 400

@admin_bp.route('/<int:admin_id>', methods=['DELETE'])
@require_admin
@validate_id_params('admin_id')
def delete_admin(admin_id):
    # Pass current admin ID if available in request.admin_id, else -1
    current_id = getattr(request, 'admin_id', -1)
    success, message = delete_admin_service(admin_id, current_id) 
    return jsonify({'message' if success else 'error': message}), 200 if success else 400