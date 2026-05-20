from datetime import datetime, timedelta

def get_all_habits(habits_list):
    """Returns all habits (simple pass-through for now)."""
    return habits_list

def filter_by_periodicity(habits_list, periodicity):
    """
    FP technique: Uses a list comprehension to filter data.
    Equivalent to a SQL 'WHERE' clause.
    """
    return [h for h in habits_list if h.periodicity == periodicity]

def calculate_streak(completions, periodicity):
    """
    The heart of the app. Calculates the current consecutive streak.
    """
    if not completions:
        return 0

  
    sorted_dates = sorted(list(set([c.date() for c in completions])), reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
 
    limit = 1 if periodicity == 'daily' else 7

    for date in sorted_dates:
        diff = (current_date - date).days
        
        if diff <= limit:
            streak += 1
            current_date = date
        else:
            break 
            
    return streak

def get_longest_streak_all(habits_list):
    """Returns the highest streak number found across all habits."""
    if not habits_list:
        return 0
    return max([calculate_streak(h.completions, h.periodicity) for h in habits_list])