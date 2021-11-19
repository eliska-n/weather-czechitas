import pandas as pd
import datetime
import matplotlib.pyplot as plt
import re

# 1.) CHMI - TEPLOTY
df_chmi_temp = pd.read_csv("in/tables/chmu_tab_teplota.csv")

def chmitemptofloat(cell):
    TEMP_REGEX = re.compile(r"([\+-]?\d+(?:[\.,]\d+)?)")
    match = TEMP_REGEX.match(cell)
    if match:
        temp = float(match.group(1).replace(",", "."))
    else:
        temp = float("NaN")
    return temp
    
df_chmi_temp["Prumernateplota"] = df_chmi_temp["Prumernateplota"].apply(chmitemptofloat)
df_chmi_temp["Maximalniteplota"] = df_chmi_temp["Maximalniteplota"].apply(chmitemptofloat)
df_chmi_temp["Minimalniteplota"] = df_chmi_temp["Minimalniteplota"].apply(chmitemptofloat)
df_chmi_temp["date_stamp"] = pd.to_datetime(df_chmi_temp["date_stamp"], format = "%d/%m/%Y %H:%M:%S")

df_chmi_temp = df_chmi_temp[(df_chmi_temp["date_stamp"].dt.time.astype(str) == "19:00:00") | (df_chmi_temp["date_stamp"].dt.time.astype(str) == "20:00:00")]

df_chmi_temp = df_chmi_temp.drop(columns=['Teplotavzduchu', 'Teplotarosneho_bodu', 'Relativnivlhkost', 'Minimalniprizemni_teplota'])
df_chmi_temp = df_chmi_temp.rename(columns={"Stanice": "location", "Prumernateplota": "chmi_temp_avg", "Maximalniteplota": "chmi_temp_max", "Minimalniteplota": "chmi_temp_min"})

df_chmi_temp["forecast_date"] = (df_chmi_temp["date_stamp"] - datetime.timedelta(days = 1)).dt.strftime('%Y-%m-%d')
#########################################################################################################################################################
# 2.) CHMI - SRAZKY
df_chmi_rain = pd.read_csv("in/tables/out-tables-chmu_tab_srazky-csv.csv")

df_chmi_rain = df_chmi_rain.drop(columns=['Srazky_za_posledni_hodinu', 'Srazky_za_12_hodin', 'Celkova_snehova_pokryvka_cm'])
df_chmi_rain = df_chmi_rain.rename(columns={"Stanice": "location", "Srazky_za_24_hodin": "chmi_rain", "Novy_snih_cm": "chmi_snow"})

df_chmi_rain["chmi_rain"] = df_chmi_rain["chmi_rain"].apply(chmitemptofloat)
df_chmi_rain["chmi_snow"] = df_chmi_rain["chmi_snow"].apply(chmitemptofloat)
df_chmi_rain["date_stamp"] = pd.to_datetime(df_chmi_rain["date_stamp"], format = "%d/%m/%Y %H:%M:%S")

df_chmi_rain = df_chmi_rain[(df_chmi_rain["date_stamp"].dt.time.astype(str) == "19:00:00") | (df_chmi_rain["date_stamp"].dt.time.astype(str) == "20:00:00")]

df_chmi_rain["forecast_date"] = (df_chmi_rain["date_stamp"] - datetime.timedelta(days = 1)).dt.strftime('%Y-%m-%d')

df_chmi_rain.loc[df_chmi_rain["chmi_rain"] > 0, "chmi_rain_bool"] = True
df_chmi_rain.loc[df_chmi_rain["chmi_rain"] == 0, "chmi_rain_bool"] = False
#############################################################################################################################################################
# 3.) WEATHER.COM
df_weathercom = pd.read_csv("in/tables/weathercom_tab-csv.csv")

df_weathercom = df_weathercom.drop(columns=['city', 'country', 'humidity', 'locationId', 'state', 'windDirection', 'windSpeed', 'zipCode'])

df_weathercom["date_stamp"] = pd.to_datetime(df_weathercom["date_stamp"])
df_weathercom = df_weathercom[(df_weathercom["date_stamp"].dt.time.astype(str) == "19:00:00") | (df_weathercom["date_stamp"].dt.time.astype(str) == "20:00:00")]

