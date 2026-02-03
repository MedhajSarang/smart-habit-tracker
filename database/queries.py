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

def add_habit(user_id, name, category, frequency):
    """
    Adds a new habit to the database for a specific user.
    """
    supabase = get_db_connection()
    
    habit_data = {
        "user_id": user_id,
        "name": name,
        "category": category,
        "frequency": frequency
    }
    
    try:
        response = supabase.table("habits").insert(habit_data).execute()
        return "Success"
    except Exception as e:
        return f"Error: {e}"

# 1. Fetch all habits for the user
def get_user_habits(user_id, active_only=True):
    """
    Fetch habits. 
    If active_only=True, returns only currently active habits.
    If active_only=False, returns EVERYTHING (for history/management).
    """
    supabase = get_db_connection()
    try:
        query = supabase.table("habits").select("*").eq("user_id", user_id)
        
        if active_only:
            query = query.eq("is_active", True)
            
        response = query.execute()
        return response.data
    except Exception as e:
        return []

# 2. Check if a specific habit is done today (to keep the box checked)
def is_habit_done_today(habit_id, date):
    supabase = get_db_connection()
    try:
        # Check for a log entry for this habit on this date
        response = supabase.table("tracker_logs").select("*").eq("habit_id", habit_id).eq("date", date).execute()
        return len(response.data) > 0 # Returns True if data exists
    except Exception as e:
        return False

# 3. Toggle the habit (Check/Uncheck)
def toggle_habit(habit_id, date, done):
    supabase = get_db_connection()
    try:
        if done:
            # Insert a log
            supabase.table("tracker_logs").insert({"habit_id": habit_id, "date": str(date)}).execute()
        else:
            # Delete the log (Uncheck)
            supabase.table("tracker_logs").delete().eq("habit_id", habit_id).eq("date", str(date)).execute()
    except Exception as e:
        print(f"Error toggling habit: {e}")

def delete_habit(habit_id):
    """
    Deletes a habit and all associated logs (Cascading delete).
    """
    supabase = get_db_connection()
    try:
        # We only need to delete from 'habits'. 
        # Because we used 'ON DELETE CASCADE' in SQL, the logs will auto-delete.
        supabase.table("habits").delete().eq("habit_id", habit_id).execute()
        return "Success"
    except Exception as e:
        return f"Error: {e}"

def update_habit(habit_id, name, category, frequency):
    """
    Updates the details of an existing habit.
    """
    supabase = get_db_connection()
    try:
        supabase.table("habits").update({
            "name": name,
            "category": category,
            "frequency": frequency
        }).eq("habit_id", habit_id).execute()
        return "Success"
    except Exception as e:
        return f"Error: {e}"

def toggle_habit_status(habit_id, current_status):
    """
    Flips the habit from Active -> Inactive OR Inactive -> Active.
    """
    supabase = get_db_connection()
    new_status = not current_status # Flip the boolean
    
    try:
        supabase.table("habits").update({"is_active": new_status}).eq("habit_id", habit_id).execute()
        return "Success"
    except Exception as e:
        return f"Error: {e}"