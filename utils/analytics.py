import pandas as pd
from database.db_connection import get_db_connection

def get_habit_stats(user_id):
    """
    Fetches raw data and transforms it into a clean DataFrame for plotting.
    """
    supabase = get_db_connection()
    
    # 1. Fetch all habits
    habits = supabase.table("habits").select("*").eq("user_id", user_id).execute().data
    
    # 2. Fetch all logs (history)
    # We need to join this with habits to get the names
    logs = supabase.table("tracker_logs").select("*").execute().data
    
    # --- PANDAS MAGIC STARTS HERE ---
    
    if not habits or not logs:
        return pd.DataFrame() # Return empty if no data
    
    # Convert to DataFrames
    df_habits = pd.DataFrame(habits)
    df_logs = pd.DataFrame(logs)
    
    # 3. Merge tables (SQL Join equivalent)
    # We want to keep all habits, even if they have 0 logs
    df_merged = pd.merge(df_habits, df_logs, on="habit_id", how="left")
    
    # 4. Calculate Completion Counts
    # Group by Habit Name and count the number of 'log_id's (completions)
    summary = df_merged.groupby("name").agg(
        count=("log_id", "count"),
        category=("category", "first") # Keep the category info
    ).reset_index()
    
    return summary

def get_day_of_week_stats(user_id):
    """
    Calculates which days of the week are most productive.
    """
    supabase = get_db_connection()
    
    # 1. Fetch raw logs
    logs = supabase.table("tracker_logs").select("*").execute().data
    habits = supabase.table("habits").select("*").eq("user_id", user_id).execute().data
    
    if not logs or not habits:
        return pd.DataFrame()

    # 2. Convert to DataFrame
    df_logs = pd.DataFrame(logs)
    df_habits = pd.DataFrame(habits)
    
    # 3. Merge to get Habit Names
    df_merged = pd.merge(df_logs, df_habits, on="habit_id")
    
    # 4. Extract Day Name (Mon, Tue, Wed...)
    # This requires converting the 'date' string to a datetime object first
    df_merged["date"] = pd.to_datetime(df_merged["date"])
    df_merged["day_name"] = df_merged["date"].dt.day_name()
    
    # 5. Order the days correctly (otherwise they appear alphabetically)
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_merged["day_name"] = pd.Categorical(df_merged["day_name"], categories=days_order, ordered=True)
    
    # 6. Group by Habit and Day
    heatmap_data = df_merged.groupby(["name", "day_name"]).size().reset_index(name="count")
    
    return heatmap_data