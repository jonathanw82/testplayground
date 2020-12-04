import requests
import os
import json
from flask import Flask
from os import path
if path.exists("env.py"):
    import env

# app = Flask(__name__)
# app.config['WEATHER_KEY'] = os.getenv('WEATHER_KEY')

keyweather = os.getenv('WEATHER_KEY')
keygeo = os.getenv('GEO_KEY')
userinput = 'BRISTOL'

# coridnates api

geokeyapi = ',UK&key=' + keygeo
responsegeo = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={userinput}{geokeyapi}")
geo = responsegeo.json()
geofomat_str = json.dumps(geo, indent=2) 
data = json.loads(geofomat_str)

for bar in data['results']:
    pin = bar['geometry']['lng']
    pin2 = bar['geometry']['lat']
    print(bar['formatted'])
    print(bar['geometry'])

print("%.2f" % pin)
print("%.2f" % pin2)

# wather api call 
# queryweather = "q=" + userinput + ",GB&units=metric"                
# keyweatherapi = '&appid='+ keyweather

# response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?{queryweather}{keyweatherapi}")
# weatherresp = response.json()
# weather_formatted_str = json.dumps(weatherresp, indent=2)
# data = json.loads(weather_formatted_str)
# # print(data['weather', 'description'])

# for foo in data['weather']:
#     dec = foo['description']
# nam = data['name']    
# print(dec + ic + mai + nam)   


# foo = f"https://api.openweathermap.org/data/2.5/weather?{query}{keyapi}"
# print(foo)

# response = requests.get("https://randomfox.ca/floof")
# fox = response.json()
# print(fox['image'])
