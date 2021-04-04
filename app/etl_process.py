from database import Database
from util import getCityNamesFromFile, getConfig, transform, MAJOR_CITIES
import json
import time
import requests

def transform(weather_data):
    return {
        "city_id": weather_data['id'],
        "city_name": weather_data['name'],
        "country": weather_data['sys']['country'],
        "temp": weather_data['main']['temp'], #Default tempurature is Kelvin
        "feels_like": weather_data['main']['feels_like'],
        "temp_min": weather_data['main']['temp_min'],
        "temp_max": weather_data['main']['temp_max'],
        "pressure": weather_data['main']['pressure'],
        "humidity": weather_data['main']['humidity'],
        "wind_speed": weather_data['wind']['speed'],
        "sunrise": weather_data['sys']['sunrise'] + weather_data['timezone'], #Convert to local timezone
        "sunset": weather_data['sys']['sunset'] + weather_data['timezone']
    }

if __name__ == "__main__":
    ## Use S3 bucket to store the json file on AWS
    cities = getCityNamesFromFile("static/ca.city.lst.json", MAJOR_CITIES)
    config = getConfig("/var/weather_config.json")
    
    api_key = config["key"]
    db_host = config["db_host"]
    db_user = config["db_user"]
    db_port = config["db_port"]
    db_name = config["db_name"]
    db_password = config["db_password"]

    while True:
        ## Establish database connection
        db = Database(db_user=db_user, db_port=db_port, db_name=db_name, db_host=db_host, db_password=db_password)
        db.setup_db_connection()

        for city in cities:
            city_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},ca&APPID={api_key}")
            
            city_data_dict = json.loads(city_data.content.decode("utf-8"))
            transformed_data = transform(city_data_dict)

            successful = db.update_weather(transformed_data)
            if successful:
                print(f"Weather data for {city}, CA updated successfully.")
            else:
                print(f"Something is wrong with updating weather data for {city}")

            ## Sleep for 1 second between each api request to reduece api key over used
            time.sleep(1)
        
        db.close_session()