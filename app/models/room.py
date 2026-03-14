from app.database.connection import create_connection as get_db_connection
from mysql.connector import Error

# --- READ OPERATIONS ---

def get_room_id(room_name):
    """Finds a room ID by its name (case-insensitive)."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT room_id FROM room WHERE LOWER(room_name) = LOWER(%s) LIMIT 1"
        cursor.execute(query, (room_name.strip(),))
        result = cursor.fetchone()
        return result['room_id'] if result else None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def room_exists(room_id):
    conn = get_db_connection() 
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM room WHERE room_id = %s", (room_id,))
        return cursor.fetchone() is not None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

def get_all_rooms():
    """
    Fetches EVERY room in the database.
    Ordered by Building Name, then Room Name.
    """
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM room ORDER BY building_name ASC, room_name ASC"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# --- WRITE OPERATIONS ---

def insert_room(building, room_name, floor):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO room (building_name, room_name, floor_number) VALUES (%s, %s, %s)", (building, room_name, floor))
        conn.commit()
        return cursor.lastrowid
    except Error: return None
    finally:
        if conn.is_connected(): cursor.close(); conn.close()


def delete_room_from_db(room_id):
    """Deletes a room by its ID and returns True if successful."""
    conn = get_db_connection()
    if not conn: 
        return False
    try:
        cursor = conn.cursor()
        # Check if the room exists first to provide an accurate response
        cursor.execute("DELETE FROM room WHERE room_id = %s", (room_id,))
        conn.commit()
        
        # rowcount tells us if a row was actually deleted
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting room: {e}")
        return False
    finally:
        if conn.is_connected(): 
            cursor.close()
            conn.close()