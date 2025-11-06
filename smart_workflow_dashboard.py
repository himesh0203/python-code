# smart_workflow_dashboard.py
# Professional Smart Workflow Dashboard with GUI, Task Prioritization, and Scheduling

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# ------------------- Global Variables -------------------
tasks = []  # Each task: {"task": str, "deadline": str, "estimated_time": int, "cluster": int, "priority": float}

# ------------------- Task Management -------------------
def add_task():
    task_name = simpledialog.askstring("Add Task", "Enter Task Name:")
    if not task_name: return
    deadline = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
    estimated_time = simpledialog.askinteger("Estimated Time", "Enter estimated time in minutes:")
    tasks.append({"task": task_name, "deadline": deadline, "estimated_time": estimated_time})
    log_task(task_name, deadline, estimated_time)
    update_task_list()

def edit_task():
    selected = task_listbox.curselection()
    if not selected: return
    idx = selected[0]
    task = tasks[idx]
    new_name = simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=task["task"])
    if new_name: task["task"] = new_name
    new_deadline = simpledialog.askstring("Edit Deadline", "Enter new deadline (YYYY-MM-DD):", initialvalue=task["deadline"])
    if new_deadline: task["deadline"] = new_deadline
    new_time = simpledialog.askinteger("Edit Time", "Enter new estimated time in minutes:", initialvalue=task["estimated_time"])
    if new_time: task["estimated_time"] = new_time
    update_task_list()

def delete_task():
    selected = task_listbox.curselection()
    if not selected: return
    idx = selected[0]
    tasks.pop(idx)
    update_task_list()

def complete_task():
    selected = task_listbox.curselection()
    if not selected: return
    idx = selected[0]
    tasks[idx]["completed"] = True
    update_task_list()

def update_task_list():
    task_listbox.delete(0, tk.END)
    for t in tasks:
        status = "✅" if t.get("completed") else "❌"
        prio = f"{t.get('priority', 0):.2f}"
        task_listbox.insert(tk.END, f"{t['task']} | Deadline: {t['deadline']} | Time: {t['estimated_time']} min | Priority: {prio} | {status}")

# ------------------- Priority Scoring -------------------
def cluster_tasks():
    if not tasks: return
    task_texts = [t["task"] for t in tasks]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(task_texts)
    kmeans = KMeans(n_clusters=min(2,len(tasks)), random_state=42)
    kmeans.fit(X)
    for i, t in enumerate(tasks):
        t["cluster"] = kmeans.labels_[i]

def prioritize_tasks():
    today = datetime.date.today()
    cluster_tasks()
    for t in tasks:
        deadline = datetime.datetime.strptime(t["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days
        urgency_score = max(0, 10 - days_left)
        effort_score = t["estimated_time"] / 60
        cluster_score = 5 if t["cluster"] == 0 else 3
        t["priority"] = urgency_score * 0.5 + effort_score * 0.3 + cluster_score * 0.2
    tasks.sort(key=lambda x: x["priority"], reverse=True)

# ------------------- Scheduling -------------------
def generate_schedule():
    prioritize_tasks()
    work_start = datetime.datetime.strptime("09:00", "%H:%M")
    work_end = datetime.datetime.strptime("17:00", "%H:%M")
    schedule = []
    current_time = work_start
    for t in tasks:
        duration = datetime.timedelta(minutes=t["estimated_time"])
        if current_time + duration <= work_end:
            schedule.append(f"{current_time.time()} - {(current_time + duration).time()} : {t['task']}")
            current_time += duration
        else:
            schedule.append(f"Tomorrow : {t['task']}")
    schedule_text = "\n".join(schedule)
    messagebox.showinfo("Today's Schedule", schedule_text)

# ------------------- Logging -------------------
def log_task(task_name, deadline, estimated_time):
    with open("task_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{task_name},{deadline},{estimated_time}\n")

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Smart Workflow Dashboard")
root.geometry("700x500")

tk.Label(root, text="Smart Workflow Dashboard", font=("Helvetica", 16, "bold")).pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Add Task", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Edit Task", command=edit_task).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete Task", command=delete_task).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Complete Task", command=complete_task).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Generate Schedule", command=generate_schedule).grid(row=0, column=4, padx=5)

task_listbox = tk.Listbox(root, width=100)
task_listbox.pack(pady=20)

tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

root.mainloop()
