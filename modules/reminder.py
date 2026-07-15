import threading
import time
from datetime import datetime
from plyer import notification
from core.memory import add_reminder, get_pending_reminders, _load, _save


def set_reminder(text: str, minutes: int):

    remind_time = datetime.now().strftime("%H:%M")
    add_reminder(text, remind_time)

    def _trigger():
        time.sleep(minutes * 60)
        notification.notify(
            title="⚡ JARVIS Reminder",
            message=text,
            app_name="JARVIS",
            timeout=10
        )
        # Mark as done
        data = _load()
        for r in data["reminders"]:
            if r["text"] == text and not r["done"]:
                r["done"] = True
                break
        _save(data)

    t = threading.Thread(target=_trigger, daemon=True)
    t.start()
    return f"Reminder set for {minutes} minute(s): '{text}'"


def check_overdue_reminders():

    pending = get_pending_reminders()
    if pending:
        for r in pending:
            notification.notify(
                title="⚡ JARVIS — Missed Reminder",
                message=r["text"],
                timeout=8
            )
