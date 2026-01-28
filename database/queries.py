from database.db_connection import get_db_connection
from utils.security import make_hash
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