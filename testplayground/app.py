import os, requests, json
from flask import Flask, render_template
from os import path
import weathercom
if path.exists("env.py"):
    import env

app = Flask(__name__)
keyweather = os.getenv('WEATHER_KEY')
keygeo = os.getenv('GEO_KEY')
userinputgeo = 'bs29up'
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


@app.route("/weathercomapi")
def weathercomapi():
    # check for single or double quotes
    # https://pypi.org/project/weathercom/
    tenday = weathercom.getCityWeatherDetails(city="bs273al", queryType="ten-days-data")
    forcast = json.loads(tenday)
    day = forcast['vt1dailyForecast']['dayOfWeek'][0]
    tempnow = forcast['vt1dailyForecast']['day']['temperature'][0]
    iconnow = forcast['vt1dailyForecast']['day']['icon'][0]
  

    context = {
       
        'today': day,
        'todaytemp': tempnow,
        'todayicon': iconnow,
         
        # 'day1pop': day1pop,
        # 'day1rain': day1rain,
        # 'day1snow': day1snow,

        # 'day2min': "%.0f" % day2min,
        # 'day2max': "%.0f" % day2max,
        # 'day2desc': day2desc,
        # 'icon2': icon2,
        # 'day2pop': day2pop,
        # 'day2rain': day2rain,
        # 'day2snow': day2snow,

        
    }
    return render_template("weathercom.html", page_title="Nested dictionary", weather=context)


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
    # split area at the comma then get the first word
    area = areapreslice.split(',')[0].split(' ')[0]
    # get the exact long and lat to 2 decimal places
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
    # probability of rain 1-0 pop times by 100 so 1=100 0.50=50 
    chanceofprecip = weatherdata['daily'][0]['pop']*100
    percipnow = "%.0f" % chanceofprecip

    for wdata in weatherdata['current']['weather']:
        dec = wdata['description']
        icon = wdata['icon']

    iconnow = f"http://openweathermap.org/img/wn/{icon}.png"

    current_temp = weatherdata['current']['temp']
    humid = weatherdata['current']['humidity']
    feels_like = weatherdata['daily'][0]['feels_like']['day']
    current_min = weatherdata['daily'][0]['temp']['min']
    current_max = weatherdata['daily'][0]['temp']['max']

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
    wspeed_con = (wspeed * 2.237) # convert to mph
    alertcurrent = weatherdata['current'].get('alert')
    
    wdcurrent = weatherdata['current']['wind_deg']
    val1 = int((wdcurrent/22.5)+.5)
    arr = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    wdirectioncurrent = arr[(val1 % 16)]
     

    # forcast days
    day1min = weatherdata['daily'][1]['temp']['min']
    day1max = weatherdata['daily'][1]['temp']['max']
    for weatherday1 in weatherdata['daily'][1]['weather']:
        day1desc = weatherday1['description']
        day1icon = weatherday1['icon']
    icon1 = f"http://openweathermap.org/img/wn/{day1icon}.png"
    day1pop = weatherdata['daily'][1]['pop']*100
    # if the key is not always availble use .get it will return none if the
    # key not present
    day1rain = weatherdata['daily'][1].get('rain')  
    day1snow = weatherdata['daily'][1].get('snow')
   
    day2min = weatherdata['daily'][2]['temp']['min']
    day2max = weatherdata['daily'][2]['temp']['max']
    for weatherday2 in weatherdata['daily'][2]['weather']:
        day2desc = weatherday2['description']
        day2icon = weatherday2['icon']
    icon2 = f"http://openweathermap.org/img/wn/{day2icon}.png"    
    day2pop = weatherdata['daily'][2]['pop']
    day2rain = weatherdata['daily'][2].get('rain')  
    day2snow = weatherdata['daily'][2].get('snow')

    day3min = weatherdata['daily'][3]['temp']['min']
    day3max = weatherdata['daily'][3]['temp']['max']
    for weatherday3 in weatherdata['daily'][3]['weather']:
        #day3desc = weatherday3['main']
        day3desc = weatherday3['description']
        day3icon = weatherday3['icon']
    day3pop = weatherdata['daily'][3]['pop']
    icon3 = f"http://openweathermap.org/img/wn/{day3icon}.png"
    day3rain = weatherdata['daily'][3].get('rain')  
    day3snow = weatherdata['daily'][3].get('snow')

    day4min = weatherdata['daily'][4]['temp']['min']
    day4max = weatherdata['daily'][4]['temp']['max']
    for weatherday4 in weatherdata['daily'][4]['weather']:
        day4desc = weatherday4['description']
        day4icon = weatherday4['icon']
    day4pop = weatherdata['daily'][4]['pop']
    icon4 = f"http://openweathermap.org/img/wn/{day4icon}.png"
    day4rain = weatherdata['daily'][4].get('rain')  
    day4snow = weatherdata['daily'][4].get('snow')

    day5min = weatherdata['daily'][5]['temp']['min']
    day5max = weatherdata['daily'][5]['temp']['max']
    for weatherday5 in weatherdata['daily'][5]['weather']:
        day5desc = weatherday5['description']
        day5icon = weatherday5['icon']
    day5pop = weatherdata['daily'][5]['pop']
    icon5 = f"http://openweathermap.org/img/wn/{day5icon}.png"
    day5rain = weatherdata['daily'][5].get('rain')  
    day5snow = weatherdata['daily'][5].get('snow')


    context = {
        'dec': dec,
        'area': area,
        'iconnow': iconnow,
        'percipnow': percipnow,
        'current_temp': "%.0f" % current_temp,
        'current_min': "%.0f" % current_min,
        'current_max': "%.0f" % current_max,
        'feels_like': round(feels_like),
        'humid': humid,
        'visname': visname,
        'wspeed_con': "%.2f" % wspeed_con,
        'wspeed': wspeed,
        'wdirectioncurrent': wdirectioncurrent,
        'alertcurrent': alertcurrent,
        
        'day1min': "%.0f" % day1min,
        'day1max': "%.0f" % day1max,
        'day1desc': day1desc,
        'icon1': icon1,
        'day1pop': "%.0f" % day1pop,
        'day1rain': day1rain,
        'day1snow': day1snow,

        'day2min': "%.0f" % day2min,
        'day2max': "%.0f" % day2max,
        'day2desc': day2desc,
        'icon2': icon2,
        'day2pop': "%.0f" % day2pop,
        'day2rain': day2rain,
        'day2snow': day2snow,

        'day3min': "%.0f" % day3min,
        'day3max': "%.0f" % day3max,
        'day3desc': day3desc,
        'icon3': icon3,
        'day3pop': "%.0f" % day3pop,
        'day3rain': day3rain,
        'day3snow': day3snow,

        'day4min': "%.0f" % day4min,
        'day4max': "%.0f" % day4max,
        'day4desc': day4desc,
        'icon4': icon4,
        'day4pop': "%.0f" % day4pop,
        'day4rain': day4rain,
        'day4snow': day4snow,

        'day5min': "%.0f" % day5min,
        'day5max': "%.0f" % day5max,
        'day5desc': day5desc,
        'icon5': icon5,
        'day5pop': "%.0f" % day5pop,
        'day5rain': day5rain,
        'day5snow': day5snow,

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
