# main.py
# StudentSync entry point: menu, input, calendar view, agenda, completion, weekly stats.

import datetime
from models import Task
import storage
from utils import parse_datetime, format_date, format_time

def main():
    tasks = storage.load_tasks()
    completed = []  # track completed tasks separately (saved together on exit)

    while True:
        print("\n=== StudentSync ===")
        print("1. Add task")
        print("2. List tasks (calendar view)")
        print("3. Daily agenda (today only)")
        print("4. Mark task as completed")
        print("5. Weekly stats dashboard")
        print("6. Save and exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Add a new task
            print("\nCategories: School, Personal, Work")
            category = input("Enter category (school/personal/work): ").strip().lower()

            if category == "school":
                print("\nExamples of subcategories: Math, Science, English, History, Religion")
                subcategory = input("Enter subject (e.g., math, science, english): ").strip().lower()
                description = input("\nWhat school task? (e.g., 'Finish math homework', 'Write lab report'): ").strip()

            elif category == "personal":
                print("\nExamples of subcategories: Health, Social, Hobbies, Errands")
                subcategory = input("Enter type (e.g., health, social, hobbies, errands): ").strip().lower()
                description = input("\nWhat personal activity? (e.g., 'Go to the gym', 'Dinner with family'): ").strip()

            elif category == "work":
                print("\nExamples of subcategories: Job, Career, Side Hustle")
                subcategory = input("Enter type (e.g., part-time, career, side hustle): ").strip().lower()
                description = input("\nWhat work task? (e.g., 'Work shift at cafe', 'Update resume'): ").strip()

            else:
                print("\nUnknown category. You can still enter a custom subcategory.")
                subcategory = input("Enter subcategory: ").strip().lower()
                description = input("\nDescribe the task: ").strip()

            # Due date/time
            while True:
                due_str = input("\nDue date/time (YYYY-MM-DD HH:MM): ").strip()
                try:
                    due = parse_datetime(due_str)
                    break
                except ValueError as e:
                    print(e)

            # Duration
            while True:
                try:
                    duration = float(input("\nEstimated duration (hours, e.g., 1.5): ").strip())
                    if duration <= 0:
                        print("Duration must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a number (e.g., 2 or 1.5).")

            tasks.append(Task(category, subcategory, description, due, duration))
            print("✅ Task added!")

        elif choice == "2":
            # Calendar view: grouped by date, ordered by time, shows PENDING/DONE
            if not tasks and not completed:
                print("No tasks yet.")
            else:
                print("\n=== Calendar View ===")
                all_tasks = sorted(tasks + completed, key=lambda t: t.due)
                current_date = None
                for t in all_tasks:
                    date_str = format_date(t.due)
                    if date_str != current_date:
                        current_date = date_str
                        print(f"\n📅 {current_date}")
                    status = "DONE" if t in completed else "PENDING"
                    print(
                        f"  [{t.category.capitalize()} - {t.subcategory.capitalize()}] "
                        f"{t.description} | {format_time(t.due)} | {t.duration:.1f}h | {status}"
                    )

        elif choice == "3":
            # Daily agenda: today's tasks only, in chronological order
            today_str = format_date(datetime.datetime.now())
            today_tasks = [t for t in tasks if format_date(t.due) == today_str]
            if not today_tasks:
                print(f"No tasks scheduled for today ({today_str}).")
            else:
                print(f"\n=== Today’s Agenda ({today_str}) ===")
                for t in sorted(today_tasks, key=lambda x: x.due):
                    print(
                        f"  [{t.category.capitalize()} - {t.subcategory.capitalize()}] "
                        f"{t.description} | {format_time(t.due)} | {t.duration:.1f}h"
                    )

        elif choice == "4":
            # Mark task as completed
            if not tasks:
                print("No pending tasks.")
            else:
                print("\n=== Pending Tasks ===")
                for i, t in enumerate(tasks, 1):
                    print(f"{i}. [{t.category} - {t.subcategory}] {t.description} "
                          f"(due {format_date(t.due)} {format_time(t.due)})")
                try:
                    idx = int(input("Enter task number to mark as completed: ").strip())
                    if 1 <= idx <= len(tasks):
                        done_task = tasks.pop(idx - 1)
                        completed.append(done_task)
                        print(f"✅ Marked '{done_task.description}' as completed.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "5":
            # Weekly stats dashboard: group by ISO week (year-Wweek)
            all_tasks = tasks + completed
            if not all_tasks:
                print("\nNo tasks to show stats for.")
            else:
                print("\n=== Weekly Stats Dashboard ===")
                weekly = {}
                for t in all_tasks:
                    year, week, _ = t.due.isocalendar()
                    key = f"{year}-W{week}"
                    if key not in weekly:
                        weekly[key] = {"pending": [], "done": []}
                    (weekly[key]["done"] if t in completed else weekly[key]["pending"]).append(t)

                for key in sorted(weekly.keys()):
                    pending_tasks = weekly[key]["pending"]
                    done_tasks = weekly[key]["done"]
                    pending_count = len(pending_tasks)
                    done_count = len(done_tasks)
                    total_count = pending_count + done_count
                    pending_hours = sum(t.duration for t in pending_tasks)
                    done_hours = sum(t.duration for t in done_tasks)
                    total_hours = pending_hours + done_hours

                    print(f"\n📅 {key}")
                    print(f"  Total tasks: {total_count} ({total_hours:.1f}h)")
                    print(f"  Pending tasks: {pending_count} ({pending_hours:.1f}h)")
                    print(f"  Completed tasks: {done_count} ({done_hours:.1f}h)")

        elif choice == "6":
            # Save and exit (saves both pending and completed together)
            storage.save_tasks(tasks + completed)
            print("💾 Tasks saved. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1–6.")

if __name__ == "__main__":
    main()