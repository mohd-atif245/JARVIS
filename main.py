import threading
import time
import sys
import os

print("=" * 55)
print("  J.A.R.V.I.S  —  Initializing Systems...")
print("=" * 55)

from core.config  import GROQ_API_KEY, OPENWEATHER_KEY, NEWS_API_KEY
from core.memory  import get_user_name, set_user_name
from modules.reminder     import check_overdue_reminders
from modules.speech_input import listen_for_wake_word, listen_for_command
from modules.speech_output import speak


def check_env():
    missing = []
    if not GROQ_API_KEY or "your_" in GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not OPENWEATHER_KEY or "your_" in OPENWEATHER_KEY:
        missing.append("OPENWEATHER_API_KEY")
    if not NEWS_API_KEY or "your_" in NEWS_API_KEY:
        missing.append("NEWS_API_KEY")
    if missing:
        print(f"\n⚠  Missing API keys in .env: {', '.join(missing)}")
        print("   Please update your .env file and restart.\n")
    else:
        print("✓  All API keys loaded.")


def wake_word_listener(hud):
    """Background thread: wake word listen karta hai safely"""
    while True:
        try:
            if listen_for_wake_word():
                hud.after(0, lambda: hud.set_status("🔴 LISTENING..."))
                speak("Yes? How can I assist?")
                command = listen_for_command()
                if command:
                    hud.after(0, lambda cmd=command: hud.add_user_message(f"[Voice] {cmd}"))
                    threading.Thread(target=hud._process_cmd, args=(command,), daemon=True).start()
                hud.after(0, lambda: hud.set_status("Listening"))
        except Exception as e:
            print(f"[Wake word thread] Error: {e}")
            time.sleep(2)


def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("credentials", exist_ok=True)

    check_env()
    check_overdue_reminders()

    name = get_user_name()
    if name == "Sir":
        print("\nFirst time setup: What should JARVIS call you?")
        new_name = input("Your name (press Enter to skip): ").strip()
        if new_name:
            set_user_name(new_name)

    from gui.hud import JarvisHUD

    hud = JarvisHUD(on_text_command=lambda x: None)

    threading.Thread(target=wake_word_listener, args=(hud,), daemon=True).start()

    print("✓  JARVIS GUI launched. Say 'JARVIS' to activate voice mode.\n")
    speak(f"JARVIS online. Welcome back, {get_user_name()}. All systems nominal.")

    hud.mainloop()


if __name__ == "__main__":
    main()