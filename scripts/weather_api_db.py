import requests
import json
import pandas as pd
import os 
import sys
import pymysql
import sqlalchemy
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("weather_api")
city=os.getenv("location")

base_url="https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city: str):
    url = f"{base_url}?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # ensures HTTP errors raise exceptions
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)

    city_name = data.get("name")
    main = data.get("main", {})
    weather_list = data.get("weather", [{}])

    temperature = main.get("temp")
    humidity = main.get("humidity")
    description = weather_list[0].get("description")

    if None in (city_name, temperature, humidity, description):
        print("Some weather data is missing.")
        return None

    return {
        "city": city_name,
        "temperature": temperature,
        "humidity": humidity,
        "description": description
    }

if __name__ == "__main__":
    result = get_weather_data(city)
    if result:
        print(f"\nCity: {result['city']}")
        print(f"Temperature: {result['temperature']} °C")
        print(f"Humidity: {result['humidity']}%")
        print(f"Weather: {result['description']}")

      