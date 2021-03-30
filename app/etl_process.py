from database import Database
import json
import time
import requests

# Get the city names from the local static file
def getCityNamesFromFile(filePath):
    json_file = open(filePath, "rb")
    city_records = json.load(json_file)

    json_file.close()

    return [city["name"] for city in city_records]

# Get the api key for the wheather app
def getConfig(filePath):
    config_file = open(filePath, "rb")
    config = json.load(config_file)
    
    config_file.close()

    return config

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
    cities = getCityNamesFromFile("ca.city.lst.json")
    config = getConfig("/config.json")
    
    api_key = config["key"]
    db_host = config["db_host"]
    db_user = config["db_user"]
    db_port = config["db_port"]
    db_name = config["db_name"]

    while True:
        for city in cities:
            weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},ca&APPID={api_key}")
            transformed_data = transform(weather_data)

            ## Establish database connection
            db = Database(db_user=db_user, db_port=db_port, db_name=db_name, db_host=db_host)

            ## Sleep for 3 seconds between each api request to reduece api key over used
            time.sleep(3)

