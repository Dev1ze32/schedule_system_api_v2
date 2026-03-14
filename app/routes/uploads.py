from flask import Blueprint, request, jsonify, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.utils.decorators import require_jwt_token, require_api_key
from app.utils.file_parser import validate_file_extension
from app.services.upload_service import process_schedule_upload, validate_schedule_preview, generate_template_csv

uploads_bp = Blueprint('uploads', __name__)
limiter = Limiter(key_func=get_remote_address)

@uploads_bp.route('/schedule', methods=['POST'])
@require_jwt_token
@limiter.limit("30 per hour")
def upload_schedule():
    if 'file' not in request.files: return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    semester_id = request.form.get('semester_id')

    if not semester_id: return jsonify({'message': 'Semester ID is required'}), 400
    if file.filename == '': return jsonify({'message': 'No selected file'}), 400
    if not validate_file_extension(file.filename): return jsonify({'message': 'Invalid file type'}), 400

    # Call Service
    result, error_data = process_schedule_upload(file, semester_id, request.faculty_id)
    
    if error_data:
        # Return 206 if some rows failed but process finished, otherwise 400
        status_code = 400
        if 'summary' in error_data and error_data['summary']['successful'] > 0:
             status_code = 206 
        return jsonify(error_data), status_code

    # Return success (201 if fully clean, or 206 if partial which is handled in logic above)
    status_code = 201 if result['summary']['failed'] == 0 else 206
    return jsonify(result), status_code


@uploads_bp.route('/schedule/validate', methods=['POST'])
@require_jwt_token
def validate_schedule_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not validate_file_extension(file.filename):
        return jsonify({
            'error': 'Invalid file type',
            'message': 'Only CSV, XLSX, and XLS files are supported'
        }), 400
    
    result, error = validate_schedule_preview(file)
    
    if error:
        return jsonify({'error': 'Validation failed', 'message': error}), 400
        
    return jsonify(result), 200


@uploads_bp.route('/template', methods=['GET'], strict_slashes=False)
@require_jwt_token  # <--- CHANGED FROM require_api_key
def download_template():
    try:
        file_buffer = generate_template_csv()
        
        return send_file(
            file_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name='schedule_template.csv'
        )
    except Exception as e:
        return jsonify({'error': 'Failed to generate template', 'message': str(e)}), 500