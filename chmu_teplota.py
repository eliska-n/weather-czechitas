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

## Strips comments that are not static
keyss = [texts2[0][i]for i in range(0, len(texts2[0]))]
for x in keyss:
    y = re.sub("[\(].*?[\)]", "", x)
    x = y

## Removes space after city name form the table
for i in range(1, len(texts2)):
    texts2[i].pop(1)

## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
values = []
for i in range(len(keyss)):
    values.append([texts2[j][i] for j in range(1, len(texts2))])

data2 = {keyss[i]: values[j] for i in range(len(keyss)) for j in range(1, len(texts2))}
df = pd.DataFrame(data2, index=[0])

print (data2)

# #Third table - klimatické údaje
# #########################################
# ## Takes third table from tables
# table3 = tables[2]

# ## Extracts texts from rows - each row becomes an item in a list
# texts3 = []
# for row in table3.find_all("tr"):
#     row_texts = [cell.get_text() for cell in row.find_all("td")]
#     texts3.append(row_texts)

# ## Strips comments that are not static
# keysss = [texts3[i][0]for i in range(0, len(texts3))]
# xx = keysss[6]
# yy = re.sub("[\(].*?[\)]", "", xx)
# keysss[6] = yy

# ## Takes data only from the exact date
# texts3_in_date = [row[2] for row in texts3]

# ## Prepares the data for conversion into csv. Makes dictionary with keys as column names.
# data3 = {
#     keysss[i]: texts3_in_date[i] for i in range(1, len(keysss))
# }

# # Merges dictionaries
# data = data1 | data2 | data3
# df = pd.DataFrame(data, index=[0])
# df["date_stamp"] = datetime.today()
# return df