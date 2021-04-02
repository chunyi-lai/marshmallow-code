from database import Database
from util import getCityNamesFromFile, getConfig, transform, MAJOR_CITIES
from flask import Flask, render_template, jsonify, request, json

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/rawdata")
def rawdata():
    return render_template("rawdata.html")

@app.route("/api/weathers", methods=['GET', 'POST'])
def get_selected_weathers():
    try:
        ## obtain database credentials 
        config = getConfig("/config.json")
        
        api_key = config["key"]
        db_host = config["db_host"]
        db_user = config["db_user"]
        db_port = config["db_port"]
        db_name = config["db_name"]
        db_password = config["db_password"]

        ## establish the database connection
        db = Database(db_user=db_user, db_port=db_port, db_name=db_name, 
            db_host=db_host, db_password=db_password)
        db.setup_db_connection()

        ## Get the cities
        # params = request.get_json()["cities"]
        # print(params)

        ## Obtain the result from the database
        results = db.get_weather_for_all_cities()

        return jsonify(results), 200
    except Exception as e:
        return jsonify({
            "error": f"Something went wrong while requesting weather data. Error: {e}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)