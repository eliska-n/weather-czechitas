#https://openweathermap.org/api/one-call-api

import pandas as pd
import datetime
import requests

locations = {
    "Cheb" : "latitude=50.0683&longitude=12.3913",
    "Karlovy Vary" : "latitude=50.2016&longitude=12.9139", 
    "Přimda": "latitude=49.6694&longitude=12.6779", 
    "Kopisty": "latitude=50.544&longitude=13.6227", 
    "Tušimice": "latitude=50.3765&longitude=13.3279", 
    "Plzeň-Mikulka": "latitude=49.7645&longitude=13.3787", 
    "Churáňov": "latitude=49.0683&longitude=13.615",
    "Milešovka": "latitude=50.5549&longitude=13.9306",
    "Kocelovice": "latitude=49.4672&longitude=13.8385", 
    "Ústí nad Labem" : "latitude=50.6833&longitude=14.041",
    "Doksany": "latitude=50.4587&longitude=14.1699", 
    "Praha-Ruzyně": "latitude=50.1003&longitude=14.2555", 
    "Praha-Karlov": "latitude=50.0691&longitude=14.4276", 
    "Praha-Libuš": "latitude=50.0077&longitude=14.4467", 
    "Temelín": "latitude=49.1975&longitude=14.3421",
    "České Budějovice": "latitude=48.9519&longitude=14.4697",
    "Praha-Kbely": "latitude=50.1232&longitude=14.538",
    "Liberec": "latitude=50.7697&longitude=15.0238",
    "Jičín": "latitude=50.4393&longitude=15.3525",
    "Čáslav": "latitude=49.9407&longitude=15.3863",
    "Košetice": "latitude=49.5735&longitude=15.0803",
    "Kostelní Myslová": "latitude=49.159&longitude=15.4391",
    "Pec pod Sněžkou": "latitude=50.6918&longitude=15.7287",
    "Pardubice": "latitude=50.0158&longitude=15.7402",
    "Přibyslav": "latitude=49.5825&longitude=15.7623",
    "Polom": "latitude=50.3503&longitude=16.3221",
    "Ústí nad Orlicí": "latitude=49.9801&longitude=16.4221",
    "Svratouch": "latitude=49.735&longitude=16.0342",
    "Náměšť nad Oslavou": "latitude=49.1708&longitude=16.1205",
    "Dukovany": "latitude=49.0954&longitude=16.1344",
    "Kuchařovice": "latitude=48.8809&longitude=16.0852",
    "Luká": "latitude=49.6522&longitude=16.9533",
    "Brno-Tuřany": "latitude=49.153&longitude=16.6888",
    "Šerák": "latitude=50.1874&longitude=17.1082",
    "Prostějov": "latitude=49.4525&longitude=17.1347",
    "Červená u Libavé": "latitude=49.777&longitude=17.5418",
    "Holešov": "latitude=49.3205&longitude=17.5699",
    "Ostrava-Mošnov": "latitude=49.6918&longitude=18.1126",
    "Lysá hora": "latitude=49.5459&longitude=18.4473",
    "Maruška": "latitude=49.365&longitude=17.8284"
}

for key, value in locations.items():
    locations[key] = value.replace("latitude=", "").replace("&longitude=", ",").split(",")

def makeforecast(lat, lon):
    API_key = "95f5a5295826bb66026e9cbad7be902d"
    part = "current,minutely,hourly,alerts"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude={part}&appid={API_key}"
    response = requests.get(url).json()
    forecasts = []
    for i in range(8):
        dt = datetime.datetime.fromtimestamp(int(response['daily'][i]['dt']))
        if 'humidity' in response['daily'][i].keys():
            humidity = response['daily'][i]['humidity']
        else: humidity = None
        if 'rain' in response['daily'][i].keys():
            rain = response['daily'][i]['rain']
        else: rain = None
        if 'snow' in response['daily'][i].keys():
            snow = response['daily'][i]['snow']
        else: snow = None
        if 'temp' in response['daily'][i].keys():
            if 'day' in response['daily'][i]['temp'].keys(): temp_day = response['daily'][i]['temp']['day'] 
            else: temp_day = None
            if 'eve' in response['daily'][i]['temp'].keys(): temp_eve = response['daily'][i]['temp']['eve']
            else: temp_eve = None
            if 'max' in response['daily'][i]['temp'].keys(): temp_max = response['daily'][i]['temp']['max']
            else: temp_max = None
            if 'min' in response['daily'][i]['temp'].keys(): temp_min = response['daily'][i]['temp']['min']
            else: temp_min = None
            if 'morn' in response['daily'][i]['temp'].keys(): temp_morn = response['daily'][i]['temp']['morn']
            else: temp_morn = None
            if 'night' in response['daily'][i]['temp'].keys(): temp_night = response['daily'][i]['temp']['night']
            else: temp_night = None
        interval_dict = {
            "forecast_dt": dt,
            "humidity": humidity, 
            "rain": rain, 
            "snow": snow,
            "temp_day": temp_day, 
            "temp_eve": temp_eve,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "temp_morn": temp_morn,
            "temp_night": temp_night,
            }
        df = pd.DataFrame(interval_dict, index=[0])
        forecasts.append(df)
    forecast_df = pd.concat(forecasts)
    return forecast_df

frames = []

for key, value in locations.items():
    lat = value[0]
    lon = value[1]
    name = key
    forecast = makeforecast(lat, lon)
    forecast["location"] = name
    forecast["date_stamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:00:00")
    frames.append(forecast)

result_df = pd.concat(frames)
result_df["source"] = "openweather"
result_df.to_csv("openweather_tab.csv", index=False)