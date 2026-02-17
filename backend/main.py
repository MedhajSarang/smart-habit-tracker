from fastapi import FastAPI
from database.db_connection import get_db_connection
from typing import List
from backend import schemas

# 1. Initialize the App
app = FastAPI(
    title="Smart Habit Tracker API",
    description="The backend brain for our habit tracker.",
    version="1.0.0"
)

# 2. Define a "Route" (Endpoint)
# When someone visits the root URL ("/"), run this function.
@app.get("/")
def health_check():
    """
    A simple health check to verify the server is running.
    """
    return {"status": "active", "message": "Backend is online! 🚀"}

# 3. A Mock Data Endpoint
@app.get("/api/v1/test-habits")
def get_test_habits():
    """
    Returns some fake data to prove we can send JSON lists.
    """
    return [
        {"id": 1, "name": "Learn FastAPI", "status": "In Progress"},
        {"id": 2, "name": "Build a Portfolio", "status": "Crushing It"}
    ]

@app.get("/api/v1/habits/{user_id}", response_model=List[schemas.Habit])
def get_user_habits(user_id: str):
    """
    Fetches real habits for a specific user from Supabase.
    Now validated by Pydantic! If the DB returns weird data, this will throw an error.
    """
    supabase = get_db_connection()

    # Query the database
    response = supabase.table("habits").select("*").eq("user_id", user_id).execute()

    return response.data
