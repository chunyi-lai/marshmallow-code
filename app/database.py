from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, insert
import etl_process as ep
import requests
import json
import time
import datetime

class Database():
    def __init__(self, db_user, db_port, db_name, db_host, db_password):
        '''
        Constructor
        '''
        self.db_user = db_user
        self.db_port = db_port
        self.db_name = db_name
        self.db_host = db_host
        self.db_password = db_password
    
    def setup_db_connection(self):
        '''
        Setup the db connection
        '''

        # Create engine
        self.engine = create_engine(f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}")

        Base = automap_base()
        Base.prepare(self.engine, reflect=True)

        # Obain the weather table object
        self.weather = Base.classes.weather

        # Establish session connection
        self.db_session = Session(self.engine)

    # Get weather data with specific city
    def get_weather(self, city):
        try:
            weather_record = self.db_session.query(
                self.weather.city_id,
                self.weather.city_name,
                self.weather.country,
                self.weather.temp,
                self.weather.feels_like,
                self.weather.temp_min,
                self.weather.temp_max,
                self.weather.pressure,
                self.weather.humidity,
                self.weather.wind_speed,
                self.weather.sunrise,
                self.weather.sunset
            ).filter(self.weather.city_name.lower() == city.lower()).first()

            weather_record_dicts = {
                "city_id": weather_record[0],
                "city_name": weather_record[1],
                "country": weather_record[2],
                "temp": weather_record[3],
                "feels_like": weather_record[4],
                "temp_min": weather_record[5],
                "temp_max": weather_record[6],
                "pressure": weather_record[7],
                "humidity": weather_record[8],
                "wind_speed": weather_record[9],
                "sunrise": weather_record[10],
                "sunset": weather_record[11]
            }
            self.db_session.commit()

            return weather_record_dicts

        except:
            print(f"Error while querying weather for specific city: {city}.")
            print(f"City, {city}, might not exist in the server.")

            return dict()
    
    # Insert into database for the first time
    def insert_weather(self, new_data):
        try:
            statement = insert(self.weather).values(
                city_id=new_data["city_id"],
                city_name=new_data["city_name"],
                country=new_data["country"],
                temp=new_data["temp"],
                feels_like=new_data["feels_like"],
                temp_min=new_data["temp_min"],
                temp_max=new_data["temp_max"],
                pressure=new_data["pressure"],
                humidity=new_data["humidity"],
                wind_speed=new_data["wind_speed"],
                sunrise=datetime.datetime.fromtimestamp(new_data["sunrise"]),
                sunset=datetime.datetime.fromtimestamp(new_data["sunset"])
            )
            connection = self.engine.connect()
            connection.execute(statement)
            return True
        except Exception as e:
            print(f"Error while inserting new data. City: {new_data['city_name']}")
            print(e)
            return False

    # Update weather for specific city
    def update_weather(self, new_data):
        try:
            update(self.weather).where(self.weather.city_name.lower() == new_data["city_name"].lower()).values(
                temp=new_data["temp"],
                feels_like=new_data["feels_like"],
                temp_min=new_data["temp_min"],
                temp_max=new_data["temp_max"],
                pressure=new_data["pressure"],
                humidity=new_data["humidity"],
                wind_speed=new_data["wind_speed"],
                sunrise=datetime.datetime.fromtimestamp(new_data["sunrise"]),
                sunset=datetime.datetime.fromtimestamp(new_data["sunset"])
            )
            connection = self.engine.connect()
            connection.execute(statement)
            return True
        except:
            print(f"Error while updating data. City: {new_data['city_name']}")
            return False
    
    # close the session
    def close_session(self):
        self.db_session.close()

if __name__ == "__main__":
    major_cities = ["Calgary", "Edmonton", "Red Deer", "Vancouver", "Surrey", 
        "Kelowna", "Saskatoon", "Regina", "London", "Kingston", "Toronto", "Ottawa",
        "Halifax", "Winnipeg", "Windsor", "Prince Albert", "St. John's", "Guelph",
        "Kitchener", "Yellowknife"]
    cities = ep.getCityNamesFromFile("ca.city.lst.json", major_cities)
    config = ep.getConfig("/config.json")

    api_key = config["key"]
    db_host = config["db_host"]
    db_user = config["db_user"]
    db_port = config["db_port"]
    db_name = config["db_name"]
    db_password = config["db_password"]

    ## Establish database connection
    db = Database(db_user=db_user, db_port=db_port, db_name=db_name, db_host=db_host, db_password=db_password)
    db.setup_db_connection()


    for city in cities:
        city_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},ca&APPID={api_key}")

        city_data_dict = json.loads(city_data.content.decode("utf-8"))
        transformed_data = ep.transform(city_data_dict)

        ## Insert data into the database
        success = db.insert_weather(transformed_data)
        if success:
            print(f"Weather data for {city}, CA inserted successfully.")
        else:
            print(f"Something is wrong with inserting Weather data for {city}")

        time.sleep(2)
    
    db.close_session()