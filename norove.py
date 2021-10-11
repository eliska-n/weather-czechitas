#https://pypi.org/project/metno-locationforecast/
#GPS stanic: https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice

from metno_locationforecast import Place, Forecast
import pandas as pd
from datetime import datetime

UserAgent = "novotna.elika@gmail.com"
usti = Place("Usti nad Labem", 50.6833, 14.041, 375)
usti_forecast = Forecast(usti, UserAgent)
usti_forecast.update()

keys = ["start",
        "end", 
        "duration", 
        "air_temperature_C",
        "precipitation_amount_mm"
        ]
yrdf = pd.DataFrame(columns = keys, index=[0])
for i in range(len(usti_forecast.data.intervals)):
    interval = usti_forecast.data.intervals[i]
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
yrdf["date_stamp"] = now.strftime("%d/%m/%Y %H:00:00")
yrdf.to_csv("yr_tab.csv", index=False)


