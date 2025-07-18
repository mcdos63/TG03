import sqlite3
import requests, logging

TOKEN = 'ТОКЕН'
# Ваш API-ключ от OpenWeatherMap
API_KEY = 'КЛЮЧ'

# Координаты для погоды
latitude = 53.259037
longitude = 50.217396

async def get_weather(latitude=latitude, longitude=longitude):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return "Не удалось получить данные о погоде. Пожалуйста, попробуйте позже."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_name = data["name"]

        weather_info = {
            "город": city_name,
            "температура": f"{temp:.1f}°C",
            "ощущается_как": f"{feels_like:.1f}°C",
            "влажность": f"{humidity}%",
            "скорость_ветра": f"{wind_speed} м/с",
            "описание": weather
        }
        return weather_info

    except Exception as e:
        logging.error(f"Ошибка при получении данных о погоде: {e}")
        return "Не удалось получить данные о погоде. Пожалуйста, попробуйте позже."

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT)
    ''')
    conn.commit()
    conn.close()

