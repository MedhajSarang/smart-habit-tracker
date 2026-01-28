from database.db_connection import get_db_connection
from utils.security import make_hash, check_hash
import streamlit as st

def create_user(username, password):
    """
    Registers a new user in the Supabase database.
    Returns "Success" or an error message.
    """
    supabase = get_db_connection()
    
    # 1. Hash the password immediately
    hashed_pw = make_hash(password)
    
    # 2. Prepare the data
    user_data = {
        "username": username,
        "password_hash": hashed_pw
    }
    
    try:
        # 3. Send to Supabase
        response = supabase.table("users").insert(user_data).execute()
        return "Success"
    except Exception as e:
        # This usually happens if the username already exists (because we set UNIQUE)
        return f"Error: {e}"

def verify_login(username, password):
    """
    Checks if username exists and password matches.
    Returns the user_id if successful, else None.
    """
    supabase = get_db_connection()
    
    # 1. Find the user by username
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()

        # Check if user exists (list is not empty)
        if len(response.data) > 0:
            user_data = response.data[0]
            stored_hash = user_data["password_hash"]

            # 2. Check the password against the hash
            if check_hash(password, stored_hash):
                return user_data["user_id"] # Login Success!
            else:
                return None # Wrong Password
        else:
            return None # User not found
            
    except Exception as e:
        print(f"Login Error: {e}")
        return None