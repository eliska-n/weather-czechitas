#https://pypi.org/project/metno-locationforecast/
#GPS stanic: https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice

from metno_locationforecast import Place, Forecast
import pandas as pd
from datetime import datetime

UserAgent = "novotna.elika@gmail.com"
places = {
    "Cheb" : Place("Cheb", 50.0683, 12.3913, 483),
    "Karlovy Vary" : Place("Karlovy Vary", 50.2016, 12.9139, 603), 
    "Přimda": Place("Přimda", 49.6694, 12.6779, 743), 
    "Kopisty": Place("Kopisty", 50.544, 13.6227, 240), 
    "Tušimice": Place("Tušimice", 50.3765, 13.3279, 322), 
    "Plzeň-Mikulka": Place("Plzeň-Mikulka", 49.7645, 13.3787, 360), 
    "Churáňov": Place("Churáňov", 49.0683, 13.615, 1118), 
    "Milešovka": Place("Milešovka", 50.5549, 13.9306, 831), 
    "Kocelovice": Place("Kocelovice", 49.4672, 13.8385, 519), 
    "Ústí nad Labem" : Place("Usti nad Labem", 50.6833, 14.041, 375),
    "Doksany": Place("Doksany", 50.4587, 14.1699, 158), 
    "Praha-Ruzyně": Place("Praha-Ruzyně", 50.1003, 14.2555, 364), 
    "Praha-Karlov": Place("Praha-Karlov", 50.0691, 14.4276, 261), 
    "Praha-Libuš": Place("Praha-Libuš", 50.0077, 14.4467, 302), 
    "Temelín": Place("Temelín", 49.1975, 14.3421, 500), 
    "České Budějovice": Place("České Budějovice", 48.9519, 14.4697, 395), 
    "Praha-Kbely": Place("Praha-Kbely", 50.1232, 14.538, 285), 
    "Liberec": Place("Liberec", 50.7697, 15.0238, 398), 
    "Jičín": Place("Jičín", 50.4393, 15.3525, 283), 
    "Čáslav": Place("Čáslav", 49.9407, 15.3863, 238), 
    "Košetice": Place("Košetice", 49.5735, 15.0803, 532), 
    "Kostelní Myslová": Place("Kostelní Myslová", 49.159, 15.4391, 569), 
    "Pec pod Sněžkou": Place("Pec pod Sněžkou", 50.6918, 15.7287, 816), 
    "Pardubice": Place("Pardubice", 50.0158, 15.7402, 224), 
    "Přibyslav": Place("Přibyslav", 49.5825, 15.7623, 532), 
    "Polom": Place("Polom", 50.3503, 16.3221, 747), 
    "Ústí nad Orlicí": Place("Ústí nad Orlicí", 49.9801, 16.4221, 402), 
    "Svratouch": Place("Svratouch", 49.735, 16.0342, 734), 
    "Náměšť nad Oslavou": Place("Náměšť nad Oslavou", 49.1708, 16.1205, 474), 
    "Dukovany": Place("Dukovany", 49.0954, 16.1344, 400), 
    "Kuchařovice": Place("Kuchařovice", 48.8809, 16.0852, 334), 
    "Luká": Place("Luká", 49.6522, 16.9533, 510), 
    "Brno-Tuřany": Place("Brno-Tuřany", 49.153, 16.6888, 241), 
    "Šerák": Place("Šerák", 50.1874, 17.1082, 1328), 
    "Prostějov": Place("Prostějov", 49.4525, 17.1347, 215), 
    "Červená u Libavé": Place("Červená u Libavé", 49.777, 17.5418, 748), 
    "Holešov": Place("Holešov", 49.3205, 17.5699, 222), 
    "Ostrava-Mošnov": Place("Ostrava-Mošnov", 49.6918, 18.1126, 253), 
    "Lysá hora": Place("Lysá hora", 49.5459, 18.4473, 1322), 
    "Maruška": Place("Maruška", 49.365, 17.8284, 664), 
}

def makeforecast(location):
    location_forecast = Forecast(location, UserAgent)
    location_forecast.update()
    keys = ["start",
        "end", 
        "duration", 
        "air_temperature_C",
        "precipitation_amount_mm", 
        "date_stamp"
        ]
    yrdf = pd.DataFrame(columns = keys, index=[0])

    for i in range(len(location_forecast.data.intervals)):
        interval = location_forecast.data.intervals[i]
        start = str(interval.start_time)
        end = str(interval.end_time)
        duration = str(interval.duration)
        if 'air_temperature' in interval.variables.keys():
            temperature = interval.variables['air_temperature']
            t_value = temperature.value
        if 'precipitation_amount' in interval.variables.keys():
            rain = interval.variables["precipitation_amount"]
            r_value = rain.value
        else:
            t_value = ""
            r_value = ""

        interval_dict = {
            "start": start, 
            "end": end, 
            "duration": duration, 
            "air_temperature_C": t_value,
            "precipitation_amount_mm": r_value
            }
        yrdf = yrdf.append(interval_dict, ignore_index = True)
    
    yrdf = yrdf.drop([0])
    now = datetime.now()
    yrdf["date_stamp"] = now.strftime("%Y-%m-%d %H:00:00")
    return yrdf

keys2 = [
    "location",
    "start",
    "end", 
    "duration", 
    "air_temperature_C",
    "precipitation_amount_mm", 
    "date_stamp"
    ]

result_yrdf = pd.DataFrame(columns = keys2, index=[0])

for name, place in places.items():
    df = makeforecast(place)
    df["location"] = name
    result_yrdf = result_yrdf.append(df, ignore_index = True)
    
result_yrdf = result_yrdf.drop([0])
result_yrdf["source"] = "yrno"
result_yrdf.to_csv("yr_tab.csv", index=False)


