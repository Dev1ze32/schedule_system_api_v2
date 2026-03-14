from app.models.admin import (
    insert_admin_profile, 
    insert_admin_login, 
    delete_admin_data, 
    update_admin_password_record,
    get_admin_by_username
)
from app.utils.security import hash_sha256

def create_admin_account_service(name, email, username, password):
    """
    Creates a new Admin account using SHA256 hashing.
    """
    # 1. Check duplicate username
    if get_admin_by_username(username):
        return None, "Username already exists"

    # 2. Create Profile
    admin_id = insert_admin_profile(name, email)
    if not admin_id:
        return None, "Failed to create profile (Email might be in use)"
    
    # 3. Hash Password (LEGACY: SHA256)
    hashed_pw = hash_sha256(password)
    
    # 4. Create Login
    login_id = insert_admin_login(admin_id, username, hashed_pw)
    
    if not login_id:
        delete_admin_data(admin_id)
        return None, "Failed to create login"
        
    return admin_id, "Admin account created successfully"

def delete_admin_service(target_admin_id, current_admin_id):
    if int(target_admin_id) == int(current_admin_id):
        return False, "You cannot delete your own account while logged in."
    return delete_admin_data(target_admin_id)

def reset_admin_password_service(admin_id, new_password):
    new_hash = hash_sha256(new_password)
    return update_admin_password_record(admin_id, new_hash)