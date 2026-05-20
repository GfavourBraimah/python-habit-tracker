from datetime import datetime

class Habit:
    """
    The Blueprint for a Habit object.
    
    This class handles the core data for a habit: its name, 
    how often it happens, when it started, and a log of every 
    time the user actually did it.
    """

    def __init__(self, name, periodicity, created_at=None):
        """
        This is the 'Constructor'. It runs the moment you 
        create a new habit (like 'Habit("Gym", "daily")').
        """
        self.name = name
        self.periodicity = periodicity  # Should be 'daily' or 'weekly'
        
        # If we don't provide a date, use 'now'. 
        # This is useful for when we load old habits from the DB later.
        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at
            
        # This list will store 'datetime' objects for every completion
        self.completions = []

    def complete_task(self):
        """
        The 'Check-off' method. 
        Adds the current date and time to the log.
        """
        self.completions.append(datetime.now())

    def __str__(self):
        """
        This just tells Python how to 'print' the object 
        so it looks nice in the terminal.
        """
        return f"Habit: {self.name} ({self.periodicity})"