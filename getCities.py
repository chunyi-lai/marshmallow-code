import json

json_file = open("city.list.json", "rb")

cities = json.load(json_file)
ca_cities = [city for city in cities if city["country"].lower() == "ca"]

ca_city_json = json.dumps(ca_cities)
ca_city_json_file = open("ca.city.lst.json", "w")
ca_city_json_file.write(ca_city_json)

json_file.close()