def todt(time):
    time = str(time)
    time = time.rstrip(time[-12:])
    time = pd.to_datetime(time)
    return time
df_weathercom["time"] = df_weathercom["time"].apply(todt)

def temptomax(temperature):
    TEMP_REGEX2 = re.compile(r"([\+-]?\d+)(?:[\/])([\+-]?.+)")
    match = TEMP_REGEX2.match(temperature)
    if match:
        temp = float(match.group(1))
    else:
        temp = float("NaN")
    return temp

def temptomin(temperature):
    TEMP_REGEX2 = re.compile(r"([\+-]?.+)(?:[\/])([\+-]?\d+)")
    match = TEMP_REGEX2.match(temperature)
    if match:
        temp = float(match.group(2))
    else:
        temp = float("NaN")
    return temp
    
df_weathercom["wc_temp_max"] = df_weathercom["temperature"].apply(temptomax)
df_weathercom["wc_temp_min"] = df_weathercom["temperature"].apply(temptomin)

df_weathercom = df_weathercom.drop(columns=['temperature'])

df_weathercom.loc[df_weathercom['forecast'].str.contains('Rain|Showers|Storm', regex=True), 'rain_bool'] = True
df_weathercom.loc[df_weathercom['rain_bool'].isna(), 'rain_bool'] = False

def forecastdays(date_stamp, time):
    delta = datetime.datetime.date(time) - datetime.datetime.date(date_stamp)
    return float(str(delta)[0])

df_weathercom["wc_fday"] = df_weathercom.apply(lambda x: forecastdays(x["date_stamp"], x["time"]), axis=1)

df_weathercom = df_weathercom.rename(columns={"time": "forecast_date", "location_name": "location"})
df_weathercom["source"] = "weathercom"
df_weathercom["forecast_date"] = df_weathercom["forecast_date"].dt.strftime('%Y-%m-%d')
df_weathercom = df_weathercom[df_weathercom["wc_fday"] > 0]
############################################################################################################
# 4.) YR.NO
df_yrno = pd.read_csv("in/tables/yr_tab.csv")
df_yrno = df_yrno.rename(columns={"air_temperature_C": "yr_temp", "precipitation_amount_mm": "yr_rain"})

df_yrno["date_stamp"] = pd.to_datetime(df_yrno["date_stamp"])
df_yrno = df_yrno[(df_yrno["date_stamp"].dt.time.astype(str) == "19:00:00") | (df_yrno["date_stamp"].dt.time.astype(str) == "20:00:00")]

df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=1)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=2)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 1
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=2)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=3)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 2
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=3)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=4)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 3
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=4)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=5)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 4
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=5)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=6)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 5
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=6)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=7)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 6
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=7)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=8)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 7
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=8)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=9)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 8
df_yrno.loc[(df_yrno["start"] >= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=9)) + datetime.timedelta(hours=6))) & 
        (df_yrno["end"] <= (pd.to_datetime(df_yrno["date_stamp"].dt.date + datetime.timedelta(days=10)) + datetime.timedelta(hours=6)))
            , ["yr_fday"]] = 9

df_yrno_g = df_yrno.groupby(['location', 'date_stamp', 'yr_fday', 'source']).agg({'yr_temp':['mean', 'max', 'min'], 
                         'yr_rain':'sum'}).reset_index()

df_yrno_g.columns = ['_'.join(col).strip('_') for col in df_yrno_g.columns.values]

def makefdate(dstamp, fday):
    forecast_date = datetime.datetime.date(dstamp) + datetime.timedelta(days = fday)
    return forecast_date
    
df_yrno_g["forecast_date"] = df_yrno_g.apply(lambda x: makefdate(x["date_stamp"], x["yr_fday"]), axis=1)
df_yrno_g["forecast_date"] = pd.to_datetime(df_yrno_g["forecast_date"]).dt.strftime('%Y-%m-%d')

df_yrno_g.loc[df_yrno_g["yr_rain_sum"] > 0, "rain_bool"] = True
df_yrno_g.loc[df_yrno_g["yr_rain_sum"] == 0, "rain_bool"] = False

