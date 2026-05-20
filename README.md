# Habit Tracker CLI

A professional Python application for tracking and analyzing daily and weekly habits.

## 1. Description

This application allows users to create habits, check them off, and view analytics such as current and longest streaks. It uses Object-Oriented Programming (OOP) for the core logic and Functional Programming (FP) for the analytics module. Data is persisted using an SQLite database.

## 2. Requirements

- Python 3.7 or newer
- `questionary` (for the CLI menu)
- `pytest` (for running tests)

## 3. Installation

1. Navigate to the project root directory.
2. Install the necessary dependencies:

   ```bash
   pip install questionary pytest
   ```

## 4. How to Run

To start the application, run the following command in your terminal:

   ```
python main.py
   ```

## 5. Example Usage

Add a Habit: Choose "Add New Habit" and enter the name and periodicity (daily/weekly).

Check-off: Select "Check-off a Habit" to log a completion for today.

Analytics: Select "View Analytics" to see your longest streaks.

## 6. Running Tests

To verify the application logic, run the unit test suite:

```
python -m pytest
```
