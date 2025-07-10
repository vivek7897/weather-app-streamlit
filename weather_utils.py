import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(base_url, params=params)
    return response.json()

def get_forecast(city, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(base_url, params=params)
    return response.json()

def kelvin_to_celsius(k):
    return round(k - 273.15, 2)

def format_sun_time(timestamp, timezone):
    return datetime.utcfromtimestamp(timestamp + timezone).strftime('%H:%M')
