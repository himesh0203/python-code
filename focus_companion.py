Run it in Python:

python focus_companion.py


Add your daily tasks

Start 25-minute focus sessions

Let it remind you to take micro-breaks, stretch, or drink water



# focus_companion.py
# A unique productivity assistant for daily work-life balance

import time
import random
from datetime import datetime

# ------------------- Motivational Prompts -------------------
motivational_quotes = [
    "Take a deep breath. You've got this!",
    "Remember to stretch your back and neck.",
    "Drink a glass of water. Hydration boosts productivity.",
    "Focus for the next 25 minutes, then take a break.",
    "Write down one small win from today.",
    "Close your eyes for 60 seconds and relax your mind."
]

# ------------------- Tasks Tracker -------------------
tasks_today = []

def add_task():
    task = input("Enter a task you want to track today: ").strip()
    if task:
        tasks_today.append({"task": task, "completed": False})
        print(f"Task added: {task}")

def complete_task():
    if not tasks_today:
        print("No tasks added yet.")
        return
    print("\nTasks:")
    for idx, t in enumerate(tasks_today, 1):
        status = "✅" if t["completed"] else "❌"
        print(f"{idx}. {t['task']} [{status}]")
    try:
        choice = int(input("Mark task number as completed: "))
        if 1 <= choice <= len(tasks_today):
            tasks_today[choice - 1]["completed"] = True
            print(f"Marked as completed: {tasks_today[choice - 1]['task']}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Enter a valid number.")

# ------------------- Micro-Break System -------------------
def micro_break_reminder():
    print("\n⏰ Time for a micro-break!")
    prompt = random.choice(motivational_quotes)
    print(f"💡 Tip: {prompt}\n")

# ------------------- Daily Planner -------------------
def show_tasks():
    if not tasks_today:
        print("No tasks added yet.")
        return
    print("\nToday's Tasks:")
    for t in tasks_today:
        status = "✅" if t["completed"] else "❌"
        print(f"- {t['task']} [{status}]")

# ------------------- Main Program -------------------
def main():
    print("✨ Welcome to Focus Companion - Your Smart Workday Assistant ✨")
    print(f"Today's Date: {datetime.now().strftime('%A, %B %d, %Y')}\n")

    while True:
        print("\nOptions:")
        print("1. Add a task")
        print("2. Complete a task")
        print("3. Show tasks")
        print("4. Take a micro-break now")
        print("5. Start focus session (25 min)")
        print("6. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            complete_task()
        elif choice == "3":
            show_tasks()
        elif choice == "4":
            micro_break_reminder()
        elif choice == "5":
            print("🔔 Focus session started for 25 minutes. Stay focused!")
            try:
                time.sleep(25 * 60)  # 25 minutes
                micro_break_reminder()
            except KeyboardInterrupt:
                print("\nFocus session interrupted.")
        elif choice == "6":
            print("Goodbye! Stay productive and healthy 😊")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
