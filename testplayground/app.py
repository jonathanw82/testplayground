import os, requests, json
from flask import Flask, render_template
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
keyweather = os.getenv('WEATHER_KEY')
keygeo = os.getenv('GEO_KEY')
userinputgeo = 'BS2 9UP'
userinput = 'CHEDDAR'


@app.route("/")
def index():
    return render_template("index.html", page_title="Home")


@app.route("/speechrecog")
def speechrecog():
    return render_template("speechrecog.html", page_title="speech rec")


@app.route("/speechtext")
def speechtext():
    return render_template("speechtext.html", page_title="speech Text")


@app.route("/acessnestdic")
def acessnestdic():
    
    return render_template("nestdic.html", page_title="Nested dictionary")


@app.route("/weather2")
def weather2():
    # -------- get the exact long litude and latitude fom the post code --------------
    geokeyapi = ',UK&key=' + keygeo
    responsegeo = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={userinputgeo}{geokeyapi}")
    geo = responsegeo.json()
    geofomat_str = json.dumps(geo, indent=2) 
    geodata = json.loads(geofomat_str)
    
    for georesults in geodata['results']:
        originallng = georesults['geometry']['lng']
        originallat = georesults['geometry']['lat']
        areapreslice = georesults['formatted']
    
    area = areapreslice.split(',')[0]

    exactlng = "%.2f" % originallng
    exactlat = "%.2f" % originallat



    #----------------------- get the exact weatherwith forcast------------------------

    queryweather = "lat=" + exactlat + "&lon=" + exactlng
    exclude = "&exclude=" + "minutely," + "alerts"
    units = "&units=" + "metric"
    keyweatherapi = '&appid=' + keyweather
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?{queryweather}{exclude}{units}{keyweatherapi}")
    weatherresp = response.json()
    weather_formatted_str = json.dumps(weatherresp, indent=2)
    weatherdata = json.loads(weather_formatted_str)
    for wdata in weatherdata['current']['weather']:
        dec = wdata['description']
        icon = wdata['icon']

    current_temp = weatherdata['current']['temp']
    humid = weatherdata['current']['humidity']
    feels_like = weatherdata['current']['feels_like']
    vis = weatherdata['current']['visibility']
    # Met office comparison https://www.metoffice.gov.uk/services/data/datapoint/code-definitions
    if vis <= 1000:
        visname = 'Very poor'
    if vis > 1000 < 4000:
        visname = 'Poor'
    if vis > 4000 < 9999:
        visname = 'Moderate'
    if vis >= 10000 < 19999:
        visname = 'Good'
    if vis >= 20000 < 39999:
        visname = 'Very Good'
    if vis >= 40000:
        visname = 'Excellent'          

    wspeed = weatherdata['current']['wind_speed']
    wspeed_con = (wspeed * 2.237)
    wdcurrent = weatherdata['current']['wind_deg']
    
    val1 = int((wdcurrent/22.5)+.5)
    arr = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    wdirectioncurrent = arr[(val1 % 16)]
     
    iconnow = f"http://openweathermap.org/img/wn/{icon}.png"
    
   


    context = {
        'dec': dec,
        'area': area,
        'iconnow': iconnow,
        'current_temp': current_temp,
        'feels_like': feels_like,
        'humid': humid,
        'visname': visname,
        'wspeed_con': "%.2f" % wspeed_con,
        'wspeed': wspeed,
        'wdirectioncurrent': wdirectioncurrent,
    }

    return render_template("weather2.html", page_title="Geo Weather",
                            geoweather = context)


@app.route("/weather")
def weather():
    # first get the post code and send it to OpenCage to get the Longlitude and latitude
    geokeyapi = ',UK&key=' + keygeo
    responsegeo = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={userinput}{geokeyapi}")
    geo = responsegeo.json()
    geofomat_str = json.dumps(geo, indent=2) 
    data = json.loads(geofomat_str)
   
    for bar in data['results']:
        originallng = bar['geometry']['lng']
        originallat = bar['geometry']['lat']

    exactlng = "%.2f" % originallng
    exactlat = "%.2f" % originallat
    print(exactlng)
    print(exactlat)

    # then get the exact weather for the specified loaction
    queryweather = "q=" + userinput + ",GB&units=metric"
    # queryweather = "lat=" + exactlat + "&lon=" + exactlng
    # exclude = "&exclude=" + "minutely, alerts"
    keyweatherapi = '&appid=' + keyweather
    response = requests.get(
         f"https://api.openweathermap.org/data/2.5/weather?{queryweather}{keyweatherapi}")
    # response = requests.get(
    #     f"https://api.openweathermap.org/data/2.5/onecall?{queryweather}{exclude}{keyweatherapi}")
    weatherresp = response.json()
    weather_formatted_str = json.dumps(weatherresp, indent=2)
    data = json.loads(weather_formatted_str)
    print(weather_formatted_str)
    for bar in data['weather']:
        dec = bar['description']

    temp = data['main']['temp']
    htemp = data['main']['temp_max']
    ltemp = data['main']['temp_min']
    wspeed = data['wind']['speed']
    wdir = data['wind']['deg']
    nam = data['name']
    
    lat = data['coord']['lat']
    lng = data['coord']['lon']
   
    # convert the wind direction to text
    val1 = int((wdir/22.5)+.5)
    arr = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    wdirection = arr[(val1 % 16)]

    context = {
        'dec':dec,
        'nam': nam,
        'temp': temp,
        'htemp': htemp,
        'ltemp': ltemp,
        'wspeed': wspeed,
        'wdirection': wdirection,
        'lng': lng,
        'lat': lat,
    }
    return render_template("weather.html", page_title="st weather api",
                            weather = context)

# def direction_to_compuss(dir_to_com):
#     val = int((dir_to_com/22.5)+.5)
#     arr = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
#     span = arr[(val % 16)]


if __name__ == "__main__":
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.getenv("DEVELOPMENT", False))
