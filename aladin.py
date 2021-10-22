import requests
from datetime import datetime, timedelta
import pandas as pd

# documentation: http://portal.chmi.cz/files/portal/docs/meteo/ov/aladin/produkty.html
#K dispozici jsou předpovědi numerického modelu ALADIN pro každou hodinu předpovědní doby. Délka předpovědi pro hlavní termíny (počátky předpovědi v 00 a 12 UTC) je 54 hod
#prediction_dt_stamp bude v utc, protože to poběží v keboole
#forecast_dt_start je v českém čase (utc+2), protže takhle to dává aladin

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

def getforecast(location):
    url = "https://aladinonline.androworks.org/get_data.php?" + location
    response = requests.get(url).json()

    forecastLength = response['forecastLength']
    series = []

    for i in range(forecastLength):    
        #date = datetime.utcfromtimestamp(row['Date']) # UTC time!
        forecastTime = datetime.strptime(response['forecastTimeIso'], "%Y-%m-%d %H:%M:%S")
        date = forecastTime + timedelta(hours=i)

        dict_row = {      
            'forecast_dt_start': date, #.strftime('%Y-%m-%d %H:%M:%S'),
            'forecast_date': date.date(),
            'prediction_dt_stamp': datetime.now().strftime("%Y-%m-%d %H:00:00"),
            'prediction_source': 'aladin',
            'rain_mm': response['parameterValues']['PRECIPITATION_TOTAL'][i],
            'snow': response['parameterValues']['PRECIPITATION_SNOW'][i],
            'temp': response['parameterValues']['TEMPERATURE'][i],
            'humidity': response['parameterValues']['HUMIDITY'][i],
        }
        df = pd.DataFrame(dict_row, index=[0])
        series.append(df)
    
    location_df = pd.concat(series)
    return location_df

forecasts=[]

for name, place in locations.items():
    df = getforecast(place)
    df["location"] = name
    forecasts.append(df)

aladin_df = pd.concat(forecasts)
aladin_df.to_csv("aladin_tab.csv", index=False)
