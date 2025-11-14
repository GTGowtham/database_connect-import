import requests
import json
import pandas as pd
import os 
import sys
import pymysql
from sqlalchemy import create_engine,Column,String,Integer,Float
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
from sqlalchemy import DateTime,func
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

base=declarative_base()

class weather(base):
    __tablename__="weather_data"
    timestamp=Column(DateTime,server_default=func.now())
    id=Column(Integer,primary_key=True,autoincrement=True)
    city=Column(String(50))
    temperature=Column(Float)
    humidity=Column(Integer)
    description=Column(String(50))

db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_port=os.getenv("DB_PORT")
db_name=os.getenv("weather_db_name")

db_url=f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine=create_engine(db_url)
base.metadata.create_all(engine)


session=sessionmaker(bind=engine)
session=session()
print("successfully create tables")



if __name__ == "__main__":
    result = get_weather_data(city)
    if result:
        new_record = weather(
        city=result["city"],
        temperature=result["temperature"],
        humidity=result["humidity"],
        description=result["description"]
    )
    
    session.add(new_record)
    session.commit()
    print("weather data inserted successfully")



      