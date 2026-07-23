import requests
from core.config import GROQ_API_KEY
from core.memory import get_recent_context, get_user_name

SYSTEM_PROMPT = """You are JARVIS — an advanced AI personal assistant, 
inspired by Iron Man's AI. You speak in a professional, slightly witty tone. 
You address the user as '{name}'. Keep answers concise (under 4 sentences 
unless more detail is explicitly asked). You have access to the user's 
recent conversation history for context."""

def get_ai_response(user_input: str) -> str:

    name = get_user_name() or "Sir"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(name=name)}]

    try:
        recent = get_recent_context(n=6)
        if recent and isinstance(recent, list):
            for turn in recent:
                if isinstance(turn, dict) and "user" in turn and "jarvis" in turn:
                    if turn["user"].strip() and turn["jarvis"].strip():
                        messages.append({"role": "user", "content": turn["user"].strip()})
                        messages.append({"role": "assistant", "content": turn["jarvis"].strip()})
    except Exception as mem_err:
        print(f"[Memory Read Warning]: {mem_err}")

    if not user_input.strip():
        return "I didn't catch anything, Sir."
        
    messages.append({"role": "user", "content": user_input.strip()})

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            print(f"--- GROQ ERROR LOG ---")
            print(response.text)
            print(f"----------------------")
            return f"System Error: Received status code {response.status_code} from cloud brain."
            
    except Exception as e:
        return f"I'm having trouble connecting to my cloud brain, {name}. Error: {e}"