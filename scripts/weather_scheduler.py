import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.weather_api_db import get_weather_data, session, weather, city
from apscheduler.schedulers.blocking import BlockingScheduler

def save_weather():
    data = get_weather_data(city)
    if data:
        record = weather(
            city=data["city"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            description=data["description"]
        )
        session.add(record)
        session.commit()
        print("Weather data inserted.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    #scheduler.add_job(save_weather, 'cron', hour='7,13,20', minute=0)
    scheduler.add_job(save_weather, 'interval', seconds=30)

    #print("Scheduler started. Running at 7 AM, 1 PM, and 8 PM.")
    print("data will be fetched every 30 seconds.")
    scheduler.start()
