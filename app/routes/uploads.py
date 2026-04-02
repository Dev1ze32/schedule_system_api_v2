from flask import Blueprint, request, jsonify, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.utils.decorators import require_jwt_token
from app.services.upload_service import process_schedule_upload, generate_template_csv

uploads_bp = Blueprint('uploads', __name__)
limiter = Limiter(key_func=get_remote_address)

@uploads_bp.route('/schedule', methods=['POST'])
@require_jwt_token
@limiter.limit("30 per hour")
def upload_schedule():
    try:
        print("=== ROUTE upload_schedule CALLED ===", flush=True)

        if 'file' not in request.files: 
            return jsonify({'message': 'No file part'}), 400
            
        file = request.files['file']
        semester_id = request.form.get('semester_id')
        
        if not semester_id: 
            return jsonify({'message': 'Semester ID is required'}), 400
            
        print(f"=== Calling process_schedule_upload with file: {file.filename} ===", flush=True)

        # Call Service
        result, error_data = process_schedule_upload(file, semester_id, request.faculty_id)

        # --- THE FIX: We must return the results to the frontend ---
        
        # If the service returned an error dictionary
        if error_data:
            return jsonify(error_data), 400
            
        # If the service was successful
        return jsonify(result), 200

    except Exception as e:
        # Catch any unexpected crashes and return them as JSON
        print(f"Route crash: {str(e)}", flush=True)
        return jsonify({
            'error': 'Internal Server Error', 
            'message': str(e)
        }), 500

@uploads_bp.route('/template', methods=['GET'], strict_slashes=False)
@require_jwt_token  
def download_template():
    try:
        print("=== ROUTE download_template CALLED ===", flush=True)
        
        file_buffer = generate_template_csv()
        
        return send_file(
            file_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name='schedule_template.csv'
        )
    except Exception as e:
        print(f"TEMPLATE CRASH: {str(e)}", flush=True)
        return jsonify({'error': 'Failed to generate template', 'message': str(e)}), 500