from app.models import Habit
from app.database import initialize_db, save_habit, get_db_connection
from app.cli import main_menu
from datetime import datetime, timedelta
import random

def seed_data():
    """Generates 5 habits and 4 weeks of history as required."""
    initialize_db()
    

    predefined = [
        Habit("Gym", "daily"),
        Habit("Read", "daily"),
        Habit("Meditation", "daily"),
        Habit("Wash Car", "weekly"),
        Habit("Grocery Shop", "weekly")
    ]

    
    for habit in predefined:
    
        for i in range(28, 0, -1):
            if habit.periodicity == "daily":
               
                if random.random() > 0.1: 
                    completion_date = datetime.now() - timedelta(days=i)
                    habit.completions.append(completion_date)
            else:
               
                if i % 7 == 0:
                    completion_date = datetime.now() - timedelta(days=i)
                    habit.completions.append(completion_date)
        
        save_habit(habit)
    print("Database initialized with 4 weeks of test data.")

if __name__ == "__main__":

    seed_data()
    
   
    habits = [] 
    main_menu(habits)