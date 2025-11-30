
import datetime

class Task:
    def __init__(self, category: str, subcategory: str, description: str,
                 due: datetime.datetime, duration: float):
        self.category = category.strip().lower()       # school, personal, work
        self.subcategory = subcategory.strip().lower() # e.g., math, gym, job
        self.description = description.strip()
        self.due = due
        self.duration = float(duration)                # hours
