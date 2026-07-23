# 🤖 J.A.R.V.I.S.

### *Just A Rather Very Intelligent System*

> **An AI-Powered Desktop Voice Assistant built with Python for intelligent conversations, voice automation, and productivity.**

---

## 🚀 Overview

**J.A.R.V.I.S.** is a modular AI-powered virtual assistant inspired by Iron Man's intelligent assistant. It enables users to interact with their computer using natural voice commands while performing various automation and productivity tasks.

The assistant integrates multiple cloud services such as **Groq AI**, **Google Cloud Speech APIs**, **Gmail API**, **OpenWeatherMap**, and **NewsAPI** to provide a fast, responsive, and intelligent experience.

---

# ✨ Features

* 🎙️ Voice Activation (Wake Word Detection)
* 🗣️ Speech-to-Text
* 🔊 Natural Text-to-Speech
* 🤖 AI Conversations using Groq (Llama Models)
* 💻 Launch Desktop Applications
* 🌤️ Real-Time Weather Information
* 📰 Latest News Headlines
* 📧 Voice-Controlled Email Sending
* ⏰ Reminder & Notification System
* 🧠 Persistent Memory Storage
* 🔆 Volume & Brightness Control
* 🖥️ Futuristic HUD Interface
* 🧩 Modular Python Architecture

---

# 🏗️ Project Structure

```text
JARVIS/
│
├── core/               # Configuration & Memory Management
├── modules/            # AI, Speech, Automation & Utilities
├── gui/                # HUD Interface
├── credentials/        # Google API Credentials
├── data/               # Memory Storage
├── main.py             # Entry Point
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

### Programming Language

* Python

### AI & APIs

* Groq API
* Google Cloud Speech-to-Text
* Google Cloud Text-to-Speech
* Gmail API
* OpenWeatherMap API
* NewsAPI

### Libraries

* Tkinter
* PyAudio
* SpeechRecognition
* JSON
* dotenv

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/mohd-atif245/JARVIS.git

cd JARVIS
```

---

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a **.env** file in the project directory.

```env
GROQ_API_KEY=
OPENWEATHER_API_KEY=
NEWS_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=
GMAIL_SENDER=
DEFAULT_CITY=
WAKE_WORD=jarvis
```

---

## 5️⃣ Run the Project

```bash
python main.py
```

---

# 🎤 Example Voice Commands

```text
Jarvis, open Chrome
Jarvis, what's the weather today?
Jarvis, latest technology news
Jarvis, set a reminder for 20 minutes
Jarvis, send an email
Jarvis, increase the volume
Jarvis, lower the brightness
```

---

# 🔒 Security

This project went through a security review after being shared publicly. The following protections are in place:

* **Confirmation gate for destructive actions** — `shutdown`, `restart`, `kill process` / `close` (force-kill), `git push`, and `send email` no longer execute on a single voice/text match. JARVIS asks for an explicit **'yes'** before running them, and any other input safely cancels the pending action. This guards against misrecognized speech (the free Google Web Speech STT tier has no confidence score to check) triggering something destructive by accident.
* **Sandboxed script generation** — the `create script` command no longer writes files using a raw filename from voice input. Filenames are sanitized, forced to a `.py` extension, and confined to a dedicated `generated_scripts/` folder with a path-containment check, so a malformed or malicious filename can't write or overwrite files elsewhere on disk. Overwriting an existing script also requires confirmation.
* **Known limitation** — the free-tier speech recognizer still doesn't expose per-word confidence, so misrecognition can still happen; the confirmation step is the current mitigation. A future improvement is switching to an STT engine that reports confidence scores.

---

# 📌 Future Improvements

* 🧠 Local LLM Integration
* 👤 Face Recognition Login
* 🏠 Smart Home Automation
* 📅 Google Calendar Integration
* 🌍 Multi-language Support
* 🔌 Plugin System
* 📱 Mobile Companion App

---



# 👨‍💻 Author

## **Muhammad Atif**

**Computer Science Student**

**Aspiring Cybersecurity Professional • Python Developer • AI & Automation Enthusiast**

---

# ⭐ Support

If you found this project helpful, consider giving it a **Star ⭐** on GitHub.

---

# 📄 License

This project is available for **educational and portfolio purposes**.
