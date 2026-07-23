import threading
import time

CONFIRM_TIMEOUT = 20  

CONFIRM_WORDS = {
    "yes", "yeah", "yep", "confirm", "confirmed", "do it",
    "proceed", "go ahead", "yes confirm", "yes jarvis", "affirmative"
}
CANCEL_WORDS = {
    "no", "nope", "cancel", "abort", "stop", "never mind", "nevermind", "negative"
}

_lock = threading.Lock()
_pending = None  


def request_confirmation(label: str, action) -> None:
    global _pending
    with _lock:
        _pending = {"label": label, "action": action, "expires": time.time() + CONFIRM_TIMEOUT}


def has_pending() -> bool:
    global _pending
    with _lock:
        if _pending is None:
            return False
        if time.time() > _pending["expires"]:
            _pending = None
            return False
        return True


def pending_label():
    with _lock:
        return _pending["label"] if _pending else None


def is_confirm_word(t: str) -> bool:
    return t.strip() in CONFIRM_WORDS


def is_cancel_word(t: str) -> bool:
    return t.strip() in CANCEL_WORDS


def confirm():
    global _pending
    with _lock:
        if _pending is None or time.time() > _pending["expires"]:
            _pending = None
            return None
        action = _pending["action"]
        _pending = None
    return action()


def clear_pending() -> None:
    global _pending
    with _lock:
        _pending = None
