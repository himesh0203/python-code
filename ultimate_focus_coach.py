Setup
pip install plyer


Run the assistant:

python ultimate_focus_coach.py


It now works as a full digital life/work coach, helping track your productivity, encourage wellness, and provide actionable insights daily.



# ultimate_focus_coach.py
# Ultimate Smart Productivity & Wellness Coach with logging and daily report

import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from datetime import datetime
from plyer import notification
import csv
import os

# ------------------- Motivational & Wellness Tips -------------------
tips = [
    "💧 Drink a glass of water.",
    "🧘 Take a 1-minute stretch break.",
    "💡 Focus for the next session. You've got this!",
    "📝 Write down a small achievement.",
    "👀 Look away from the screen for 30 seconds.",
    "🫁 Take a deep breath and relax your shoulders."
]

# ------------------- Global Variables -------------------
completed_sessions = 0
micro_break_interval = 60  # minutes
focus_session_duration = 25  # minutes
tasks = []

# CSV file to store daily logs
log_file = "productivity_log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Event", "Details"])

# ------------------- Helper Functions -------------------
def send_notification(title, message):
    notification.notify(title=title, message=message, timeout=8)
    log_event(title, message)

def random_tip():
    return random.choice(tips)

def log_event(event, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event, details])

# ------------------- Scheduler Threads -------------------
def micro_break_scheduler():
    while True:
        time.sleep(micro_break_interval * 60)
        tip = random_tip()
        send_notification("⏰ Micro-Break Time!", tip)

def focus_session_scheduler():
    global completed_sessions
    while True:
        send_notification("🔔 Focus Time!", f"Focus for {focus_session_duration} minutes now!")
        time.sleep(focus_session_duration * 60)
        completed_sessions += 1
        send_notification("✅ Focus Session Complete!", "Take a short break now!")

# ------------------- Task Management -------------------
def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append({"task": task, "completed": False})
        log_event("Task Added", task)
        update_task_list()
        task_entry.delete(0, tk.END)
        messagebox.showinfo("Task Added", f"Task added: {task}")
    else:
        messagebox.showwarning("Empty Input", "Please enter a task.")

def complete_task():
    try:
        selected = task_listbox.curselection()
        if selected:
            index = selected[0]
            tasks[index]["completed"] = True
            log_event("Task Completed", tasks[index]["task"])
            update_task_list()
            messagebox.showinfo("Task Completed", f"Task marked as completed: {tasks[index]['task']}")
        else:
            messagebox.showwarning("No Selection", "Select a task to mark as completed.")
    except Exception as e:
        print(e)

def update_task_list():
    task_listbox.delete(0, tk.END)
    for t in tasks:
        status = "✅" if t["completed"] else "❌"
        task_listbox.insert(tk.END, f"{t['task']} [{status}]")

# ------------------- Daily Report -------------------
def generate_report():
    completed_tasks = sum(1 for t in tasks if t["completed"])
    pending_tasks = len(tasks) - completed_tasks
    report = (
        f"📊 Daily Productivity Report\n\n"
        f"Focus Sessions Completed: {completed_sessions}\n"
        f"Tasks Completed: {completed_tasks}\n"
        f"Tasks Pending: {pending_tasks}\n"
        f"Micro-Break Interval: {micro_break_interval} min\n"
        f"Focus Session Duration: {focus_session_duration} min\n"
        f"Logged Events: See '{log_file}'"
    )
    messagebox.showinfo("Daily Report", report)
    log_event("Daily Report Generated", report)

# ------------------- GUI -------------------
def update_intervals():
    global micro_break_interval, focus_session_duration
    try:
        micro_break_interval = int(micro_entry.get())
        focus_session_duration = int(focus_entry.get())
        messagebox.showinfo("Intervals Updated", "Intervals updated successfully!")
        log_event("Intervals Updated", f"Micro-break: {micro_break_interval}, Focus: {focus_session_duration}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers.")

# ------------------- GUI Layout -------------------
root = tk.Tk()
root.title("Ultimate Focus & Wellness Coach")
root.geometry("500x500")

tk.Label(root, text="Ultimate Focus & Wellness Coach", font=("Helvetica", 16, "bold")).pack(pady=10)

# Interval Settings
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Micro-Break Interval (min):").grid(row=0, column=0, padx=5, pady=5)
micro_entry = tk.Entry(frame)
micro_entry.grid(row=0, column=1, padx=5, pady=5)
micro_entry.insert(0, str(micro_break_interval))

tk.Label(frame, text="Focus Session Duration (min):").grid(row=1, column=0, padx=5, pady=5)
focus_entry = tk.Entry(frame)
focus_entry.grid(row=1, column=1, padx=5, pady=5)
focus_entry.insert(0, str(focus_session_duration))

tk.Button(root, text="Update Intervals", command=update_intervals).pack(pady=5)

# Task Management
tk.Label(root, text="Tasks for Today:", font=("Helvetica", 12, "bold")).pack(pady=5)
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)
tk.Button(root, text="Add Task", command=add_task).pack(pady=2)
tk.Button(root, text="Complete Selected Task", command=complete_task).pack(pady=2)

task_listbox = tk.Listbox(root, width=60)
task_listbox.pack(pady=10)

# Daily Report
tk.Button(root, text="Generate Daily Report", command=generate_report).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# ------------------- Start Scheduler Threads -------------------
threading.Thread(target=micro_break_scheduler, daemon=True).start()
threading.Thread(target=focus_session_scheduler, daemon=True).start()

root.mainloop()
