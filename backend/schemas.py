from pydantic import BaseModel
from typing import Optional
from datetime import date

# 1. The "Base" model (shared fields)
class HabitBase(BaseModel):
    name: str
    category: str
    frequency: str

# 2. The "Create" model (what we need to create a habit)
class HabitCreate(HabitBase):
    user_id: str

# 3. The "Response" model (what we send back to the user)
class Habit(HabitBase):
    habit_id: int
    created_at: str
    is_active: bool

    class Config:
        # This tells Pydantic to treat database rows like dictionaries
        from_attributes = True