import os
import time
import pygame
from gtts import gTTS

try:
    pygame.mixer.init()
except Exception as e:
    print(f"[JARVIS] Mixer Init Warning: {e}")

def speak(text: str):

    print(f"[JARVIS] Speaking: {text}")

    if not text or "System Error" in text:
        return
        
    os.makedirs("data", exist_ok=True)

    temp_file = f"data/reply_{int(time.time())}.mp3"
    
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(temp_file)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()

        try:
            os.remove(temp_file)
        except Exception:
            pass 

    except Exception as e:
        print(f"[JARVIS] TTS Error: {e}")