from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import pandas as pd

url = "https://www.chmi.cz/files/portal/docs/meteo/opss/pocasicko_nove/st_srazky_cz.html" #Prehled teplot a relativni vlhkosti vzduchu na stanicich
http = urllib3.PoolManager()
response = http.request('GET', url)
soup = BeautifulSoup(response.data, "lxml")

#Finds everything inside all html <table> tags
tables = soup.find_all("table")

#Second table - to get all the data
#########################################
## Takes second table from tables
table2 = tables[1]

## Extracts texts from rows - each row becomes an item in a list
texts2 = []
for row in table2.find_all("tr"):
    row_texts = [cell.get_text() for cell in row.find_all("td")]
    texts2.append(row_texts)

## Strips comments that are in brackets
keyss = ["Stanice", "Srazky_za_posledni_hodinu", "Srazky_za_12_hodin", "Srazky_za_24_hodin", "Novy_snih_cm", "Celkova_snehova_pokryvka_cm"]

## Removes space after city name form the table
for i in range(1, len(texts2)):
    texts2[i].pop(1)

## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
df = pd.DataFrame(columns = keyss, index=[0])

for row in texts2[1:len(texts2)]:
    dict = {keyss[i]: row[i] for i in range(len(keyss))}
    df = df.append(dict, ignore_index = True)

df = df.drop([0])
now = datetime.now()
df["date_stamp"] = now.strftime("%d/%m/%Y %H:00:00")
df.to_csv("chmu_tab_srazky.csv", index=False)
