import json

json_file = open("ca.city.lst.json", "rb")
ca_cities = json.load(json_file)

for city in ca_cities:
    if(city['name'] == "Calgary"):
        print(city)

json_file.close()