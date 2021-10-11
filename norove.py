#https://pypi.org/project/metno-locationforecast/
#GPS stanic: https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice

from metno_locationforecast import Place, Forecast
import pandas as pd
import datetime

UserAgent = "novotna.elika@gmail.com"
usti = Place("Usti nad Labem", 50.6833, 14.041, 375)
usti_forecast = Forecast(usti, UserAgent)
usti_forecast.update()

first_interval = usti_forecast.data.intervals[0]
start = str(first_interval.start_time)
end = str(first_interval.end_time)
duration = str(first_interval.duration)
temperature = first_interval.variables['air_temperature']
rain = first_interval.variables["precipitation_amount"]
t_value = temperature.value
r_value = rain.value


yrdict = {
    "start": start, 
    "end": end, 
    "duration": duration, 
    "air_temperature_C": t_value,
    "precipitation_amount_mm": r_value
    }


print(yrdict)