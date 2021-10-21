#https://pypi.org/project/metno-locationforecast/
#GPS stanic: https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice

from metno_locationforecast import Place, Forecast
import pandas as pd
from datetime import datetime

UserAgent = "novotna.elika@gmail.com"
places = [Place("Usti nad Labem", 50.6833, 14.041, 375)]



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

keys = ["start",
    "end", 
    "duration", 
    "air_temperature_C",
    "precipitation_amount_mm", 
    "date_stamp"
    ]
result_yrdf = pd.DataFrame(columns = keys, index=[0])

for place in places:
    result_yrdf = result_yrdf.append(makeforecast(place), ignore_index = True)

result_yrdf.to_csv("yr_tab.csv", index=False)


