import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask.json.provider import DefaultJSONProvider
from datetime import timedelta, date, datetime
from werkzeug.middleware.proxy_fix import ProxyFix

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.settings import Config
from app.database.connection import init_db_pool

# Import Blueprints
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.semester import semester_bp
from app.routes.declaration import declaration_bp
from app.routes.uploads import uploads_bp
from app.routes.rooms import rooms_bp

# CUSTOM JSON PROVIDER
class CustomJSONProvider(DefaultJSONProvider):
    """
    Handles serialization of database time/date objects to JSON strings
    """
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

# APPLICATION FACTORY
def create_app(config_class=Config):
    """Create and configure the Flask application"""
    
    # Validate configuration before starting
    try:
        config_class.validate()
    except ValueError as e:
        print(f"CONFIGURATION ERROR:\n{e}")
        sys.exit(1)
    
    # Initialize Flask app
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)  
    app.json = CustomJSONProvider(app)
    app.config.from_object(config_class)
    
    # SECURITY HEADERS (Production Only)
    if not app.debug:
        try:
            from flask_talisman import Talisman
            Talisman(
                app,
                force_https=config_class.FORCE_HTTPS,
                strict_transport_security=True,
                strict_transport_security_max_age=31536000,
                content_security_policy={
                    'default-src': "'self'",
                    'img-src': '*',
                    'script-src': "'self' 'unsafe-inline'",
                    'style-src': "'self' 'unsafe-inline'"
                },
                content_security_policy_nonce_in=['script-src'],
                feature_policy={
                    'geolocation': "'none'",
                }
            )
            print("✓ Security headers enabled (Talisman)")
        except ImportError:
            print("⚠ Warning: flask-talisman not installed. Security headers disabled.")
            print("  Install with: pip install flask-talisman")
    
    # CORS CONFIG
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            # FIX: Added "X-API-Key" to allow_headers
            "allow_headers": ["Content-Type", "Authorization", "X-API-Key"],
            "expose_headers": ["Content-Type", "Authorization", "X-API-Key"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # RATE LIMITING
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=config_class.RATELIMIT_STORAGE_URL,
        default_limits=[config_class.RATELIMIT_DEFAULT] if config_class.RATELIMIT_ENABLED else [],
        headers_enabled=True
    )
    
    # LOGGING CONFIGURATION
    if not app.debug:
        log_dir = os.path.dirname(config_class.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = RotatingFileHandler(
            config_class.LOG_FILE,
            maxBytes=10485760,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CampusNav API startup')
    
    # DATABASE INITIALIZATION
    try:
        init_db_pool()
        print("✓ Database pool initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        if not app.debug:
            sys.exit(1)
    
    # REQUEST LOGGING & SECURITY
    @app.before_request
    def log_request_info():
        if app.debug:
            app.logger.debug(f'{request.method} {request.path}')
        if app.debug and request.remote_addr != '127.0.0.1':
            app.logger.warning(f"External request in DEBUG mode from {request.remote_addr}")
    
    @app.after_request
    def after_request(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # BLUEPRINT REGISTRATION
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(semester_bp, url_prefix='/api/semesters')
    app.register_blueprint(declaration_bp, url_prefix='/api/declarations')
    app.register_blueprint(uploads_bp, url_prefix='/api/upload')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    
	# HEALTH CHECK ENDPOINT
    @app.route('/api/health', methods=['GET'])
    def health():
        from app.database.connection import create_connection 
        
        db_status = 'disconnected'
        try:
            conn = create_connection() # Using the correct function from connection.py
            if conn: 
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                conn.close()
                db_status = 'connected'
        except Exception as e:
            app.logger.error(f"Health check DB error: {e}")
        
        return jsonify({
            'status': 'healthy' if db_status == 'connected' else 'degraded',
            'server': Config.API_TITLE,
            'version': Config.API_VERSION,
            'database': db_status,
            'environment': 'development' if app.debug else 'production'
        })
    
    # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(413)
    def request_entity_too_large(e):
        return jsonify({
            'error': 'File too large',
            'message': f'Maximum file size is {config_class.MAX_FILE_SIZE / 1024 / 1024}MB'
        }), 413
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f'Server Error: {e}', exc_info=True)
        if app.debug:
            return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
        else:
            return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
    return app

# APPLICATION ENTRY POINT
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 CAMPUSNAV API STARTING")
    print("="*50)
    print(f"Environment: {'DEVELOPMENT' if Config.DEBUG else 'PRODUCTION'}")
    print(f"Client URLs: {', '.join(Config.CORS_ORIGINS)}")
    print(f"Database: {Config.DB_CONFIG['host']}/{Config.DB_CONFIG['database']}")
    print(f"Rate Limiting: {'Enabled' if Config.RATELIMIT_ENABLED else 'Disabled'}")
    print(f"HTTPS Enforcement: {'Yes' if Config.FORCE_HTTPS else 'No'}")
    print("="*50 + "\n")
    
    if Config.DEBUG:
        print("⚠️  WARNING: Running in DEBUG mode")
        print("   - Do NOT use in production")
        print("   - Detailed errors exposed")
        print("   - Auto-reload enabled\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG,
        use_reloader=Config.DEBUG,
        threaded=True
    )
