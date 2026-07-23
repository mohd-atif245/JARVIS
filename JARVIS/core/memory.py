import json
import os
from datetime import datetime
from core.config import MEMORY_FILE


def _load() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {"user_name": "Sir", "conversations": [], "reminders": [], "preferences": {}}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def _save(data: dict):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def remember_conversation(user_text: str, jarvis_reply: str):
    """Conversation history save karta hai"""
    data = _load()
    data["conversations"].append({
        "timestamp": datetime.now().isoformat(),
        "user": user_text,
        "jarvis": jarvis_reply
    })
    data["conversations"] = data["conversations"][-50:]
    _save(data)


def get_recent_context(n: int = 6) -> list:
    """Last N conversations return karta hai (AI context ke liye)"""
    data = _load()
    return data["conversations"][-n:]


def set_preference(key: str, value):
    data = _load()
    data["preferences"][key] = value
    _save(data)


def get_preference(key: str, default=None):
    return _load()["preferences"].get(key, default)


def get_user_name() -> str:
    return _load().get("user_name", "Sir")


def set_user_name(name: str):
    data = _load()
    data["user_name"] = name
    _save(data)


def add_reminder(text: str, time_str: str):
    data = _load()
    data["reminders"].append({"text": text, "time": time_str, "done": False})
    _save(data)


def get_pending_reminders() -> list:
    return [r for r in _load()["reminders"] if not r["done"]]
