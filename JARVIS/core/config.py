import os
from dotenv import load_dotenv

load_dotenv()

# AI
GROQ_API_KEY       = os.getenv("GROQ_API_KEY")

# Google
GOOGLE_CREDS       = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Gmail
GMAIL_SENDER       = os.getenv("GMAIL_SENDER")

# Weather
OPENWEATHER_KEY    = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_CITY       = os.getenv("DEFAULT_CITY", "Karachi")

# News
NEWS_API_KEY       = os.getenv("NEWS_API_KEY")

# System
WAKE_WORD          = os.getenv("WAKE_WORD", "jarvis")
MEMORY_FILE        = os.getenv("MEMORY_FILE", "data/memory.json")
