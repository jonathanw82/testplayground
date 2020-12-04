import os, requests, json
from flask import Flask, render_template
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
keyweather = os.getenv('WEATHER_KEY')
keygeo = os.getenv('GEO_KEY')
userinput = 'BRISTOL'


@app.route("/")
def index():
    return render_template("index.html", page_title="Home")


@app.route("/speechrecog")
def speechrecog():
    return render_template("speechrecog.html", page_title="speech rec")


@app.route("/speechtext")
def speechtext():
    return render_template("speechtext.html", page_title="speech Text")


@app.route("/weather")
def weather():
    queryweather = "q=" + userinput + ",GB&units=metric"
    keyweatherapi = '&appid=' + keyweather
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?{queryweather}{keyweatherapi}")
    weatherresp = response.json()
    weather_formatted_str = json.dumps(weatherresp, indent=2)
    data = json.loads(weather_formatted_str)

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
    # for co in data['coord']:
    #     lat = co['lat']
    #     lng = co['lon']

    # convert the wind direction to text
    val = int((wdir/22.5)+.5)
    arr = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    wdirection = arr[(val % 16)]

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
    return render_template("weather.html", page_title="weather api",
                            weather = context)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.getenv("DEVELOPMENT", False))
