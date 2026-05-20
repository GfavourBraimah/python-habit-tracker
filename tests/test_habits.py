import pytest
from datetime import datetime, timedelta
from app.models import Habit
from app.analytics import calculate_streak, filter_by_periodicity, get_longest_streak_all
from app.database import save_habit, delete_habit, edit_habit_name, get_db_connection

# --- 1. CORE LOGIC TESTS ---

def test_habit_initialization():
    """Verify that a new habit is set up correctly."""
    h = Habit("Gym", "daily")
    assert h.name == "Gym"
    assert h.periodicity == "daily"
    assert len(h.completions) == 0

def test_complete_task():
    """Verify that clicking 'complete' adds a timestamp."""
    h = Habit("Read", "daily")
    h.complete_task()
    assert len(h.completions) == 1
    assert isinstance(h.completions[0], datetime)

# --- 2. ANALYTICS (FP) TESTS ---

def test_streak_calculation():
    """Verify the logic for a 2-day streak."""
    h = Habit("Water", "daily")
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    h.completions = [today, yesterday]
    streak = calculate_streak(h.completions, "daily")
    assert streak == 2

def test_analytics_filter():
    """Verify the FP filter function works."""
    h1 = Habit("Code", "daily")
    h2 = Habit("Wash Car", "weekly")
    
    filtered = filter_by_periodicity([h1, h2], "weekly")
    assert len(filtered) == 1
    assert filtered[0].name == "Wash Car"

def test_analytics_longest_streak_all():
    """Verify it finds the highest streak across multiple habits."""
    h1 = Habit("Run", "daily")
    h2 = Habit("Stretch", "daily")
    
    # Give h1 a streak of 2, and h2 a streak of 1
    h1.completions = [datetime.now(), datetime.now() - timedelta(days=1)]
    h2.completions = [datetime.now()]
    
    longest = get_longest_streak_all([h1, h2])
    assert longest == 2

# --- 3. DATABASE (CRUD) TESTS ---

def test_edit_and_delete_database():
    """Verify that we can save, edit, and delete a habit in SQLite."""
    test_name = "TestDeleteHabit"
    renamed = "RenamedHabit"
    
    # 1. Create & Save
    h = Habit(test_name, "daily")
    save_habit(h)
    
    # 2. Edit
    edit_habit_name(test_name, renamed)
    
    # 3. Delete
    delete_habit(renamed)
    
    # 4. Verify it is actually gone from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE name = ?", (renamed,))
    result = cursor.fetchone()
    conn.close()
    
    assert result is None  # Ensures the database returned nothing