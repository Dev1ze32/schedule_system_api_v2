from flask import Blueprint, jsonify, request
from app.utils.decorators import require_jwt_token
from app.models.room import get_all_rooms, insert_room, delete_room_from_db

rooms_bp = Blueprint('rooms', __name__)

# --- GET ALL ROOMS (NO FILTER) ---
@rooms_bp.route('/all', methods=['GET'], strict_slashes=False)
@require_jwt_token
def get_all_rooms_route():
    """
    Returns a list of ALL rooms, regardless of building.
    Useful for 'Show All' options in dropdowns.
    """
    rooms = get_all_rooms()
    return jsonify(rooms)

# --- CREATE ROOM ---
@rooms_bp.route('/', methods=['POST'], strict_slashes=False)
@require_jwt_token
def add_room():
    data = request.get_json() or {}
    r_name = data.get('room_name') or data.get('room_number')
    
    if not r_name: return jsonify({'error': 'Missing room_name'}), 400
    
    room_id = insert_room(
        data.get('building', 'Main Building'), 
        r_name, 
        data.get('floor', 1)
    )
    
    if room_id: return jsonify({'message': 'Room created', 'room_id': room_id}), 201
    return jsonify({'error': 'Failed to create room'}), 500

@rooms_bp.route('/<int:room_id>', methods=['DELETE'])
@require_jwt_token
def delete_room(room_id):
    # Call a function to delete from DB
    success = delete_room_from_db(room_id) 
    if success:
        return jsonify({'message': 'Room deleted'}), 200
    return jsonify({'error': 'Room not found'}), 404