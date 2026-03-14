from flask import Blueprint, jsonify, request
from app.services.semester_service import (
    get_semester_by_id, activate_semester_service, get_all_semesters, 
    get_active_semester, get_semester_statistics, create_semester_service, 
    deactivate_semester_service, update_semester_service, delete_semester_service
)
from app.utils.decorators import require_api_key, require_admin, require_jwt_token
from app.utils.validators import validate_id_params

semester_bp = Blueprint('semester', __name__)

# --- READ ROUTES (Changed to JWT for Faculty Access) ---

@semester_bp.route('/', methods=['GET'], strict_slashes=False)
@require_jwt_token  # <--- CHANGED FROM require_api_key
def get_semesters():
    semesters = get_all_semesters()
    return jsonify(semesters)

@semester_bp.route('/active', methods=['GET'])
@require_jwt_token  # <--- CHANGED FROM require_api_key
def get_current_active_semester():
    semester = get_active_semester()
    if semester:
        return jsonify(semester)
    return jsonify({'message': 'No active semester'}), 404

@semester_bp.route('/<int:semester_id>', methods=['GET'])
@require_jwt_token  # <--- CHANGED FROM require_api_key
@validate_id_params('semester_id')
def get_semester(semester_id):
    semester = get_semester_by_id(semester_id)
    if semester:
        return jsonify(semester)
    return jsonify({'error': 'Semester not found'}), 404

@semester_bp.route('/<int:semester_id>/statistics', methods=['GET'])
@require_jwt_token  # <--- CHANGED FROM require_api_key
@validate_id_params('semester_id')
def get_semester_stats(semester_id):
    stats = get_semester_statistics(semester_id)
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'Semester not found'}), 404

# --- ADMIN WRITE ROUTES (Keep as require_admin) ---

@semester_bp.route('/<int:semester_id>/activate', methods=['POST'])
@require_admin
@validate_id_params('semester_id')
def activate_sem(semester_id):
    success, message, affected = activate_semester_service(semester_id)
    if success:
        return jsonify({'message': message, 'affected_declarations': affected}), 200
    return jsonify({'error': message}), 400

@semester_bp.route('/', methods=['POST'], strict_slashes=False)
@require_admin
def create_new_semester():
    data = request.get_json() or {}
    required = ('semester_name', 'semester_code', 'academic_year', 'start_date', 'end_date')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Unpack tuple: (id, error_message)
    semester_id, error = create_semester_service(
        data['semester_name'], data['semester_code'],
        data['academic_year'], data['start_date'], data['end_date']
    )
    
    # Success Case
    if semester_id:
        return jsonify({'message': 'Semester created', 'semester_id': semester_id}), 201
    
    # Error Handling
    if error and ("exists" in error or "Duplicate" in error):
        # Return 409 Conflict if duplicate
        return jsonify({'error': error}), 409
        
    # Default Server Error
    return jsonify({'error': error or 'Failed to create semester'}), 500

@semester_bp.route('/<int:semester_id>/deactivate', methods=['POST'])
@require_admin
@validate_id_params('semester_id')
def deactivate_sem(semester_id):
    success, message = deactivate_semester_service(semester_id)
    status = 200 if success else 400
    return jsonify({'message' if success else 'error': message}), status

@semester_bp.route('/<int:semester_id>', methods=['PUT'])
@require_admin
@validate_id_params('semester_id')
def update_sem(semester_id):
    data = request.get_json() or {}
    success, message = update_semester_service(
        semester_id, 
        data.get('semester_name'), data.get('semester_code'),
        data.get('academic_year'), data.get('start_date'), data.get('end_date')
    )
    status = 200 if success else 400
    return jsonify({'message' if success else 'error': message}), status

@semester_bp.route('/<int:semester_id>', methods=['DELETE'])
@require_admin
@validate_id_params('semester_id')
def delete_sem(semester_id):
    success, message = delete_semester_service(semester_id)
    status = 200 if success else 400
    return jsonify({'message' if success else 'error': message}), status