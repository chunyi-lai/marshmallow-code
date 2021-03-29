-- Create the user vagrant
CREATE ROLE vagrant WITH LOGIN;

-- Grant privileges to the real_time_weather database
GRANT ALL PRIVILEGES ON DATABASE real_time_weather TO vagrant;

-- Grant privileges to the tables
-- GRANT ALL PRIVILEGES ON weather TO vagrant;
