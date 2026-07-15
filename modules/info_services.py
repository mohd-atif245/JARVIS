import requests
from core.config import OPENWEATHER_KEY, DEFAULT_CITY, NEWS_API_KEY


def get_weather(city: str = None) -> str:
    city = city or DEFAULT_CITY
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    )
    try:
        r = requests.get(url, timeout=5).json()
        if r.get("cod") != 200:
            return f"Weather data unavailable for {city}."
        desc    = r["weather"][0]["description"].capitalize()
        temp    = r["main"]["temp"]
        feels   = r["main"]["feels_like"]
        humidity= r["main"]["humidity"]
        return (
            f"Weather in {city}: {desc}. "
            f"Temperature {temp}°C, feels like {feels}°C. "
            f"Humidity {humidity}%."
        )
    except Exception as e:
        return f"Could not fetch weather: {e}"


def get_news(category: str = "technology", count: int = 5) -> str:
    url = (
        f"https://newsapi.org/v2/top-headlines"
        f"?category={category}&pageSize={count}&language=en&apiKey={NEWS_API_KEY}"
    )
    try:
        r = requests.get(url, timeout=5).json()
        articles = r.get("articles", [])
        if not articles:
            return "No news available right now."
        headlines = [f"{i+1}. {a['title']}" for i, a in enumerate(articles[:count])]
        return "Here are today's top headlines: " + ". ".join(headlines)
    except Exception as e:
        return f"Could not fetch news: {e}"