######################################################################################################
# 5.) OPENWEATHER
df_ow = pd.read_csv("in/tables/openweather_tab.csv")
df_ow["temp_mean"] = df_ow[["temp_day", "temp_eve", "temp_morn", "temp_night"]].mean(axis=1)
df_ow = df_ow.drop(columns=["humidity", "temp_day", "temp_eve", "temp_morn", "temp_night"])
df_ow["fday"] = pd.to_numeric(((pd.to_datetime(df_ow["forecast_dt"]).dt.date) - (pd.to_datetime(df_ow["date_stamp"]).dt.date)).astype("string").str.strip(" days"))
df_ow["forecast_dt"] = pd.to_datetime(df_ow["forecast_dt"]).dt.strftime('%Y-%m-%d')
df_ow = df_ow.rename(columns={"forecast_dt": "forecast_date"})
df_ow["date_stamp"] = pd.to_datetime(df_ow["date_stamp"])
df_ow = df_ow[df_ow["fday"] > 0]
df_ow.loc[df_ow["rain"] > 0, "rain_bool"] = True
df_ow.loc[df_ow["rain"].isna(), "rain_bool"] = False

###################################################################################################
# 6.) JOINOVÁNÍ
df_weathercom = df_weathercom.rename(columns={"wc_temp_max": "temp_max", "wc_temp_min": "temp_min", "wc_fday": "fday"})
df_yrno_g = df_yrno_g.rename(columns={"yr_temp_max": "temp_max", "yr_temp_min": "temp_min", "yr_temp_mean": "temp_mean", "yr_rain_sum": "rain", "yr_fday": "fday"})

df_forecasts = pd.concat([df_weathercom, df_yrno_g, df_ow])
df_chmi = pd.merge(df_chmi_temp, df_chmi_rain, on = ["date_stamp", "forecast_date", "location"], how = "left")
df_joined = pd.merge(df_forecasts, df_chmi, on = ["forecast_date", "location"], how = "left", suffixes=('_f', '_chmi'))

gps = {'location': ['Cheb', 'Karlovy Vary', 'Přimda', 'Kopisty', 'Tušimice', 'Plzeň-Mikulka', 'Churáňov', 'Milešovka', 'Kocelovice', 'Ústí nad Labem', 'Doksany', 'Praha-Ruzyně', 'Praha-Karlov', 'Praha-Libuš', 'Temelín', 'České Budějovice', 'Praha-Kbely', 'Liberec', 'Jičín', 'Čáslav', 'Košetice', 'Kostelní Myslová', 'Pec pod Sněžkou', 'Pardubice', 'Přibyslav', 'Polom', 'Ústí nad Orlicí', 'Svratouch', 'Náměšť nad Oslavou', 'Dukovany', 'Kuchařovice', 'Luká', 'Brno-Tuřany', 'Šerák', 'Prostějov', 'Červená u Libavé', 'Holešov', 'Ostrava-Mošnov', 'Lysá hora', 'Maruška'],
       'latitude': ['50.0683', '50.2016', '49.6694', '50.544', '50.3765', '49.7645', '49.0683', '50.5549', '49.4672', '50.6833', '50.4587', '50.1003', '50.0691', '50.0077', '49.1975', '48.9519', '50.1232', '50.7697', '50.4393', '49.9407', '49.5735', '49.159', '50.6918', '50.0158', '49.5825', '50.3503', '49.9801', '49.735', '49.1708', '49.0954', '48.8809', '49.6522', '49.153', '50.1874', '49.4525', '49.777', '49.3205', '49.6918', '49.5459', '49.365'], 
       'longitude': ['12.3913', '12.9139', '12.6779', '13.6227', '13.3279', '13.3787', '13.615', '13.9306', '13.8385', '14.041', '14.1699', '14.2555', '14.4276', '14.4467', '14.3421', '14.4697', '14.538', '15.0238', '15.3525', '15.3863', '15.0803', '15.4391', '15.7287', '15.7402', '15.7623', '16.3221', '16.4221', '16.0342', '16.1205', '16.1344', '16.0852', '16.9533', '16.6888', '17.1082', '17.1347', '17.5418', '17.5699', '18.1126', '18.4473', '17.8284']}
df_gps = pd.DataFrame.from_dict(gps, orient="columns")
df_gps["latitude"] = pd.to_numeric(df_gps["latitude"])
df_gps["longitude"] = pd.to_numeric(df_gps["longitude"])
df_joined = pd.merge(df_joined, df_gps, on = ["location"], how = "left")

df_joined.to_csv("out/tables/df_joined.csv", index=False)

