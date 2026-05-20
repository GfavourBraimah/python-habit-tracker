import questionary
from .models import Habit
from .database import save_habit, get_db_connection, delete_habit, edit_habit_name
from .analytics import calculate_streak, filter_by_periodicity, get_longest_streak_all

def view_analytics(habits):
    """Sub-menu for the Analytics Department."""
    choice = questionary.select(
        "Which analysis would you like to see?",
        choices=[
            "Show all current habits",
            "Show habits by periodicity",
            "Longest streak (Overall)",
            "Longest streak (Specific Habit)",
            "Back to Main Menu"
        ]
    ).ask()

    if choice == "Show all current habits":
        for h in habits:
            print(f"- {h.name} ({h.periodicity})")
    
    elif choice == "Show habits by periodicity":
        period = questionary.select("Choose period:", choices=["daily", "weekly"]).ask()
        filtered = filter_by_periodicity(habits, period)
        for h in filtered:
            print(f"- {h.name}")

    elif choice == "Longest streak (Overall)":
        longest = get_longest_streak_all(habits)
        print(f"The longest streak across all your habits is: {longest} days")

    elif choice == "Longest streak (Specific Habit)":
        names = [h.name for h in habits]
        if not names:
            print("No habits available to analyze.")
            return
        target = questionary.select("Select a habit:", choices=names).ask()
        # Find the habit object and calculate its streak
        for h in habits:
            if h.name == target:
                s = calculate_streak(h.completions, h.periodicity)
                print(f"The longest streak for {target} is: {s}")


def main_menu(habits):
    """The main loop for the user interface."""
    while True:
        print("\n--- Habit Tracker ---")
        print("1. View All Habits")
        print("2. Check-off a Habit")
        print("3. Add New Habit")
        print("4. Edit a Habit Name")  # NEW
        print("5. Delete a Habit")     # NEW
        print("6. View Analytics")
        print("7. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            if not habits:
                print("No habits currently tracked.")
            for h in habits:
                streak = calculate_streak(h.completions, h.periodicity)
                print(f"[{h.periodicity}] {h.name} - Current Streak: {streak}")
        
        elif choice == '2':
            name = input("Enter habit name to check off: ")
            found = False
            for h in habits:
                if h.name.lower() == name.lower():
                    h.complete_task()
                    save_habit(h)
                    print(f"Task '{h.name}' marked as complete!")
                    found = True
                    break
            if not found:
                print(f"Could not find habit: {name}")
                    
        elif choice == '3':
            name = input("Enter new habit name: ")
            period = input("Enter periodicity (daily/weekly): ")
            new_h = Habit(name, period)
            habits.append(new_h)
            save_habit(new_h)
            print(f"Habit '{name}' created!")

        elif choice == '4':
            old_name = input("Enter the current name of the habit to edit: ")
            new_name = input("Enter the new name: ")
            # Update the database
            edit_habit_name(old_name, new_name)
            # Update the object in memory
            for h in habits:
                if h.name.lower() == old_name.lower():
                    h.name = new_name
            print(f"Habit renamed to '{new_name}'!")

        elif choice == '5':
            name = input("Enter the name of the habit to delete: ")
            # Delete from database
            delete_habit(name)
            # Remove from memory safely
            habit_to_remove = None
            for h in habits:
                if h.name.lower() == name.lower():
                    habit_to_remove = h
                    break
            if habit_to_remove:
                habits.remove(habit_to_remove)
                print(f"Habit '{name}' deleted!")
            else:
                print(f"Could not find habit: {name}")
            
        elif choice == '6':
            view_analytics(habits)
            
        elif choice == '7':
            break