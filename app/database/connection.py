import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv

load_dotenv()

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'campus_nav')
}

# --- CONNECTION POOL SETUP ---
db_pool = None

def init_db_pool():
    global db_pool
    try:
        db_pool = pooling.MySQLConnectionPool(
            pool_name="campus_nav_pool",
            pool_size=20,
            pool_reset_session=True,
            **DB_CONFIG
        )
        print("✅ Database Connection Pool Initialized")
    except Error as e:
        print(f"❌ Critical Error: Could not initialize DB Pool. {e}")
        db_pool = None

# Initialize on module load
init_db_pool()

def create_connection():
    """
    Get a connection from the pool.
    """
    global db_pool
    if db_pool is None:
        init_db_pool()
        
    try:
        if db_pool:
            conn = db_pool.get_connection()
            if conn.is_connected():
                return conn
    except Error as e:
        print(f"Error getting connection from pool: {e}")
    
    return None