####################################################################################################
# 7.) STATISTIKA
df_joined["temp_max_diff"] = df_joined["temp_max"] - df_joined["chmi_temp_max"]
df_joined["temp_min_diff"] = (df_joined["temp_min"] - df_joined["chmi_temp_min"])
df_joined["temp_mean_diff"] = (df_joined["temp_mean"] - df_joined["chmi_temp_avg"])
df_joined["rain_diff"] = (df_joined["rain"] - df_joined["chmi_rain"])
df_joined["temp_max_diff_abs"] = (df_joined["temp_max"] - df_joined["chmi_temp_max"]).abs()
df_joined["temp_min_diff_abs"] = (df_joined["temp_min"] - df_joined["chmi_temp_min"]).abs()
df_joined["temp_mean_diff_abs"] = (df_joined["temp_mean"] - df_joined["chmi_temp_avg"]).abs()
df_joined["rain_diff_abs"] = (df_joined["rain"] - df_joined["chmi_rain"]).abs()

df_joined.loc[((df_joined["rain_bool"] == True) & (df_joined["chmi_rain_bool"] == True)) | ((df_joined["rain_bool"] == False) & (df_joined["chmi_rain_bool"] == False)), "rain_match"] = 1
df_joined.loc[(df_joined["rain_bool"] == False) & (df_joined["chmi_rain_bool"] == True), "rain_falsenegative"] = 1
df_joined.loc[(df_joined["rain_bool"] == True) & (df_joined["chmi_rain_bool"] == False), "rain_falsepositive"] = 1

df_grouped1 = df_joined.groupby(["location","latitude", "longitude", "fday", "source"]).agg({'temp_max_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_min_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_mean_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'rain_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_max_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_min_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_mean_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_mean_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'rain_match':'sum', 
                                                       'rain_falsenegative': 'sum', 
                                                       'rain_falsepositive': 'sum',
                                                      }).reset_index()

df_grouped1.columns = ['_'.join(col).strip('_') for col in df_grouped1.columns.values]

df_grouped1["rain_match_percent"] = df_grouped1["rain_match_sum"] / (df_grouped1["rain_match_sum"] + df_grouped1["rain_falsenegative_sum"] + df_grouped1["rain_falsepositive_sum"])
df_grouped1["rain_falsenegative_percent"] = df_grouped1["rain_falsenegative_sum"] / (df_grouped1["rain_match_sum"] + df_grouped1["rain_falsenegative_sum"] + df_grouped1["rain_falsepositive_sum"])
df_grouped1["rain_falsepositive_percent"] = df_grouped1["rain_falsepositive_sum"] / (df_grouped1["rain_match_sum"] + df_grouped1["rain_falsenegative_sum"] + df_grouped1["rain_falsepositive_sum"])

df_grouped2 = df_joined.groupby(["source", "fday"]).agg({'temp_max_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_min_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_mean_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'rain_diff':['mean', 'median', 'std', 'var', 'count'], 
                                                       'temp_max_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_min_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_mean_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'temp_mean_diff_abs':['mean', 'median', 'std', 'var'], 
                                                       'rain_match':'sum', 
                                                       'rain_falsenegative': 'sum', 
                                                       'rain_falsepositive': 'sum',
                                                      }).reset_index()

df_grouped2.columns = ['_'.join(col).strip('_') for col in df_grouped2.columns.values]

df_grouped2["rain_match_percent"] = df_grouped2["rain_match_sum"] / (df_grouped2["rain_match_sum"] + df_grouped2["rain_falsenegative_sum"] + df_grouped2["rain_falsepositive_sum"])
df_grouped2["rain_falsenegative_percent"] = df_grouped2["rain_falsenegative_sum"] / (df_grouped2["rain_match_sum"] + df_grouped2["rain_falsenegative_sum"] + df_grouped2["rain_falsepositive_sum"])
df_grouped2["rain_falsepositive_percent"] = df_grouped2["rain_falsepositive_sum"] / (df_grouped2["rain_match_sum"] + df_grouped2["rain_falsenegative_sum"] + df_grouped2["rain_falsepositive_sum"])

df_grouped1.to_csv("out/tables/df_grouped1.csv", index=False)
df_grouped2.to_csv("out/tables/df_grouped2.csv", index=False)