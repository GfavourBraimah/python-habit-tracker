import sqlite3
from .models import Habit
from datetime import datetime

def get_db_connection():
    """Creates a connection to the SQLite database file."""
    conn = sqlite3.connect('data/habits.db')
    return conn

def initialize_db():
    """Creates the tables if they don't exist yet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table 1: Stores the habit definition
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            created_at TEXT
        )
    ''')
    
    # Table 2: Stores every single time a habit was completed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            habit_name TEXT,
            timestamp TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits (name)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_habit(habit):
    """Takes a Habit object and saves it to the DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert habit info (or ignore if it's already there)
    cursor.execute(
        "INSERT OR IGNORE INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)",
        (habit.name, habit.periodicity, habit.created_at.isoformat())
    )
    
    # Clear and re-insert completions to keep it simple for now
    cursor.execute("DELETE FROM completions WHERE habit_name = ?", (habit.name,))
    for timestamp in habit.completions:
        cursor.execute(
            "INSERT INTO completions (habit_name, timestamp) VALUES (?, ?)",
            (habit.name, timestamp.isoformat())
        )
    
    conn.commit()
    conn.close()

def delete_habit(name):
    """Removes a habit and all its completions from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the logs first (Foreign Key constraint best practice)
    cursor.execute("DELETE FROM completions WHERE habit_name = ?", (name,))
    # Delete the actual habit
    cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
    
    conn.commit()
    conn.close()

def edit_habit_name(old_name, new_name):
    """Renames an existing habit in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update the logs to point to the new name
    cursor.execute("UPDATE completions SET habit_name = ? WHERE habit_name = ?", (new_name, old_name))
    # Update the habit definition
    cursor.execute("UPDATE habits SET name = ? WHERE name = ?", (new_name, old_name))
    
    conn.commit()
    conn.close()