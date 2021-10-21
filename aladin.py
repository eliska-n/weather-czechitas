import requests
from datetime import datetime, timedelta


# documentation: http://portal.chmi.cz/files/portal/docs/meteo/ov/aladin/produkty.html

location = "latitude=50.073658&longitude=14.418540"
url = "https://aladinonline.androworks.org/get_data.php?" + location

response = requests.get(url).json()
print(response)


forecastLength = response['forecastLength']

for i in range(forecastLength):    
    #date = datetime.utcfromtimestamp(row['Date']) # UTC time!


    forecastTime = datetime.strptime(response['forecastTimeIso'], "%Y-%m-%d %H:%M:%S")
    date = forecastTime + timedelta(hours=i)

    print(date.strftime('%Y-%m-%d %H:%M:%S'))

    dict_row = {      
        'dt': date, #.strftime('%Y-%m-%d %H:%M:%S'),
        'date': date.date(),
        'temp_min': response['parameterValues']['TEMPERATURE'][i],
        'temp_max': response['parameterValues']['TEMPERATURE'][i],
        'prediction_dt': datetime.now(),
        'prediction_source': 'aladin',
        'place': location,
        'rain_pct': None,
        'rain_mm': response['parameterValues']['PRECIPITATION_TOTAL'][i],
    }

    
    print(dict_row)