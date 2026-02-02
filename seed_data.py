import random
from datetime import date, timedelta
from database.db_connection import get_db_connection

# 1. Connect to DB
supabase = get_db_connection()

def seed_history():
    print("🌱 Starting Data Seeding...")
    
    # 2. Get your User ID (We'll just pick the first user found for simplicity)
    users = supabase.table("users").select("user_id").execute()
    if not users.data:
        print("❌ No users found! Sign up first.")
        return
    
    user_id = users.data[0]['user_id']
    
    # 3. Get that user's habits
    habits = supabase.table("habits").select("habit_id", "name").eq("user_id", user_id).execute()
    
    if not habits.data:
        print("❌ No habits found! Add some habits in the app first.")
        return

    print(f"Found {len(habits.data)} habits. Generating history...")

    # 4. Loop back 30 days
    today = date.today()
    logs_to_insert = []
    
    for i in range(30):
        # Calculate the date (Today - i days)
        current_date = today - timedelta(days=i)
        
        for habit in habits.data:
            # FLIP A COIN: 70% chance of completing the habit
            if random.random() < 0.7: 
                log = {
                    "habit_id": habit['habit_id'],
                    "date": str(current_date),
                    "status": "completed"
                }
                logs_to_insert.append(log)

    # 5. Bulk Insert (Much faster than one by one)
    if logs_to_insert:
        try:
            supabase.table("tracker_logs").insert(logs_to_insert).execute()
            print(f"✅ Successfully inserted {len(logs_to_insert)} log entries!")
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
    else:
        print("⚠️ No data generated.")

# Run the function
if __name__ == "__main__":
    seed_history()