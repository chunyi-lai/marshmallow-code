import json

MAJOR_CITIES = ["Calgary", "Edmonton", "Red Deer", "Vancouver", "Surrey", 
        "Kelowna", "Saskatoon", "Regina", "London", "Kingston", "Toronto", "Ottawa",
        "Halifax", "Winnipeg", "Windsor", "Prince Albert", "St. John's", "Guelph",
        "Kitchener", "Yellowknife"]

# Get the city names from the local static file
def getCityNamesFromFile(filePath, selectedCities):
    json_file = open(filePath, "rb")
    city_records = json.load(json_file)

    json_file.close()

    citySet = set(selectedCities)

    return [city["name"] for city in city_records 
        if city["name"] in citySet]

# Get the api key for the wheather app
def getConfig(filePath):
    config_file = open(filePath, "rb")
    config = json.load(config_file)
    
    config_file.close()

    return config

# Transform data from the api
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