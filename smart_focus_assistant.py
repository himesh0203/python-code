Setup

Install required packages:

pip install plyer psutil


Run the assistant:

python smart_focus_assistant.py


It runs in the background and pops up notifications every 25-60 minutes.



# smart_focus_assistant.py
# A background-running productivity & wellness assistant with desktop notifications

import time
import random
from datetime import datetime
from plyer import notification
import threading
import psutil

# ------------------- Motivational & Wellness Tips -------------------
tips = [
    "💧 Drink a glass of water.",
    "🧘 Take a 1-minute stretch break.",
    "💡 Focus for the next 25 minutes. You've got this!",
    "📝 Write down a small achievement.",
    "👀 Look away from the screen for 30 seconds.",
    "🫁 Take a deep breath and relax your shoulders."
]

# ------------------- Helper Functions -------------------
def send_notification(title, message):
    """Send a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=8  # seconds
    )

def random_tip():
    """Return a random wellness tip."""
    return random.choice(tips)

# ------------------- Activity Monitoring -------------------
def is_user_active(threshold_seconds=300):
    """Check if user has been active in the last threshold_seconds."""
    # We'll use CPU activity as a rough proxy for user activity
    idle_time = psutil.boot_time() - psutil.cpu_times().idle
    # This is a simplified approximation
    return True  # In real usage, replace with proper idle detection for your OS

# ------------------- Micro-break Scheduler -------------------
def micro_break_scheduler(interval_minutes=60):
    """Send wellness reminders at regular intervals."""
    while True:
        time.sleep(interval_minutes * 60)
        send_notification("⏰ Micro-Break Time!", random_tip())

# ------------------- Pomodoro Reminder -------------------
def pomodoro_session(focus_minutes=25):
    """Notify user to focus, then suggest break."""
    while True:
        send_notification("🔔 Focus Time!", f"Focus for {focus_minutes} minutes now!")
        time.sleep(focus_minutes * 60)
        send_notification("✅ Focus Session Complete!", "Take a short break now.")

# ------------------- Main Program -------------------
def main():
    print("✨ Smart Focus & Wellness Assistant Started ✨")
    print(f"Today's Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    print("Running in the background with wellness reminders...\n")

    # Start background threads
    micro_break_thread = threading.Thread(target=micro_break_scheduler, args=(60,), daemon=True)
    pomodoro_thread = threading.Thread(target=pomodoro_session, args=(25,), daemon=True)

    micro_break_thread.start()
    pomodoro_thread.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAssistant stopped. Stay productive and healthy! 😊")

if __name__ == "__main__":
    main()
