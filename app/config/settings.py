import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ==========================================
    # ENVIRONMENT & DEBUG
    # ==========================================
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = ENV == 'development'
    TESTING = False
    
    # ==========================================
    # SECRET KEYS (CRITICAL - MUST BE SET)
    # ==========================================
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # Validate secrets are set
    if not SECRET_KEY:
        if DEBUG:
            print("WARNING: FLASK_SECRET_KEY not set! Using insecure default.")
            SECRET_KEY = 'dev-secret-key-CHANGE-IN-PRODUCTION'
        else:
            raise ValueError("FLASK_SECRET_KEY must be set in production!")
    
    if not JWT_SECRET_KEY:
        if DEBUG:
            print("WARNING: JWT_SECRET_KEY not set! Using insecure default.")
            JWT_SECRET_KEY = 'dev-jwt-secret-CHANGE-IN-PRODUCTION'
        else:
            raise ValueError("JWT_SECRET_KEY must be set in production!")
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour default
    JWT_ALGORITHM = 'HS256'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # ==========================================
    # DATABASE SETTINGS
    # ==========================================
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'campus_nav'),
        'charset': 'utf8mb4',
        'autocommit': False,
        'pool_size': int(os.getenv('DB_POOL_SIZE', 5)),
        'pool_name': 'campusnav_pool'
    }
    
    # Validate database password in production
    if not DEBUG and not DB_CONFIG['password']:
        raise ValueError("DB_PASSWORD must be set in production!")
    
    # ==========================================
    # FILE UPLOADS
    # ==========================================
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB for entire request
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}
    
    # ==========================================
    # SECURITY SETTINGS
    # ==========================================
    # Password Requirements
    MIN_PASSWORD_LENGTH = 8
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    
    # Session Security
    SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # HTTPS/Security Headers
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'False').lower() == 'true'
    
    # CORS
    CLIENT_URL = os.getenv('CLIENT_URL', 'http://localhost:5173')
    # Support multiple origins (comma-separated)
    CORS_ORIGINS = [url.strip() for url in CLIENT_URL.split(',')]
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per day;50 per hour')
    
    # ==========================================
    # LOGGING
    # ==========================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO' if not DEBUG else 'DEBUG')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/api.log')
    
    # ==========================================
    # API SETTINGS
    # ==========================================
    API_TITLE = 'CampusNav API'
    API_VERSION = '1.0.0'
    
    @staticmethod
    def get_safe_db_config():
        """Return DB config with password masked for logging"""
        safe_config = Config.DB_CONFIG.copy()
        if safe_config.get('password'):
            safe_config['password'] = '***HIDDEN***'
        return safe_config
    
    @staticmethod
    def validate():
        """Validate all critical configuration"""
        errors = []
        
        if not Config.SECRET_KEY or Config.SECRET_KEY.startswith('dev-'):
            if not Config.DEBUG:
                errors.append("Production SECRET_KEY must be set and not use dev default")
        
        if not Config.JWT_SECRET_KEY or Config.JWT_SECRET_KEY.startswith('dev-'):
            if not Config.DEBUG:
                errors.append("Production JWT_SECRET_KEY must be set and not use dev default")
        
        if not Config.DB_CONFIG.get('password') and not Config.DEBUG:
            errors.append("Database password must be set in production")
        
        if len(Config.SECRET_KEY) < 32:
            errors.append("SECRET_KEY should be at least 32 characters long")
        
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True