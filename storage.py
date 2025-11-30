import json
import os
import datetime
from models import Task

DATA_FILE = "tasks.json"

def save_tasks(tasks):
    raw = [
        {
            "category": t.category,
            "subcategory": t.subcategory,
            "description": t.description,
            "due": t.due.isoformat(),
            "duration": t.duration
        }
        for t in tasks
    ]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return []  # start fresh if corrupted

    tasks = []
    for t in raw:
        try:
            due = datetime.datetime.fromisoformat(t["due"])
            tasks.append(Task(t["category"], t["subcategory"], t["description"], due, t["duration"]))
        except Exception:
            # skip malformed entries
            continue
    return tasks
