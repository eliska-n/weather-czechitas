from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import re

url = "https://www.chmi.cz/files/portal/docs/meteo/opss/pocasicko_nove/st_teploty_cz.html" #Prehled teplot a relativni vlhkosti vzduchu na stanicich
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
keyss = [texts2[0][i]for i in range(0, len(texts2[0]))]
for x in keyss:
    y = re.sub("[\(].*?[\)]", "", x)
    x = y

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
df.to_csv("chmu_tab_teplota.csv", index=False)

