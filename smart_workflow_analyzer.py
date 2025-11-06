# smart_workflow_analyzer.py
# Professional Smart Workflow Analyzer & Task Prioritizer

import datetime
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ------------------- Sample Tasks -------------------
# In real-world, tasks can be imported from CSV, Google Calendar, Email API, etc.
tasks = [
    {"task": "Finish project report", "deadline": "2025-11-07", "estimated_time": 120}, # minutes
    {"task": "Reply to client emails", "deadline": "2025-11-06", "estimated_time": 30},
    {"task": "Prepare presentation slides", "deadline": "2025-11-08", "estimated_time": 90},
    {"task": "Team meeting", "deadline": "2025-11-06", "estimated_time": 60},
    {"task": "Code review", "deadline": "2025-11-07", "estimated_time": 45},
    {"task": "Update project plan", "deadline": "2025-11-09", "estimated_time": 60},
]

# ------------------- NLP-based Task Clustering -------------------
def cluster_tasks(tasks):
    task_texts = [t["task"] for t in tasks]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(task_texts)

    # Cluster tasks into 2 groups: urgent/important vs less urgent
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(X)
    clusters = kmeans.labels_
    
    for i, t in enumerate(tasks):
        t["cluster"] = clusters[i]
    return tasks

# ------------------- Priority Scoring -------------------
def prioritize_tasks(tasks):
    today = datetime.date.today()
    for t in tasks:
        deadline = datetime.datetime.strptime(t["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days
        urgency_score = max(0, 10 - days_left)  # closer deadlines get higher score
        effort_score = t["estimated_time"] / 60  # 1 point per hour
        cluster_score = 5 if t["cluster"] == 0 else 3  # cluster 0 = higher importance

        # Total priority = weighted sum
        t["priority"] = urgency_score * 0.5 + effort_score * 0.3 + cluster_score * 0.2
    # Sort tasks by priority descending
    tasks.sort(key=lambda x: x["priority"], reverse=True)
    return tasks

# ------------------- Schedule Suggestion -------------------
def generate_schedule(tasks, work_start="09:00", work_end="17:00"):
    schedule = []
    current_time = datetime.datetime.strptime(work_start, "%H:%M")
    work_end_time = datetime.datetime.strptime(work_end, "%H:%M")

    for t in tasks:
        task_duration = datetime.timedelta(minutes=t["estimated_time"])
        if current_time + task_duration <= work_end_time:
            schedule.append({"task": t["task"], "start_time": current_time.time(), "end_time": (current_time + task_duration).time()})
            current_time += task_duration
        else:
            # Task cannot fit today, suggest for next day
            schedule.append({"task": t["task"], "start_time": "Tomorrow", "end_time": "Tomorrow"})
    return schedule

# ------------------- Reporting -------------------
def display_schedule(schedule):
    print("\n📊 Suggested Work Schedule for Today:\n")
    for s in schedule:
        print(f"{s['start_time']} - {s['end_time']} : {s['task']}")

def display_prioritized_tasks(tasks):
    print("\n🔥 Prioritized Tasks:\n")
    for t in tasks:
        print(f"{t['task']} | Deadline: {t['deadline']} | Estimated Time: {t['estimated_time']} min | Priority Score: {t['priority']:.2f}")

# ------------------- Main Program -------------------
def main():
    print("✨ Smart Workflow Analyzer & Task Prioritizer ✨")
    
    clustered_tasks = cluster_tasks(tasks)
    prioritized_tasks = prioritize_tasks(clustered_tasks)
    
    display_prioritized_tasks(prioritized_tasks)
    
    schedule = generate_schedule(prioritized_tasks)
    display_schedule(schedule)

if __name__ == "__main__":
    main()
