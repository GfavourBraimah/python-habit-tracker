from app.models import Habit
from app.database import initialize_db, save_habit, get_db_connection
from app.cli import main_menu
from datetime import datetime, timedelta
import random

def seed_data():
    """Generates 5 habits and 4 weeks of history as required."""
    initialize_db()
    
    # 1. Define the 5 predefined habits
    predefined = [
        Habit("Gym", "daily"),
        Habit("Read", "daily"),
        Habit("Meditation", "daily"),
        Habit("Wash Car", "weekly"),
        Habit("Grocery Shop", "weekly")
    ]

    # 2. Add 4 weeks of 'fake' history for each
    for habit in predefined:
        # Loop back 28 days
        for i in range(28, 0, -1):
            if habit.periodicity == "daily":
                # Randomly complete most days to simulate a real user
                if random.random() > 0.1: 
                    completion_date = datetime.now() - timedelta(days=i)
                    habit.completions.append(completion_date)
            else:
                # For weekly, complete once every 7 days
                if i % 7 == 0:
                    completion_date = datetime.now() - timedelta(days=i)
                    habit.completions.append(completion_date)
        
        save_habit(habit)
    print("Database initialized with 4 weeks of test data.")

if __name__ == "__main__":
    # Run the seeder once to setup the project
    seed_data()
    
    # Normally, you would load habits from the DB here
    # For now, we'll just start the menu
    habits = [] # Logic to load from DB goes here next
    main_menu(habits)