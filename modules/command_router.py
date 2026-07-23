import re
import os
import subprocess
import webbrowser
import psutil
import threading
import time
from modules.system_control import (
    open_app, close_app, set_volume, set_brightness, 
    shutdown, restart, cancel_shutdown
)
from modules.reminder     import set_reminder
from modules.email_sender import send_email
from modules.info_services import get_weather, get_news
from modules.ai_brain     import get_ai_response
from core.memory          import get_user_name


def clean_target(text: str) -> str:
    """Extra filler words ko target se saaf karta hai"""
    text = text.lower()
    fillers = ["my ", "please ", "can you ", "just ", "the "]
    for f in fillers:
        text = text.replace(f, "")
    return text.strip()


def background_reminder(task: str, minutes: int, name: str):
    """Background mein reminder timer chalane ke liye thread function"""
    time.sleep(minutes * 60)
    set_reminder(task, 0) 
    print(f"\n[JARVIS REMINDER] {name}, you asked me to remind you to: {task}")


def route_command(text: str) -> str:
    """
    User command parse karke sahi development ya system action execute karta hai.
    """
    t = text.lower().strip()
    name = get_user_name() or "Sir"

    if "on youtube" in t or t.startswith("youtube search "):
        query = t.replace("on youtube", "").replace("youtube search ", "").replace("search ", "").strip()
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching YouTube for: '{query}', {name}."

    if t.startswith("search for ") or t.startswith("google search ") or t.startswith("google "):
        query = t.replace("search for ", "").replace("google search ", "").replace("google ", "").strip()
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Executing Google search query for: '{query}', {name}."

    if "create script" in t and " to " in t:
        try:
            match = re.search(r"create script ([\w\.-]+) to (.+)", t)
            if match:
                file_name = match.group(1).strip()
                instruction = match.group(2).strip()
                
                prompt = f"Write ONLY clean executable Python code for the following task: {instruction}. Do not include any markdown format, explanations, or triple backticks. Just pure python code."
                raw_code = get_ai_response(prompt)
                clean_code = raw_code.replace("```python", "").replace("```", "").strip()
                
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(clean_code)
                    
                return f"Script '{file_name}' successfully compiled and saved to workspace, {name}."
        except Exception as e:
            return f"Failed to auto-generate script. Error: {e}"

    if "git push" in t or "commit and push" in t:
        try:
            if not os.path.exists(".git"):
                return "This directory is not configured as a Git repository, Sir."
            
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-commit by JARVIS Dev-Engine"], check=True)
            
            result = subprocess.run(["git", "push"], capture_output=True, text=True)
            if "Everything up-to-date" in result.stdout or "Everything up-to-date" in result.stderr:
                return f"Git Push bypassed: Repository is already up-to-date, {name}."
            return f"Git workspace synced. Commit and Push executed successfully, {name}."
        except subprocess.CalledProcessError:
            return "Git operation failed. Please verify your authentication or remote branch settings."

    if "system diagnostics" in t or "system report" in t:
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]
            
            report = f"Diagnostic Report: CPU utilization is at {cpu_usage}%. RAM consumption is at {memory.percent}%. "
            report += "Top active background tasks are: "
            report += ", ".join([f"{p['name']} (PID: {p['pid']})" for p in processes])
            return report
        except Exception as e:
            return f"Diagnostic run failed. Error: {e}"

    if "close" in t:
        target = t.split("close", 1)[1].strip()
        cleaned = clean_target(target)

        response = close_app(cleaned)

        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if cleaned in proc.info['name'].lower():
                    psutil.Process(proc.info['pid']).terminate()
                    killed = True
            except (psutil.NoSuchProcess, os.error, Exception):
                pass
        
        if killed:
            return f"App '{cleaned.capitalize()}' process force closed and terminated, {name}."
        return response

    if "kill process" in t or "force close" in t:
        target = t.replace("kill process ", "").replace("force close ", "").strip()
        cleaned = clean_target(target)
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if cleaned in proc.info['name'].lower():
                    psutil.Process(proc.info['pid']).terminate()
                    killed = True
            except (psutil.NoSuchProcess, os.error, Exception):
                pass
        if killed:
            return f"Process tree for '{cleaned}' successfully terminated, {name}."
        return f"Process '{cleaned}' was not detected in active system threads."

    web_shortcuts = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "linkedin": "https://www.linkedin.com",
        "facebook": "https://www.facebook.com"
    }

    if "open" in t:
        target = t.split("open", 1)[1].strip()
        cleaned = clean_target(target)
        
        if cleaned in web_shortcuts:
            webbrowser.open(web_shortcuts[cleaned])
            return f"Opening {cleaned.capitalize()} for you, {name}."
            
        return open_app(cleaned)

    if m := re.search(r"set volume (?:to )?(\d+)", t):
        set_volume(int(m.group(1)))
        return f"Volume set to {m.group(1)}%."

    if "mute" in t:
        from modules.system_control import mute_volume
        mute_volume()
        return "System muted."

    if m := re.search(r"set brightness (?:to )?(\d+)", t):
        set_brightness(int(m.group(1)))
        return f"Brightness set to {m.group(1)}%."

    if "shutdown" in t:
        shutdown(30)
        return "Shutting down system in 30 seconds. Say 'cancel shutdown' to abort."
    if "restart" in t or "reboot" in t:
        restart()
        return "Restarting system."
    if "cancel shutdown" in t:
        cancel_shutdown()
        return "Shutdown cancelled."

    if m := re.search(r"remind(?:er)? (?:me )?(?:to )?(.+?) in (\d+) minute", t):
        task = m.group(1).strip()
        minutes = int(m.group(2))

        t_thread = threading.Thread(target=background_reminder, args=(task, minutes, name), daemon=True)
        t_thread.start()
        
        return f"Understood, {name}. I will remind you to '{task}' in exactly {minutes} minutes."

    if "weather" in t:
        if m := re.search(r"weather (?:in|of|for) (.+)", t):
            city = clean_target(m.group(1))
            return get_weather(city)
        return get_weather()

    if "news" in t or "headlines" in t:
        for cat in ["technology", "sports", "business", "health", "science"]:
            if cat in t:
                return get_news(cat)
        return get_news()

    if "send email" in t or "send mail" in t:
        if m := re.search(r"(?:to|email) ([\w\.-]+@[\w\.-]+)", t):
            return send_email(
                to=m.group(1),
                subject="Message from JARVIS",
                body=f"This email was sent via JARVIS on your behalf, {name}."
            )
        return "Please say: 'send email to someone@example.com'"


    if any(w in t for w in ["hello", "hi", "hey"]):
        return f"Hello {name}! All systems operational. How can I assist?"

    if "your name" in t or "who are you" in t:
        return "I am JARVIS — Just A Rather Very Intelligent System. At your service."

    return get_ai_response(text)