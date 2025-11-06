# smart_task_planner.py
# A Python tool that analyzes and prioritizes your daily to-do list intelligently.

import re
from datetime import datetime, timedelta

def estimate_priority(task: str) -> int:
    """Estimate priority level based on keywords."""
    keywords = {
        "urgent": 5, "today": 5, "asap": 5,
        "important": 4, "meeting": 4,
        "email": 3, "call": 3,
        "review": 2, "read": 1, "optional": 1
    }
    score = sum(value for word, value in keywords.items() if word in task.lower())
    return score or 2  # default medium priority


def estimate_time(task: str) -> int:
    """Roughly estimate task time in minutes based on context."""
    if "meeting" in task.lower() or "call" in task.lower():
        return 30
    elif any(x in task.lower() for x in ["email", "reply", "review"]):
        return 10
    elif any(x in task.lower() for x in ["report", "project", "presentation"]):
        return 60
    else:
        return 20


def plan_day(tasks: list[str]):
    """Generate a structured daily plan from a list of tasks."""
    print("\n🧠 SMART DAILY PLAN -", datetime.now().strftime("%A, %B %d, %Y"))
    print("="*55)

    # Analyze tasks
    analyzed = []
    for t in tasks:
        analyzed.append({
            "task": t.strip(),
            "priority": estimate_priority(t),
            "duration": estimate_time(t)
        })

    # Sort by priority descending
    analyzed.sort(key=lambda x: x["priority"], reverse=True)

    # Display results with time allocation
    start_time = datetime.now().replace(second=0, microsecond=0)
    for i, item in enumerate(analyzed, start=1):
        end_time = start_time + timedelta(minutes=item["duration"])
        print(f"\n{i}. {item['task']}")
        print(f"   ⏱ Duration: {item['duration']} min | 🔥 Priority: {item['priority']}")
        print(f"   🕒 Suggested Time: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}")
        start_time = end_time + timedelta(minutes=5)  # short break

    print("\n✅ Day planned successfully! Stay productive 🚀")


if __name__ == "__main__":
    print("Enter your tasks (type 'done' to finish):")
    tasks = []
    while True:
        task = input("- ")
        if task.lower() == "done":
            break
        if task.strip():
            tasks.append(task)

    if tasks:
        plan_day(tasks)
    else:
        print("No tasks entered. Nothing to plan!")
