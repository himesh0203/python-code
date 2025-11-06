Setup

Install required packages:

pip install plyer


Run the program:

python smart_focus_gui.py





# smart_focus_gui.py
# Smart Focus & Wellness Assistant with GUI, analytics, and custom intervals

import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from datetime import datetime
from plyer import notification

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

# ------------------- Notification Helper -------------------
def send_notification(title, message):
    notification.notify(title=title, message=message, timeout=8)

def random_tip():
    return random.choice(tips)

# ------------------- Scheduler Threads -------------------
def micro_break_scheduler():
    while True:
        time.sleep(micro_break_interval * 60)
        send_notification("⏰ Micro-Break Time!", random_tip())
        print(f"Micro-break reminder sent at {datetime.now().strftime('%H:%M:%S')}")

def focus_session_scheduler():
    global completed_sessions
    while True:
        send_notification("🔔 Focus Time!", f"Focus for {focus_session_duration} minutes now!")
        print(f"Focus session started at {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(focus_session_duration * 60)
        completed_sessions += 1
        send_notification("✅ Focus Session Complete!", "Take a short break now!")
        print(f"Focus session completed at {datetime.now().strftime('%H:%M:%S')}")

# ------------------- GUI -------------------
def show_analytics():
    messagebox.showinfo("Daily Analytics",
                        f"Focus Sessions Completed: {completed_sessions}\n"
                        f"Micro-Break Interval: {micro_break_interval} min\n"
                        f"Focus Session Duration: {focus_session_duration} min")

def update_intervals():
    global micro_break_interval, focus_session_duration
    try:
        micro_break_interval = int(micro_entry.get())
        focus_session_duration = int(focus_entry.get())
        messagebox.showinfo("Intervals Updated", "Intervals updated successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers for intervals.")

root = tk.Tk()
root.title("Smart Focus & Wellness Assistant")
root.geometry("400x300")

tk.Label(root, text="Smart Focus & Wellness Assistant", font=("Helvetica", 14, "bold")).pack(pady=10)

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
tk.Button(root, text="Show Daily Analytics", command=show_analytics).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# ------------------- Start Scheduler Threads -------------------
threading.Thread(target=micro_break_scheduler, daemon=True).start()
threading.Thread(target=focus_session_scheduler, daemon=True).start()

root.mainloop()
