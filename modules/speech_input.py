import speech_recognition as sr
from core.config import WAKE_WORD

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300      # Noise sensitivity
recognizer.dynamic_energy_threshold = True


def listen_for_wake_word() -> bool:
 
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("[JARVIS] Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()
            print(f"[JARVIS] Heard: {text}")
            return WAKE_WORD in text
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return False


def listen_for_command() -> str:

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("[JARVIS] Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"[JARVIS] Command: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[JARVIS] STT Error: {e}")
            return ""
