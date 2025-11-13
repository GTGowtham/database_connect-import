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

def get_weather_data():
      url=f"{base_url}?q={city}&appid={api_key}"
      
      try:
            response=requests.get(url)
            data=response.json()
            return data
      except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            sys.exit(1)
            return None
      city_name=data.get("name")
      main=data.get("main",{})
      weather_list=data.get("weather",[{}])

      temparature=main.get("temp")
      humidity=main.get("humidity")
      description=weather_list[0].get("description")


      if None in(city,temparture,humidity,description):
            print("some data is missing")
            return 0;

      return{
            "city":city_name,
            "temparature":temparature,
            "humidity":humidity,
            "description":description
      }
if __name__=="__main__":
      