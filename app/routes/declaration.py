from flask import Blueprint, jsonify, request
from bleach import clean
from datetime import datetime
from app.utils.decorators import require_jwt_token
from app.utils.validators import validate_id_params
from app.services.declaration_service import (
    insert_declaration_service, update_declaration_service, delete_declaration_service
)
from app.models.room import get_room_id
from app.models.declaration import get_faculty_schedule_data

declaration_bp = Blueprint('declaration', __name__)

# --- FIX: Added strict_slashes=False to prevent 308 Redirect ---
@declaration_bp.route('/', methods=['POST'], strict_slashes=False)
@require_jwt_token
def create_declaration():
    data = request.get_json() or {}
    
    required = ('room', 'semester_id', 'subject_code', 'class_section', 'day', 'start_time', 'end_time')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Sanitize input
    subject_code = clean(data['subject_code'].strip())
    
    # Get Room ID
    room_id = get_room_id(data['room'].strip())
    if not room_id:
        return jsonify({'error': f"Room '{data['room']}' not found"}), 404
        
    dec_id, error_msg = insert_declaration_service(
        faculty_id=request.faculty_id,
        room_id=room_id,
        semester_id=data['semester_id'],
        subject_code=subject_code,
        class_section=data['class_section'],
        day=data['day'],
        start=data['start_time'],
        end=data['end_time']
    )
    
    if error_msg:
        code = 409 if "Conflict" in error_msg else 400
        return jsonify({'error': error_msg}), code
        
    return jsonify({'message': 'Declaration created', 'declaration_id': dec_id}), 201

@declaration_bp.route('/me', methods=['GET'])
@require_jwt_token
def get_my_declarations():
    semester_id = request.args.get('semester_id', type=int)
    # Note: request.faculty_id comes from the @require_jwt_token decorator
    schedule = get_faculty_schedule_data(request.faculty_id, semester_id)
    return jsonify(schedule)

@declaration_bp.route('/<int:declaration_id>', methods=['PUT'])
@require_jwt_token
@validate_id_params('declaration_id')
def update_decl(declaration_id):
    data = request.get_json() or {}
    
    room_id = None
    if 'room' in data:
        room_id = get_room_id(data['room'])
        if not room_id:
            return jsonify({'error': f"Room '{data['room']}' not found"}), 404
    
    success, message = update_declaration_service(
        declaration_id=declaration_id,
        faculty_id=request.faculty_id,
        room_id=room_id,
        subject_code=data.get('subject_code'),
        class_section=data.get('class_section'),
        day=data.get('day'),
        start=data.get('start_time'),
        end=data.get('end_time')
    )
    
    if success:
        return jsonify({'message': message}), 200
    
    status_code = 409 if "Conflict" in message else 400
    return jsonify({'error': message}), status_code

@declaration_bp.route('/<int:declaration_id>', methods=['DELETE'])
@require_jwt_token
@validate_id_params('declaration_id')
def delete_decl(declaration_id):
    success, message = delete_declaration_service(declaration_id, request.faculty_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400