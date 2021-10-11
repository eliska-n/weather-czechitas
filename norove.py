#https://pypi.org/project/metno-locationforecast/
#GPS stanic: https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice

from metno_locationforecast import Place, Forecast
import pandas as pd

UserAgent = "novotna.elika@gmail.com"
usti = Place("Usti nad Labem", 50.6833, 14.041, 375)
usti_forecast = Forecast(usti, UserAgent)
usti_forecast.update()

keys = vars(usti_forecast.data).keys()


print(usti_forecast.data.intervals)