BEGIN;
-- Create the wheather table

CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INT,
    city_name VARCHAR(100),
    country VARCHAR(30),
    temp FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    preasure FLOAT,
    humidity INT,
    wind_speed FLOAT,
    sunrise TIMESTAMP,
    sunset TIMESTAMP
);

GRANT ALL PRIVILEGES ON weather TO vagrant;
-- GRANT USAGE, SELECT ON SEQUENCE weather_wheather_id_seq TO vagrant;

END;